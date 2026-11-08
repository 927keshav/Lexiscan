"""
3_nlp_engine/postprocessor.py
Clean, validate, merge, and format raw NER output into structured JSON.
"""
import re
import json
from datetime import datetime


# Date regex patterns
DATE_PATTERNS = [
    re.compile(r"\d{4}-\d{2}-\d{2}"),                          # YYYY-MM-DD
    re.compile(r"\d{2}/\d{2}/\d{4}"),                          # MM/DD/YYYY
    re.compile(r"[A-Z][a-z]+ \d{1,2},? \d{4}"),               # Month DD, YYYY
]

# Corresponding datetime formats for parsing
DATE_FORMATS = [
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%B %d, %Y",
    "%B %d %Y",
]


def _validate_date(text: str) -> str | None:
    """Validate and return a date string if it matches known patterns."""
    text = text.strip()
    for pattern in DATE_PATTERNS:
        if pattern.fullmatch(text):
            for fmt in DATE_FORMATS:
                try:
                    datetime.strptime(text, fmt)
                    return text
                except ValueError:
                    continue
    return None


def _normalize_amount(text: str) -> dict | None:
    """Normalize a dollar amount string to a float value."""
    raw = text.strip()
    cleaned = re.sub(r"[^\d.\-]", "", raw)
    if not cleaned:
        return None
    try:
        value = float(cleaned)
        return {"raw": raw, "value": value}
    except ValueError:
        return None


def _merge_consecutive_parties(entities: list) -> list:
    """Merge consecutive PARTY entities into single names."""
    if not entities:
        return []

    merged = []
    i = 0
    while i < len(entities):
        if entities[i]["label"] == "PARTY":
            parts = [entities[i]["text"]]
            start = entities[i]["start"]
            end = entities[i]["end"]
            j = i + 1
            while j < len(entities) and entities[j]["label"] == "PARTY":
                gap = entities[j]["start"] - end
                if gap <= 2:
                    parts.append(entities[j]["text"])
                    end = entities[j]["end"]
                    j += 1
                else:
                    break
            merged.append({
                "text": " ".join(parts),
                "label": "PARTY",
                "start": start,
                "end": end,
            })
            i = j
        else:
            merged.append(entities[i])
            i += 1

    return merged


def postprocess(ner_entities: list) -> dict:
    """
    Clean raw NER output and produce structured JSON.

    Args:
        ner_entities: List of dicts with keys: text, label, start, end.

    Returns:
        Dict matching the output JSON schema with keys:
        dates, parties, dollar_amounts, termination_clauses.
    """
    entities = _merge_consecutive_parties(ner_entities)

    dates = []
    parties = []
    dollar_amounts = []
    termination_clauses = []

    seen_parties = set()
    seen_dates = set()

    for ent in entities:
        label = ent.get("label", "")
        text = ent.get("text", "").strip()

        if not text:
            continue

        if label == "DATE":
            validated = _validate_date(text)
            if validated and validated not in seen_dates:
                dates.append(validated)
                seen_dates.add(validated)

        elif label == "PARTY":
            if text not in seen_parties:
                parties.append(text)
                seen_parties.add(text)

        elif label in ("DOLLAR", "AMOUNT"):
            amount = _normalize_amount(text)
            if amount is not None:
                dollar_amounts.append(amount)

        elif label == "TERM_CLAUSE":
            cleaned = " ".join(text.split())
            if cleaned:
                termination_clauses.append(cleaned)

    return {
        "dates": dates,
        "parties": parties,
        "dollar_amounts": dollar_amounts,
        "termination_clauses": termination_clauses,
    }


if __name__ == "__main__":
    sample_entities = [
        {"text": "Acme", "label": "PARTY", "start": 0, "end": 4},
        {"text": "Corp", "label": "PARTY", "start": 5, "end": 9},
        {"text": "Beta LLC", "label": "PARTY", "start": 14, "end": 22},
        {"text": "2025-01-15", "label": "DATE", "start": 33, "end": 43},
        {"text": "March 3, 2024", "label": "DATE", "start": 50, "end": 63},
        {"text": "$500,000", "label": "DOLLAR", "start": 70, "end": 78},
        {"text": "30 days notice required", "label": "TERM_CLAUSE", "start": 90, "end": 113},
    ]

    result = postprocess(sample_entities)
    print("Postprocessed output:")
    print(json.dumps(result, indent=2))
