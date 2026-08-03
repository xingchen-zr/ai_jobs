#连接数据库
import os
import sqlalchemy
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(encoding="utf-8-sig")

mysql_host = os.getenv("MYSQL_HOST", "localhost")
mysql_port = int(os.getenv("MYSQL_PORT", "3306"))
mysql_user = os.getenv("MYSQL_USER", "root")
mysql_password = os.getenv("MYSQL_PASSWORD") or os.getenv("MYSQL_Password")
mysql_database = os.getenv("MYSQL_DATABASE", "chenxing")

if not mysql_password:
    raise RuntimeError("请先在 .env 文件中配置 MYSQL_PASSWORD")

database_url = URL.create(
    drivername="mysql+pymysql",
    username=mysql_user,
    password=mysql_password,
    host=mysql_host,
    port=mysql_port,
    database=mysql_database,
)

engine = sqlalchemy.create_engine(database_url, pool_pre_ping=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()