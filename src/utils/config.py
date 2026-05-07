import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
DEFAULT_BASE_URL = Path(__file__).resolve().parents[2].joinpath("sample_site", "index.html").as_uri()


@dataclass(frozen=True)
class TestConfig:
    base_url: str = os.getenv("BASE_URL", DEFAULT_BASE_URL)
    valid_user: str = os.getenv("VALID_USER", "standard_user")
    valid_password: str = os.getenv("VALID_PASSWORD", "secret_sauce")
    locked_user: str = os.getenv("LOCKED_USER", "locked_out_user")
    locked_password: str = os.getenv("LOCKED_PASSWORD", "secret_sauce")


config = TestConfig()
