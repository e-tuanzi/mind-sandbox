from pydantic import BaseModel, Field, PrivateAttr
from enum import Enum
from typing import Optional, Any
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
    
    # Runtime components (not serialized directly usually, but for simplicity here)
    # We use PrivateAttr so Pydantic ignores them for JSON serialization by default
    _memory: Any = PrivateAttr(default=None)
    _brain: Any = PrivateAttr(default=None)
    _perception: Any = PrivateAttr(default=None)

    def bind_soul(self, memory, brain, perception):
        self._memory = memory
        self._brain = brain
        self._perception = perception
