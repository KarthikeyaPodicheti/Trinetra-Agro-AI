"""
Trinetra Agro AI - Translation Utility
Uses deep-translator (Google Translate, free, no API key) with caching.
"""

import streamlit as st
from typing import Optional

# Language code mapping
_LANG_CODES = {
    "English": "en",
    "Telugu (తెలుగు)": "te",
    "Hindi (हिंदी)": "hi",
}

# Google Translate has a ~5000 char limit per call; split if needed.
_MAX_CHARS = 4900


def _get_lang_code(language: str) -> str:
    return _LANG_CODES.get(language, "en")


@st.cache_data(show_spinner=False, ttl=3600)
def _cached_translate(text: str, target: str) -> str:
    """Translate *text* to *target* language code. Cached for 1 hour."""
    from deep_translator import GoogleTranslator

    # Split long texts into chunks
    if len(text) <= _MAX_CHARS:
        return GoogleTranslator(source="en", target=target).translate(text) or text

    parts, current = [], ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > _MAX_CHARS:
            parts.append(current)
            current = line
        else:
            current = f"{current}\n{line}" if current else line
    if current:
        parts.append(current)

    translator = GoogleTranslator(source="en", target=target)
    translated = []
    for part in parts:
        translated.append(translator.translate(part) or part)
    return "\n".join(translated)


def translate(text: str, language: Optional[str] = None) -> str:
    """
    Translate *text* into the selected language.

    - If *language* is None, reads from ``st.session_state.language``.
    - Returns the original text unchanged for English or empty/whitespace input.
    """
    if not text or not text.strip():
        return text

    if language is None:
        language = st.session_state.get("language", "English")

    code = _get_lang_code(language)
    if code == "en":
        return text

    try:
        return _cached_translate(text.strip(), code)
    except Exception:
        # If translation fails, return original text gracefully
        return text
