"""Configuration settings for the ETL pipeline"""

from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Add your configuration settings here
CONFIG = {
    "source_path": "",
    "destination_path": "",
    "log_path": str(BASE_DIR / "logs"),
}
