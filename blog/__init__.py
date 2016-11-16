from pathlib import Path

from yaml import load

_blog_dir = Path(__file__).resolve().parent
_config_yml = _blog_dir.joinpath('_config.yml')

with open(str(_config_yml), encoding='utf-8') as f:
    config = load(f)

_theme_config = _blog_dir.joinpath('themes', config['theme'], '_config.yml')
with open(str(_theme_config), encoding='utf-8') as f:
    theme = load(f)
