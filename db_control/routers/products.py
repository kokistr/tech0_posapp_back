from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_control.database import get_db
from db_control.models import ProductMaster

router = APIRouter(prefix="/api/product", tags=["products"])

@router.get("")
async def get_product(code: str, db: Session = Depends(get_db)):
    product = db.query(ProductMaster).filter(ProductMaster.code == code).first()
    if product is None:
        return {"error": "商品が見つかりません"}
    return {"prd_id": product.prd_id, "code": product.code, "name": product.name, "price": product.price}
