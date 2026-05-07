import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class TestConfig:
    base_url: str = os.getenv("BASE_URL", "https://www.saucedemo.com/")
    valid_user: str = os.getenv("VALID_USER", "standard_user")
    valid_password: str = os.getenv("VALID_PASSWORD", "secret_sauce")
    invalid_user: str = os.getenv("INVALID_USER", "locked_out_user")
    invalid_password: str = os.getenv("INVALID_PASSWORD", "secret_sauce")


config = TestConfig()
