from mypy_extensions import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()


DBConfig = TypedDict('DBConfig',
                     {'db_host': str, 'db_port': int, 'db_user': str, 'db_pwd': str, 'db_name': str, })


DB_CONFIG: DBConfig = {
    'db_host': os.getenv("DB_HOST"),
    'db_port': os.getenv("DB_PORT"),
    'db_user': os.getenv("DB_USER"),
    'db_pwd': os.getenv("DB_PASSWORD"),
    'db_name': os.getenv("DATABASE")
}
