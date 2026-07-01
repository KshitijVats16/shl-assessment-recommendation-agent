from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SHL Assessment Agent"

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    LLM_PROVIDER: str = "groq"
    LLM_MODEL: str = "llama-3.3-70b-versatile"

    API_KEY: str = ""
    BASE_URL: str = ""

    TOP_K: int = 20

    class Config:
        env_file = ".env"


settings = Settings()