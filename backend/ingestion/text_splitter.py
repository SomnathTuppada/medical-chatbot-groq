import re

MEDICAL_KEYWORDS = [
    "disease", "condition", "symptoms", "treatment", "diagnosis",
    "patient", "patients", "clinical", "therapy", "medicine",
    "blood", "infection", "syndrome", "disorder", "cells", "body"
]

BLOCKLIST_PATTERNS = [
    r"\bSTAFF\b",
    r"\bEDITOR\b",
    r"\bEDITORS\b",
    r"\bVOLUME\b",
    r"\bENCYCLOPEDIA\b",
    r"\bISBN\b",
    r"\bCOPYRIGHT\b"
]


def is_valid_chunk(chunk: str) -> bool:
    # Too short
    if len(chunk) < 300:
        return False

    # Blocklisted structural content
    for pattern in BLOCKLIST_PATTERNS:
        if re.search(pattern, chunk, re.IGNORECASE):
            return False

    # Sentence density check
    sentence_count = chunk.count(".")
    if sentence_count < 3:
        return False

    # Medical signal check
    lowered = chunk.lower()
    if not any(keyword in lowered for keyword in MEDICAL_KEYWORDS):
        return False

    return True


def split_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if is_valid_chunk(chunk):
            chunks.append(chunk)

        start = end - overlap

    return chunks
