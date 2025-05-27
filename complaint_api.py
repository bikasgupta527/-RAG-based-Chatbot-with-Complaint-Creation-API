from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional,List
from uuid import uuid4

import mongomock
client = mongomock.MongoClient()

db = client["complaints_db"]
collection = db["complaints"]

app = FastAPI(title="Complaint API")

# MongoDB setup with mongomock
client = mongomock.MongoClient()
db = client["complaints_db"]
collection = db["complaints"]

# --- FastAPI Data Schemas ---
class Complaint(BaseModel):
    name: str
    phone_number: str
    email: str
    complaint_details: str

class ComplaintInDB(Complaint):
    complaint_id: str = Field(default_factory=lambda: str(uuid4()))

# --- FastAPI Endpoints ---
@app.post("/complaints", response_model=ComplaintInDB)
def create_complaint(complaint: Complaint):
    complaint_data = ComplaintInDB(**complaint.dict())
    collection.insert_one(complaint_data.dict())
    print(complaint_data)
    return complaint_data

@app.get("/complaints/search", response_model=List[ComplaintInDB])
def search_complaint(complaint_id: Optional[str] = Query(None), name: Optional[str] = Query(None)):
    if not complaint_id and not name:
        raise HTTPException(status_code=400, detail="Provide complaint_id or name")
    
    query = {}
    if complaint_id:
        query["complaint_id"] = complaint_id
    if name:
        query["name"] = name
    
    results = list(collection.find(query, {"_id": 0}))
    print(results)
    if not results:
        raise HTTPException(status_code=404, detail=f"Complaint not found for complaint_id={complaint_id}, name={name}")
    
    # Convert dictionaries to ComplaintInDB objects
    return [ComplaintInDB(**result) for result in results]
