from pydantic import BaseSettings

class Settings(BaseSettings):
    AOAI_ENDPOINT: str
    AOAI_API_KEY: str
    AISEARCH_ENDPOINT: str
    AISEARCH_ADMIN_KEY: str
    BLOB_CONN_STRING: str
    SQL_CONNECTION_STRING: str

    class Config:
        env_file = ".env"

settings = Settings()
