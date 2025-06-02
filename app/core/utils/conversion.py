import base64


def base10_to_urlsafe_base64(number: int, /) -> str:
    """Convert a base 10 number to URL-safe base 64 string.

    Args:
        number: Integer to convert

    Returns:
        URL-safe base64 string without padding.
    """
    byte_representation: bytes = number.to_bytes(
        (number.bit_length() + 7) // 8,
        byteorder="big",
    )

    return (
        base64.b64encode(byte_representation)
        .decode("utf-8")
        .replace("+", "-")
        .replace("/", "_")
        .rstrip("=")
    )
