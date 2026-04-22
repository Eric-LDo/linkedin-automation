from typing import Optional


def remove_backslashes(value: Optional[str]) -> Optional[str]:
    if value is None:
        return value
    return value.replace("\\", "").strip()


def normalize_search_query(value: Optional[str], default_value: Optional[str] = None) -> Optional[str]:
    if value is None:
        return default_value

    cleaned = value.strip()
    if cleaned == "":
        return default_value if default_value is not None else ""

    # Remove aspas externas quando a query chega envelopada em "..." ou '...'
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in ('"', "'"):
        cleaned = cleaned[1:-1].strip()

    # Converte aspas escapadas para aspas duplas utilizaveis.
    cleaned = cleaned.replace('\\"', '"').replace("\\'", "'")

    return cleaned
