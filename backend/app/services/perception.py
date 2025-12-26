from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.models.map import LocationInfo
from app.models.agent import AgentStats
from app.models.entity import Entity

class EnvironmentSnapshot(BaseModel):
    """Agent 感知到的环境快照"""
    agent_id: str
    location: LocationInfo
    nearby_entities: List[Entity]
    self_stats: AgentStats
    time_desc: str # e.g. "Morning, 08:00"
    weather: str = "Sunny"

class PerceptionFilter:
    def process(self, snapshot: EnvironmentSnapshot) -> str:
        """将环境快照转化为自然语言描述"""
        # 1. Time & Weather
        desc = [f"It is currently {snapshot.time_desc}. The weather is {snapshot.weather}."]
        
        # 2. Location
        loc = snapshot.location
        terrain_desc = f"You are standing at ({loc.x}, {loc.y}), which is {loc.terrain.value}."
        if loc.description:
            terrain_desc += f" ({loc.description})"
        desc.append(terrain_desc)
        
        # 3. Self Stats
        stats = snapshot.self_stats
        status_desc = f"You feel: Health={stats.health:.1f}, Energy={stats.energy:.1f}, Sanity={stats.sanity:.1f}. You have ${stats.wealth:.1f}."
        desc.append(status_desc)
        
        # 4. Nearby Entities
        if snapshot.nearby_entities:
            entity_descs = []
            for e in snapshot.nearby_entities:
                if e.id == snapshot.agent_id:
                    continue
                # Simple relative position
                rel_x = e.x - loc.x
                rel_y = e.y - loc.y
                # Simplification: just list them
                entity_descs.append(f"A {e.type} (ID: {e.id}) at ({e.x}, {e.y})")
            
            if entity_descs:
                desc.append("Nearby you see: " + ", ".join(entity_descs) + ".")
            else:
                desc.append("You don't see anyone else nearby.")
        else:
             desc.append("You don't see anyone else nearby.")

        return "\n".join(desc)
