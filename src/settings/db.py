from mypy_extensions import TypedDict

from pathlib import Path
from starlette.config import Config

p: Path = Path(__file__).parents[2] / ".env"
config: Config = Config(p if p.exists() else None)

DATABASE: str = config("DATABASE", cast=str)
DB_USER: str = config("DB_USER", cast=str)
DB_PASSWORD: str = config("DB_PASSWORD", cast=str)
DB_HOST: str = config("DB_HOST", cast=str)
DB_PORT: int = config("DB_PORT", cast=int)


DBConfig = TypedDict('DBConfig',
                     {'host': str, 'port': int, 'user': str, 'password': str, 'database': str, })


DB_CONFIG: DBConfig = {
    'db_host': DB_HOST,
    'db_port': DB_PORT,
    'db_user': DB_USER,
    'db_pwd': DB_PASSWORD,
    'db_name': DATABASE
}
