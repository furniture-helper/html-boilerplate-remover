from typing import Optional

from bs4 import BeautifulSoup

from utils.string_utils import replace_common_values_with_hashes


def get_attribute(element: BeautifulSoup, attr_name: str, replace_common_values: bool = True) -> str | list[str] | None:
    attribute: Optional[str] = element.get(attr_name) if hasattr(element, 'get') else None
    if isinstance(attribute, list):
        return [replace_common_values_with_hashes(attr) if replace_common_values else attr for attr in attribute]

    return replace_common_values_with_hashes(attribute) if attribute and replace_common_values else attribute


def get_direct_text(element: BeautifulSoup) -> str:
    if not hasattr(element, 'find_all'):
        return ""

    parts = [str(t) for t in element.find_all(string=True, recursive=False)]
    return " ".join(p for p in parts if p).strip()
