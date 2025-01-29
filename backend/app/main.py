from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Database setup
DB_CONN = os.getenv("DB_CONN")
conn = psycopg2.connect(DB_CONN)

# Models
class PANRequest(BaseModel):
    pan_number: str

class BankRequest(BaseModel):
    account_number: str
    ifsc_code: str

@app.post("/verify-pan")
async def verify_pan(request: PANRequest):
    try:
        response = requests.post(
            "https://api.setu.co/pan/verify",
            json={"pan": request.pan_number},
            headers={"Authorization": f"Bearer {os.getenv('SETU_API_KEY')}"}
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
            "https://api.setu.co/rpd/verify",
            json={"account_number": request.account_number, "ifsc_code": request.ifsc_code},
            headers={"Authorization": f"Bearer {os.getenv('SETU_API_KEY')}"}
        )
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        else:
            raise HTTPException(status_code=400, detail=response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
def get_analytics():
    # Query database to calculate analytics
    return {"data": "Analytics will go here"}

@app.get("/users")
def get_users():
    # Query database to fetch user KYC data
    return {"data": "Users list will go here"}
