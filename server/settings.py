from pydantic import BaseSettings


class Settings(BaseSettings):
    generator_interval_in_seconds: float = 0.5
