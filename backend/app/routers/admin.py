from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.world import world

router = APIRouter()

class EventInjection(BaseModel):
    type: str
    description: str
    target_agents: Optional[List[str]] = None

class TickRequest(BaseModel):
    ticks: int = 1

@router.post("/inject-event")
def inject_event(event: EventInjection):
    """管理员接口，注入全局事件"""
    try:
        world.inject_event(event.type, event.description, event.target_agents)
        return {
            "message": f"Event '{event.type}' injected successfully.",
            "description": event.description,
            "affected_agents": event.target_agents or ["ALL"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/world/tick")
def advance_tick(request: TickRequest):
    """手动推进世界时间片"""
    world.run_agent_loop(request.ticks)
    
    current_time = world.time_system.get_current_time()
    return {
        "message": f"Advanced {request.ticks} tick(s).",
        "current_time": str(current_time),
        "is_night": world.time_system.is_night(),
        "active_agents": len(world.get_all_agents())
    }

@router.post("/agents/create")
def create_agent(agent_id: str = "new_agent", x: int = 0, y: int = 0):
    """创建一个新的 Agent"""
    try:
        agent = world.create_agent(agent_id=agent_id, x=x, y=y)
        return {
            "message": f"Agent {agent_id} created successfully.",
            "agent": {
                "id": agent.id,
                "x": agent.x,
                "y": agent.y
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/world/reset")
def reset_world():
    """重置世界状态"""
    world.map_system.entities.clear()
    
    from app.services.time_system import TimeSystem
    world.time_system = TimeSystem()
    
    return {"message": "World reset successfully."}