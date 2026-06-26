from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class BotConfig(BaseSettings):
    """Bot config"""

    # чтение .env
    # потом менять на нужные данные в .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    MAX_BOT_TOKEN : str
    MAX_WEBHOOK_URL: Optional[str] = None

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "bot_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str

    @property
    def database_url(self) -> str:
        """Получение строки для подключения SQLAlchemy"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    SECRET_KEY: str
    ADMIN_IDS: List[int] = []

    YANDEX_MAPS_API_KEY: Optional[str] = None
    GIGACHAT_CLIENT_ID: Optional[str] = None
    GIGACHAT_CLIENT_SECRET: Optional[str] = None

    QUIZ_CORRECT_POINTS: int = 10
    CHALLENGE_SUCCESS_POINTS: int = 50
    NEWSLETTER_TIME: str = "09:00"


#тест модуля
settings = BotConfig()

if __name__ == "__main__":
    print("BotConfig | Load BotConfig")
    print(f"MAX_BOT_TOKEN: {settings.MAX_BOT_TOKEN}")
    print(f"️DB: {settings.DB_NAME} on {settings.DB_HOST}")
    print(f"Admin list: {settings.ADMIN_IDS}")