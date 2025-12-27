from fastapi import FastAPI
from app.core.config import settings
from app.routers import world, agents, admin

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(world.router, prefix=f"{settings.API_V1_STR}/world", tags=["world"])
app.include_router(agents.router, prefix=f"{settings.API_V1_STR}/agents", tags=["agents"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
