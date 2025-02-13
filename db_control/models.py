# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Baseクラスを作成
Base = declarative_base()

# Baseクラスを継承したモデルを作成
# usersテーブルのモデルUsers
class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    mail = Column(String(50),nullable=False,unique=True)
    sex = Column(String(3),nullable=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())

# 商品マスタ
class ProductMaster(Base):
    __tablename__ = 'product_master'
    prd_id = Column(Integer, primary_key=True)
    code = Column(CHAR(13), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

# 取引
class Transaction(Base):
    __tablename__ = 'transaction'
    trd_id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, server_default=func.current_timestamp())
    emp_cd = Column(CHAR(10), nullable=False)
    store_cd = Column(CHAR(5), nullable=False)
    pos_no = Column(CHAR(3), nullable=False)
    total_amt = Column(Integer, nullable=False)

    # 取引詳細とのリレーション
    details = relationship("TransactionDetail", back_populates="transaction")

# 取引詳細
class TransactionDetail(Base):
    __tablename__ = 'transaction_detail'
    trd_id = Column(Integer, ForeignKey('transaction.trd_id'), primary_key=True)
    dtl_id = Column(Integer, primary_key=True, autoincrement=True)
    prd_id = Column(Integer, ForeignKey('product_master.prd_id'), nullable=False)
    prd_code = Column(CHAR(13), nullable=False)
    prd_name = Column(String(50), nullable=False)
    prd_price = Column(Integer, nullable=False)

    transaction = relationship("Transaction", back_populates="details")
    product = relationship("ProductMaster")
