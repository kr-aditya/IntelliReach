import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    app_name: str = "IntelliReach"
    app_version: str = "1.0.0"

    groq_api_key: str = os.getenv(
        "GROQ_API_KEY",
        "",
    )

    serper_api_key: str = os.getenv(
        "SERPER_API_KEY",
        "",
    )


settings = Settings()