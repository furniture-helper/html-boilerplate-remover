from bs4 import BeautifulSoup, Comment


def _first_srcset_url(value: str) -> str | None:
    if not isinstance(value, str):
        return None
    first_entry = value.split(',', 1)[0].strip()
    if not first_entry:
        return None
    return first_entry.split()[0] if first_entry.split() else None


def clean_soup(soup: BeautifulSoup,
               remove_tags=True,
               remove_data_uris=True,
               strip_event_handlers=True,
               remove_style_attrs=True,
               remove_comments=True) -> BeautifulSoup:
    """
    Clean a BeautifulSoup document in-place and return it.
    - removes common non-content tags (scripts, styles, noscript, iframe, embed, object, base, link, meta)
    - removes images/sources that use `data:` URIs (base64)
    - strips inline event handlers (attributes starting with `on`)
    - removes `javascript:` href/src values
    - optionally removes `style` attributes
    """
    if remove_tags:
        for name in (
                'script', 'style', 'noscript', 'iframe', 'embed', 'object', 'base', 'link', 'form', 'input',
                'button', 'meta'):
            for tag in soup.find_all(name):
                tag.decompose()

    if remove_comments:
        for comment in soup.find_all(string=lambda s: isinstance(s, Comment)):
            comment.extract()

    if remove_data_uris:
        # Keep lazy-loading/media tags that still carry real URL candidates.
        keep_attrs = ('srcset', 'imagesrcset', 'data-brsrcset')

        # remove images and other tags with data: URIs in src/srcset/href
        for tag in soup.find_all():
            # If responsive image attrs exist, normalize src to the first candidate URL.
            for keep_attr in keep_attrs:
                keep_val = tag.get(keep_attr)
                if isinstance(keep_val, str) and keep_val.strip():
                    first_url = _first_srcset_url(keep_val)
                    if first_url:
                        tag['src'] = first_url
                        break

            keep_tag = any(isinstance(tag.get(a), str) and tag.get(a).strip() for a in keep_attrs)
            for attr in ('src', 'href', 'srcset', 'data-src', 'data'):
                val = tag.get(attr)
                if not val:
                    continue
                # handle srcset which may contain multiple items
                if attr == 'srcset' and 'data:' in val:
                    if keep_tag:
                        continue
                    tag.decompose()
                    break
                if isinstance(val, str) and val.strip().lower().startswith('data:'):
                    if keep_tag:
                        continue
                    tag.decompose()
                    break

    if strip_event_handlers or remove_style_attrs:
        for tag in soup.find_all():
            # remove inline event handlers like onclick, onmouseover, etc.
            if strip_event_handlers:
                for a in list(tag.attrs):
                    if a.lower().startswith('on'):
                        del tag.attrs[a]
            # remove javascript: links
            for a in ('href', 'src'):
                v = tag.get(a)
                if isinstance(v, str) and v.strip().lower().startswith('javascript:'):
                    del tag.attrs[a]
            # remove style attribute if requested
            if remove_style_attrs and 'style' in tag.attrs:
                del tag.attrs['style']

    return soup
