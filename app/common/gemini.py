from pydantic_settings import BaseSettings


class Gemini(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str
