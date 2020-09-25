from typing_extensions import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()


DBConfig = TypedDict('DBConfig',
                     {'db_host': str, 'db_port': str, 'db_user': str, 'db_pwd': str, 'db_name': str, })


DB_CONFIG: DBConfig = {
    'db_host': os.getenv("DB_HOST", 'localhost'),
    'db_port': os.getenv("DB_PORT", '3306'),
    'db_user': os.getenv("MYSQL_USER", 'root'),
    'db_pwd': os.getenv("MYSQL_PASSWORD", 'root_password'),
    'db_name': os.getenv("MYSQL_DATABASE", 'test_db')
}
