import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "YoloFund API"

    ENVIRONMENT: str = "PRODUCTION"
    API_V1_STR: str = "/api/v1"
    PORT: int = 8000
    LOGLEVEL: str = "warning"

    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str

    FINNHUB_API_KEY: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgres",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=f'{values.get("POSTGRES_PORT")}',
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()