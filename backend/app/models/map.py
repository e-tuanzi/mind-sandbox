from enum import Enum
from pydantic import BaseModel
from typing import Tuple, Optional

class TerrainType(str, Enum):
    EMPTY = "Empty"
    WALL = "Wall"
    ROAD = "Road"
    BUILDING = "Building"

class LocationInfo(BaseModel):
    x: int
    y: int
    terrain: TerrainType
    description: Optional[str] = None
    is_walkable: bool = True
