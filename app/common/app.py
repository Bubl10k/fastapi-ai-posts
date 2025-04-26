from pydantic import field_validator
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
	SERVER_HOST: str
	PORT: int
	RELOAD: bool
	ALLOWED_ORIGINS: str

	@classmethod
	@field_validator("ALLOWED_ORIGINS", mode="before")
	def validate_allowed_origins(cls, value):
		return value.split(",")
