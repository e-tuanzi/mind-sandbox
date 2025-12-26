from typing import Tuple, List, Dict
from app.models.map import LocationInfo, TerrainType
from app.models.entity import Entity
from app.core.config import settings
import math

class MapSystem:
    def __init__(self):
        self.width = settings.MAP_WIDTH
        self.height = settings.MAP_HEIGHT
        self.grid: Dict[Tuple[int, int], LocationInfo] = {}
        self.entities: Dict[str, Entity] = {}
        
        # Initialize default empty map
        self._init_map()

    def _init_map(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[(x, y)] = LocationInfo(
                    x=x, y=y, 
                    terrain=TerrainType.EMPTY, 
                    is_walkable=True
                )

    def set_terrain(self, x: int, y: int, terrain: TerrainType, is_walkable: bool):
        if (x, y) in self.grid:
            self.grid[(x, y)].terrain = terrain
            self.grid[(x, y)].is_walkable = is_walkable

    def register_entity(self, entity: Entity):
        self.entities[entity.id] = entity

    def get_location(self, coord: Tuple[int, int]) -> LocationInfo:
        return self.grid.get(coord, LocationInfo(x=coord[0], y=coord[1], terrain=TerrainType.WALL, is_walkable=False))

    def move_entity(self, entity_id: str, target: Tuple[int, int]) -> bool:
        """尝试移动实体，返回成功/失败"""
        if entity_id not in self.entities:
            return False
            
        # Check bounds
        if not (0 <= target[0] < self.width and 0 <= target[1] < self.height):
            return False
            
        # Check terrain walkability
        location = self.get_location(target)
        if not location.is_walkable:
            return False
            
        # Check collision with other entities (optional, for now simple 2D overlap might be allowed or not)
        # Let's assume for now collision is only with terrain
        
        entity = self.entities[entity_id]
        # Basic distance check (can only move 1 tile at a time?)
        # Docs don't specify speed, but usually move is adjacent.
        # Let's assume teleport/pathfinding is handled by caller or it's a direct move request.
        # For simulation, let's enforce adjacency (1 step) or just allow it if it's a valid target.
        # Given "Agent attempts to move to (1,1)", let's assume it's a direct neighbor step.
        dx = abs(entity.x - target[0])
        dy = abs(entity.y - target[1])
        if dx > 1 or dy > 1:
             # Assuming movement is only to neighbors
             return False

        entity.x = target[0]
        entity.y = target[1]
        return True

    def get_nearby_entities(self, center: Tuple[int, int], radius: int) -> List[Entity]:
        result = []
        for entity in self.entities.values():
            dist = math.sqrt((entity.x - center[0])**2 + (entity.y - center[1])**2)
            if dist <= radius:
                result.append(entity)
        return result
