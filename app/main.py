from fastapi import FastAPI
from app.routes import item_routes, clock_in_routes

app = FastAPI()

# Include routes for Items and Clock-In Records
app.include_router(item_routes.router, prefix="/items", tags=["Items"])
app.include_router(clock_in_routes.router, prefix="/clock-in", tags=["Clock-In Records"])
