from pathlib import Path
from dotenv import load_dotenv
import os

# Carga el .env desde la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(env_path)

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
MODEL_ID = os.getenv("MODEL_ID")
LOCAL_DIR = os.getenv("LOCAL_DIR")
PORT = int(os.getenv("PORT", 8000))

#import configuration of any module
#from app.config import BUCKET_NAME, MODEL_ID


