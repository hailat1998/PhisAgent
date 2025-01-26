from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Test API",
    description="A simple API for testing FastAPI functionality",
    version="1.0.0"
)

# Pydantic model for request body
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Store items in memory (for demo purposes)
items = {}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Test API"}

# GET all items
@app.get("/items")
async def get_items():
    return items

# GET item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# POST new item
@app.post("/items")
async def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"item_id": item_id, "item": item}

# GET items with query parameter
@app.get("/search")
async def search_items(name: Optional[str] = None, min_price: Optional[float] = None):
    if name is None and min_price is None:
        return items
    
    filtered_items = {}
    for item_id, item in items.items():
        if name and name.lower() not in item.name.lower():
            continue
        if min_price and item.price < min_price:
            continue
        filtered_items[item_id] = item
    
    return filtered_items

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}