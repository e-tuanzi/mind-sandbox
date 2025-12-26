from fastapi import FastAPI
from app.core.config import settings
from app.routers import world

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(world.router, prefix=f"{settings.API_V1_STR}/world", tags=["world"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
