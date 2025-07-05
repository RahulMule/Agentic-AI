from pydantic_settings import BaseSettings
from pydantic import Field
class Settings(BaseSettings):
    groq_api_key : str
    grok_model_name: str

    class Config:
        env_file = ".env"
        extra = "ignore"
    
settings = Settings()