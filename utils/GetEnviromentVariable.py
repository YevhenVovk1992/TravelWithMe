import os
import environ
from pathlib import Path

from environ import Env


def get_environment_variables() -> Env:
    BASE_DIR = Path(__file__).resolve().parent.parent
    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    return env
