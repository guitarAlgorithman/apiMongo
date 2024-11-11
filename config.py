import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")

settings = Settings()
