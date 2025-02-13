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

# CORS設定（フロントエンドのアクセス許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tech0-gen8-step4-pos-app-3.azurewebsites.net",
        "https://tech0-gen-8-step4-db-1.mysql.database.azure.com"
        "http://localhost:3000"  # ローカル開発確認用
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベース初期化（テーブル作成）
models.Base.metadata.create_all(bind=database.engine)

# ルーターを追加（各機能のエンドポイントを管理）
## ユーザー管理（ユーザーの登録・取得）
app.include_router(users.router)

##　商品管理（商品の取得・検索）
app.include_router(products.router)

## 　取引管理（購入処理・トランザクション管理）
app.include_router(transactions.router)

@app.get("/")
def root():
    """ サーバーの動作確認エンドポイント """
    return {"message": "Welcome to FastAPI with Azure DB!"}

## ユーザー管理API
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """ ユーザーを新規登録するエンドポイント """
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    """ ユーザーIDからユーザー情報を取得するエンドポイント """
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
