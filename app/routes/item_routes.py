from typing import Optional
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.item import Item, ItemUpdate
from app.database import items_collection
from datetime import datetime

router = APIRouter()

# Create Item
@router.post("/")
def create_item(item: Item):
    item_data = item.dict()
    item_data["insert_date"] = datetime.utcnow()  
    result = items_collection.insert_one(item_data)
    return {"id": str(result.inserted_id)}

# Get Item by ID
@router.get("/{id}")
def get_item(id: str):
    item = items_collection.find_one({"_id": ObjectId(id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item["id"] = str(item["_id"])
    return item

# Filter Items
@router.get("/filter")
def filter_items(email: Optional[str] = None, expiry_date: Optional[str] = None,
                 insert_date: Optional[str] = None, quantity: Optional[int] = None):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt": expiry_date}
    if insert_date:
        query["insert_date"] = {"$gt": datetime.strptime(insert_date, "%Y-%m-%d")}
    if quantity:
        query["quantity"] = {"$gte": quantity}

    items = list(items_collection.find(query))
    for item in items:
        item["id"] = str(item["_id"])
    return items

# Aggregate Items by Email
@router.get("/aggregate")
def aggregate_items_by_email():
    pipeline = [
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]
    result = list(items_collection.aggregate(pipeline))
    return result

# Delete Item
@router.delete("/{id}")
def delete_item(id: str):
    result = items_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}

# Update Item by ID
@router.put("/{id}")
def update_item(id: str, item: ItemUpdate):
    updated_data = {k: v for k, v in item.dict().items() if v is not None}
    result = items_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated"}
