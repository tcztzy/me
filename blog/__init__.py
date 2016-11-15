import json
from pathlib import Path

settings_path = str(Path(__file__).resolve().parent.joinpath('settings.json'))
with open(settings_path, encoding='utf-8') as stream:
    settings = json.load(stream)
