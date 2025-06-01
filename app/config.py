from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"

    SECRET_KEY: str
    OPENROUTER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()