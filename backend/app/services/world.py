from app.services.time_system import TimeSystem
from app.services.map_system import MapSystem
from app.services.state_dynamics import StateDynamics

class WorldEngine:
    def __init__(self):
        self.time_system = TimeSystem()
        self.map_system = MapSystem()
        self.state_dynamics = StateDynamics(self.map_system)
        
    def tick(self):
        # 1. Time Advance
        self.time_system.tick()
        
        # 2. Update Agents (State Dynamics)
        # For Phase 1, we just simulate effect application if they were doing something.
        # In full version, this would iterate all agents and apply their current action's effect.
        for agent_id, agent in self.map_system.entities.items():
            if agent.is_active:
                self.state_dynamics.apply_action_effect(agent_id, agent.current_action)

# Singleton Instance
world = WorldEngine()
