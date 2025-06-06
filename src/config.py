import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".ai_stem_splitter"
CONFIG_PATH = CONFIG_DIR / "config.json"

class Config:
    def __init__(self):
        self.data = {
            "model_dir": str(CONFIG_DIR / "models"),
            "output_dir": str(CONFIG_DIR / "output"),
        }
        self.load()

    def load(self):
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                try:
                    self.data.update(json.load(f))
                except Exception:
                    pass
        else:
            self.save()

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.data, f)

    @property
    def model_dir(self) -> str:
        return self.data["model_dir"]

    @model_dir.setter
    def model_dir(self, path: str) -> None:
        self.data["model_dir"] = path
        self.save()

    @property
    def output_dir(self) -> str:
        return self.data["output_dir"]

    @output_dir.setter
    def output_dir(self, path: str) -> None:
        self.data["output_dir"] = path
        self.save()
