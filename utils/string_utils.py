import re


def replace_common_values_with_hashes(s: str) -> str:
    """
    Replace common variable values in `s` with '###'.
    This includes hexadecimal numbers and regular numbers.
    Example: 'color #ff0000 and order 123' -> 'color ### and order ###'
    """
    s = remove_product_tags(s)
    s = remove_product_cats(s)
    s = remove_uuids(s)
    s = replace_hexadecimal_numbers_with_hashes(s)
    s = replace_numbers_with_hashes(s)
    return s


def replace_hexadecimal_numbers_with_hashes(s: str) -> str:
    """
    Replace contiguous hexadecimal runs with `###` when:
    - the entire string is a hexadecimal token of length > 6 (e.g. an ID), OR
    - the hex run (length > 6) has whitespace or a hyphen immediately to the left or right.
    """
    # full-string hex (only hex chars) and length > 6
    if re.fullmatch(r'[0-9a-fA-F]{7,}', s):
        return "###"
    # match hex tokens of length > 6 that have whitespace or a hyphen on left or right
    _hex_re = re.compile(r'(?<=[\s\-])[0-9a-fA-F]{7,}|[0-9a-fA-F]{7,}(?=[\s\-])')
    return _hex_re.sub("###", s)


def remove_product_tags(s: str) -> str:
    """
    If a string in the form product-tag-dskjflj appears, replace it with '###'.
    This is common in e-commerce sites where tag IDs are embedded in class names or IDs.
    """
    _product_tag_re = re.compile(r'product_tag-[^\s]+')
    return _product_tag_re.sub("", s)


def remove_product_cats(s: str) -> str:
    _product_cat_re = re.compile(r'product_cat-[^\s]+')
    return _product_cat_re.sub("", s)


def remove_uuids(s: str) -> str:
    """
    Replace UUIDs in `s` with '###'.
    Example: 'user 123e4567-e89b-12d3-a456-426614174000' -> 'user ###'
    """
    _uuid_re = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
    return _uuid_re.sub("###", s)


def replace_numbers_with_hashes(s: str) -> str:
    """
    Replace contiguous sequences of digits of length > 3 with '###'.
    Example: 'order 123 on 20240101' -> 'order 123 on ###'
    """
    _number_re = re.compile(r"\d{4,}")
    return _number_re.sub("###", s)
