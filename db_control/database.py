from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os
import urllib.parse  # ← 追加（パスワードエンコード用）
from dotenv import load_dotenv

# .env をロード（ローカル環境用、Azure ではシステム環境変数を使用）
load_dotenv()

# 環境変数を取得
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")  # デフォルトで 3306 を設定
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SSL_CERT = os.getenv("DB_SSL_CERT", "db_control/certs/DigiCertGlobalRootCA.crt.pem")

# デバッグ用に出力
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {'*' * len(DB_PASSWORD) if DB_PASSWORD else 'None'}")

# パスワードをURLエンコード（@ や特殊文字を正しく処理するため）
if DB_PASSWORD:
    DB_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD)

# 必須変数のチェック（None ならエラーを出す）
if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("環境変数が正しく設定されていません。Azure ポータルで環境変数を確認してください。")

# データベース URL を作成
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンを作成
engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl_ca": DB_SSL_CERT} 
)

# データベースが存在しなければ作成
if not database_exists(engine.url):
    create_database(engine.url)

# ORM の設定
Base = declarative_base()
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
