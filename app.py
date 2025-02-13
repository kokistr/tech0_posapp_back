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

allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tech0-gen8-step4-pos-app-3.azurewebsites.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB初期化
models.Base.metadata.create_all(bind=database.engine)

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
