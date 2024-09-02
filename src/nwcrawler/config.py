import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    NW_URL: str = Field(default="https://blog.neoway.com.br", env="NW_URL") 
    ENV: str = Field(default="dev", env="ENV")
    LOGURU_LEVEL: str = Field(default="INFO", env="LOGURU_LEVEL")


load_dotenv()
config = Config()
