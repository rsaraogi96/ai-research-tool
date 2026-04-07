from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./data/research.db"
    semantic_scholar_api_key: str = ""
    github_token: str = ""
    huggingface_token: str = ""
    collector_enabled: bool = True
    arxiv_interval_hours: int = 6
    semantic_scholar_interval_hours: int = 6
    rss_interval_hours: int = 4

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
