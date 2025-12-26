from fastapi import APIRouter
from app.services.world import world

router = APIRouter()

@router.get("/status")
def get_world_status():
    current_time = world.time_system.get_current_time()
    active_agents = len([a for a in world.map_system.entities.values() if a.is_active])
    
    return {
        "time": str(current_time),
        "weather": "Sunny", # Placeholder
        "active_agents": active_agents,
        "is_night": world.time_system.is_night()
    }
