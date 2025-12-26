from pydantic import BaseModel
from typing import Tuple

class Entity(BaseModel):
    id: str
    x: int
    y: int
    type: str # 'Agent', 'NPC', 'Object'
    
    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)
