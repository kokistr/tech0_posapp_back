from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db_control import models, schemas, crud, database
from db_control.routers import users, products, transactions
import os
from dotenv import load_dotenv

load_dotenv()

# FastAPI インスタンス作成
app = FastAPI()

# 追加 20250213
@app.on_event("startup")
def startup_event():
    print("DB Initialization...")
    models.Base.metadata.create_all(bind=database.engine)

# CORS設定（フロントエンドのアクセス許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tech0-gen8-step4-pos-app-3.azurewebsites.net",
        "https://tech0-gen-8-step4-db-1.mysql.database.azure.com",
        "http://localhost:3000"  # ローカル開発確認用
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベースのチェックと初期化
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise RuntimeError("DATABASE_URL is not set. Please configure environment variables.")

@app.on_event("startup")
def startup_event():
    print("DB Initialization...")
    models.Base.metadata.create_all(bind=database.engine)

# ルーター追加
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

# サーバーの起動
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
