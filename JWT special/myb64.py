import base64

def base64url_encode(data: bytes) -> str:
    """Encode bytes to base64url (no padding, safe for URLs)"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def base64url_decode(data: str) -> bytes:
    """Decode base64url string back to bytes"""
    padding = len(data) % 4
    if padding:
        data += '=' * (4 - padding)
    return base64.urlsafe_b64decode(data)
