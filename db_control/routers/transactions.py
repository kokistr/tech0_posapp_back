from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db_control.database import get_db
from db_control import models, schemas

router = APIRouter(prefix="/api/transaction", tags=["transaction"])

@router.post("")
async def save_transaction(transaction: schemas.TransactionRequest, db: Session = Depends(get_db)):
    new_transaction = models.Transaction(
        emp_cd=transaction.emp_cd,
        store_cd=transaction.store_cd,
        pos_no=transaction.pos_no,
        total_amt=transaction.total_amt
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return {"trd_id": new_transaction.trd_id}

@router.post("/details")
async def save_transaction_details(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    details = data["details"]

    try:
        for detail in details:
            new_detail = models.TransactionDetail(
                trd_id=detail["trd_id"],
                prd_id=detail["prd_id"],
                prd_code=detail["prd_code"],
                prd_name=detail["prd_name"],
                prd_price=detail["prd_price"]
            )
            db.add(new_detail)

        db.commit()
        db.refresh(new_detail)

        return {"message": "Transaction details saved successfully!"}
    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")
        return {"error": "Failed to save transaction details"}, 500
