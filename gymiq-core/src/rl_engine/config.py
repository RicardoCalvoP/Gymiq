from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
DUMMY_FILE = BASE_DIR / "exerciseData.json"
