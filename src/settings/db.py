from mypy_extensions import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE: str = os.getenv("DATABASE")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: str = os.getenv("DB_PORT")


DBConfig = TypedDict('DBConfig',
                     {'db_host': str, 'db_port': int, 'db_user': str, 'db_pwd': str, 'db_name': str, })


DB_CONFIG: DBConfig = {
    'db_host': DB_HOST,
    'db_port': DB_PORT,
    'db_user': DB_USER,
    'db_pwd': DB_PASSWORD,
    'db_name': DATABASE
}
