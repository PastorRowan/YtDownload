
from urllib.parse import urlparse

def isUrlValid(url: str) -> bool:

    try:

        parsed = urlparse(url.strip())

        return (
            parsed.scheme in ("http", "https")
            and parsed.netloc != ""
        )

    except Exception:
        return False
