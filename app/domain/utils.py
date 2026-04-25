import html


def sanitize_string(value: str) -> str:
    """
    Sanitizes a string by escaping HTML characters to prevent XSS attacks.

    Args:
        cls: The class that is calling this validator (not used in this function).
        value (str): The string value to be sanitized.
    Returns:
        str: The sanitized string.
    """
    if isinstance(value, str):
        return html.escape(value)
    return value