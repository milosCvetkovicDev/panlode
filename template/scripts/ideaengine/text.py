"""Text helpers shared by the CLI and the validator."""

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
# Latin letters that have no Unicode decomposition, so NFKD alone would drop them.
_UNDECOMPOSED = str.maketrans({
    "đ": "dj", "Đ": "Dj", "æ": "ae", "Æ": "Ae", "œ": "oe", "Œ": "Oe", "ø": "o", "Ø": "O",
    "ł": "l", "Ł": "L", "þ": "th", "Þ": "Th", "ð": "d", "Ð": "D",
})


def slugify(text: str, max_len: int = 60) -> str:
    """ASCII file-name slug; Latin letters with diacritics map the same way from NFC and NFD input."""
    text = text.translate(_UNDECOMPOSED)
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in decomposed if not unicodedata.combining(c))
    slug = _NON_ALNUM.sub("-", ascii_text.casefold()).strip("-")
    if len(slug) > max_len:
        cut = slug.rfind("-", 0, max_len + 1)
        slug = (slug[:cut] if cut > 0 else slug[:max_len]).strip("-")
    return slug or "untitled"
