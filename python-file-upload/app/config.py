import yaml
from pathlib import Path
from dataclasses import dataclass

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yml"

@dataclass
class StorageConfig:
    base_path: Path
    key_info: str

@dataclass
class AppConfig:
    host: str
    port: int
    storage: StorageConfig

def load_config() -> AppConfig:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    storage_cfg = data.get("storage", {})
    server_cfg = data.get("server", {})

    storage = StorageConfig(
        base_path=Path(storage_cfg.get("base_path", "./uploads")).resolve(),
        key_info=storage_cfg.get("key_info", "missing-key"),
    )

    return AppConfig(
        host=server_cfg.get("host", "0.0.0.0"),
        port=int(server_cfg.get("port", 8000)),
        storage=storage,
    )

config = load_config()
