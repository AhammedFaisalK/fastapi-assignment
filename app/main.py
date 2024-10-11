import os
from fastapi import FastAPI
from app.routes import item_routes, clock_in_routes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the secret key from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

# Include routes for Items and Clock-In Records
app.include_router(item_routes.router, prefix="/items", tags=["Items"])
app.include_router(clock_in_routes.router, prefix="/clock-in", tags=["Clock-In Records"])

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
