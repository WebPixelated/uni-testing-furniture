import re


def parse_price(price_str: str) -> int:
    """
    Convert a price string from the site to an integer (rubles).

    Handles formats:
      '12 405'       →  12405  (catalog card, space as thousands separator)
      '12,015 ₽'     →  12015  (cart total, comma as thousands separator)
      '12 015'       →  12015
      ' 9 815 '      →  9815
    """
    # Keep only digits
    digits = re.sub(r"[^\d]", "", price_str)
    if not digits:
        raise ValueError(f"Cannot parse price from: {price_str!r}")
    return int(digits)


def parse_dimension(text: str) -> int | None:
    """
    Parses integers from a string with dimensions.
    Example:
    'Ширина: 1400 мм," -> 1400
    """
    match = re.search(r"(\d+)", text)
    if match:
        return int(match.group(1))
    return None
