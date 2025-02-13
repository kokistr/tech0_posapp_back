from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db_control import models, schemas, crud, database
from db_control.routers import users, products, transactions
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# FastAPI インスタンス作成
app = FastAPI()

# 環境変数の確認
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", "******")  # ログ出力時にパスワードをマスク
DB_PORT = os.getenv("DB_PORT", "3306")

# 設定確認用ログ出力
print("🔍 [環境変数チェック]")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")  # マスク済み
print(f"DB_PORT: {DB_PORT}")

# CORS設定
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not allowed_origins or allowed_origins == [""]:
    allowed_origins = ["https://tech0-gen8-step4-pos-app-3.azurewebsites.net"]

print(f"🌍 [CORS設定] ALLOWED_ORIGINS: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# アプリ起動時の処理
@app.on_event("startup")
async def startup_event():
    print("🚀 [アプリ起動] データベースの接続確認を実行中...")
    try:
        models.Base.metadata.create_all(bind=database.engine)
        print("✅ [データベース] 初期化完了")
    except Exception as e:
        print(f"❌ [データベースエラー] {e}")

# ルーターを追加
app.include_router(users.router)
app.include_router(products.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI with Azure DB!"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
