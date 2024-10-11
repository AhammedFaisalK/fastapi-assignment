from typing import Optional
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from app.models.clock_in import ClockIn, ClockInUpdate
from app.database import clockin_collection

router = APIRouter()

# Create Clock-In Record
@router.post("/")
def create_clock_in(clock_in: ClockIn):
    clock_in_data = clock_in.dict()
    clock_in_data["insert_datetime"] = datetime.utcnow()  # Add Insert DateTime automatically
    result = clockin_collection.insert_one(clock_in_data)
    return {"id": str(result.inserted_id)}

# Get Clock-In Record by ID
@router.get("/{id}")
def get_clock_in(id: str):
    clock_in = clockin_collection.find_one({"_id": ObjectId(id)})
    if clock_in is None:
        raise HTTPException(status_code=404, detail="Clock-In record not found")
    clock_in["id"] = str(clock_in["_id"])
    return clock_in

# Filter Clock-In Records
@router.get("/filter")
def filter_clock_in(email: Optional[str] = None, location: Optional[str] = None,
                    insert_datetime: Optional[str] = None):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        query["insert_datetime"] = {"$gt": datetime.strptime(insert_datetime, "%Y-%m-%d")}

    clock_ins = list(clockin_collection.find(query))
    for clock_in in clock_ins:
        clock_in["id"] = str(clock_in["_id"])
    return clock_ins

# Delete Clock-In Record
@router.delete("/{id}")
def delete_clock_in(id: str):
    result = clockin_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Clock-In record not found")
    return {"message": "Clock-In record deleted"}

# Update Clock-In Record by ID
@router.put("/{id}")
def update_clock_in(id: str, clock_in: ClockInUpdate):
    updated_data = {k: v for k, v in clock_in.dict().items() if v is not None}
    result = clockin_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Clock-In record not found")
    return {"message": "Clock-In record updated"}
