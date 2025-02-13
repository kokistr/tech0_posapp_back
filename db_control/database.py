from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import urllib.parse  # パスワードエンコード用
from dotenv import load_dotenv

# .env をロード（ローカル環境用、Azureでは環境変数を使用）
load_dotenv()

# 環境変数を取得
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")  # デフォルト値 3306
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", "").strip('"')  # 余計な `"` を削除
DB_SSL_CERT = os.getenv("DB_SSL_CERT", "db_control/certs/DigiCertGlobalRootCA.crt.pem")

# パスワードのURLエンコード（特殊文字の処理）
if DB_PASSWORD:
    DB_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD)

# 必須環境変数のチェック
if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("❌ [環境変数エラー] 必須のデータベース接続情報が設定されていません。Azureポータルの環境変数を確認してください。")

# データベース URL を作成
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# デバッグ用の出力（パスワードはマスク）
print("🔍 [環境変数チェック]")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {'*' * len(DB_PASSWORD)}")  # マスク済み
print(f"DB_PORT: {DB_PORT}")

# SQLAlchemy エンジンの作成
try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"ssl_ca": DB_SSL_CERT},  # SSL接続
        pool_pre_ping=True  # DB切断検知
    )
    print("✅ [データベース] 接続成功！")
except Exception as e:
    print(f"❌ [データベースエラー] 接続に失敗しました: {e}")
    raise

# ORM の設定
Base = declarative_base()

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースセッションの取得関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
