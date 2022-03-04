from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    ENVIRONMENT: str
    DOCKER_FOLDER: str
    DOCKER_COMPOSE_FILE_NAME: str
    FLASK_ENV: str
    FLASK_CONFIG: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    MONGODB_USER: str
    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_PASSWORD: str
    MONGODB_URI: str = None
    APPLICATION_DB: str
    FAKER_DATA_LOCATE: str
    API_V1_PREFIX: str
    APPLICATION_API_MIMETYPE: str
    ENCODING_FORMAT: str

    @validator("MONGODB_URI", pre=True)
    def assemble_db_connection(
        cls, value: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(value, str):
            return value

        mongodb_uri = (
            f"mongodb://"
            f"{values.get('MONGODB_USER')}:"
            f"{values.get('MONGODB_PASSWORD')}@"
            f"{values.get('MONGODB_HOST')}:"
            f"{values.get('MONGODB_PORT')}"
        )
        return mongodb_uri

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
