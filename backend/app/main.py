from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests
import os
from .database import SessionLocal, engine, Base
from .models import UserKYC

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Database setup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
class PANRequest(BaseModel):
    pan_number: str

class BankRequest(BaseModel):
    account_number: str
    ifsc_code: str

@app.post("/verify-pan")
async def verify_pan(request: PANRequest):
    try:
        response = requests.post(
            f"{os.getenv('SETU_BASE_URL')}/pan/verify",  
    json={"pan": request.pan_number},
    headers={"Authorization": f"Bearer {os.getenv('SETU_PAN_API_KEY')}"}
        )
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        else:
            raise HTTPException(status_code=400, detail=response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify-bank")
async def verify_bank(request: BankRequest):
    try:
        response = requests.post(
            f"{os.getenv('SETU_BASE_URL')}/rpd/verify",
            json={"account_number": request.account_number, "ifsc_code": request.ifsc_code},
            headers={"Authorization": f"Bearer {os.getenv('SETU_PAN_API_KEY')}"}
        )
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        else:
            raise HTTPException(status_code=400, detail=response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_users(db: Session = Depends(get_db)):
    users = db.query(UserKYC).all()
    return {"data": [user.__dict__ for user in users]}

# Fetch Analytics
@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    total_kyc = db.query(UserKYC).count()
    total_success = db.query(UserKYC).filter(UserKYC.pan_verified == True, UserKYC.bank_verified == True).count()
    total_failed = total_kyc - total_success
    failed_pan = db.query(UserKYC).filter(UserKYC.pan_verified == False).count()
    failed_bank = db.query(UserKYC).filter(UserKYC.bank_verified == False).count()
    failed_both = db.query(UserKYC).filter(UserKYC.pan_verified == False, UserKYC.bank_verified == False).count()
    return {
        "total_kyc_attempted": total_kyc,
        "total_kyc_successful": total_success,
        "total_kyc_failed": total_failed,
        "total_kyc_failed_due_to_pan": failed_pan,
        "total_kyc_failed_due_to_bank": failed_bank,
        "total_kyc_failed_due_to_both": failed_both
    }

# Admin API to Delete a UserKYC Entry
@app.delete("/admin/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserKYC).filter(UserKYC.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status": "success", "message": "User deleted successfully"}

# Admin API to Update User Verification Status
@app.put("/admin/update-user/{user_id}")
def update_user(user_id: int, pan_verified: bool, bank_verified: bool, db: Session = Depends(get_db)):
    user = db.query(UserKYC).filter(UserKYC.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.pan_verified = pan_verified
    user.bank_verified = bank_verified
    db.commit()
    return {"status": "success", "message": "User verification status updated"}