import json
from pathlib import Path

# Store configuration and models inside the project directory so that
# everything lives under the repository root.  This makes the application
# portable and avoids writing files to the user's home directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"

class Config:
    def __init__(self):
        self.data = {
            "model_dir": str(PROJECT_ROOT / "models"),
            "output_dir": str(PROJECT_ROOT / "output"),
        }
        self.load()
        # Ensure default directories exist
        Path(self.data["model_dir"]).mkdir(parents=True, exist_ok=True)
        Path(self.data["output_dir"]).mkdir(parents=True, exist_ok=True)

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
        PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.data, f)

    @property
    def model_dir(self) -> str:
        return self.data["model_dir"]

    @model_dir.setter
    def model_dir(self, path: str) -> None:
        self.data["model_dir"] = path
        Path(path).mkdir(parents=True, exist_ok=True)
        self.save()

    @property
    def output_dir(self) -> str:
        return self.data["output_dir"]

    @output_dir.setter
    def output_dir(self, path: str) -> None:
        self.data["output_dir"] = path
        Path(path).mkdir(parents=True, exist_ok=True)
        self.save()
