from pydantic import BaseModel, Field
from enum import Enum
from app.models.entity import Entity

class ActionType(str, Enum):
    WORK_996 = "WORK_996"
    WORK_965 = "WORK_965"
    REST_PARK = "REST_PARK"
    CONSUME_ENT = "CONSUME_ENT"
    SLEEP = "SLEEP"
    IDLE = "IDLE"

class AgentStats(BaseModel):
    health: float = Field(default=100.0, ge=0, le=100)
    sanity: float = Field(default=100.0, ge=0, le=100)
    wealth: float = Field(default=0.0)
    energy: float = Field(default=100.0, ge=0, le=100)

class Agent(Entity):
    type: str = "Agent"
    stats: AgentStats = Field(default_factory=AgentStats)
    current_action: ActionType = ActionType.IDLE
    is_active: bool = True
