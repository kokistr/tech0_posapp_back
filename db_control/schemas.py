from pydantic import BaseModel

class UserBase(BaseModel):
    name : str
    mail : str
    sex : str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class Product(BaseModel):
    prd_id: int
    code: str
    name: str
    price: int

class EchoMessage(BaseModel):
    message: str | None = None

class TransactionRequest(BaseModel):
    total_amt: float
    emp_cd: int
    store_cd: int
    pos_no: int