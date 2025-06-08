import yaml

def load_config(path: str) -> dict:
    """Завантажує YAML-конфіг, або повертає пустий dict, якщо немає файлу."""
    if not path:
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}