import json

def get_format_ids():
    DECKLISTS_FILE = "data/formats.json"
    formats = []
    format_ids = []

    with open(DECKLISTS_FILE, 'r', encoding="utf-8") as f:
        formats = json.load(f)["data"]

    for f in formats:
        format_ids.append(f["id"])

    return format_ids

def get_formats():
    DECKLISTS_FILE = "data/formats.json"
    formats = []

    with open(DECKLISTS_FILE, 'r', encoding="utf-8") as f:
        formats = json.load(f)["data"]

    return formats