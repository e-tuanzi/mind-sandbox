from typing import Dict
from app.models.agent import Agent, ActionType
from app.services.map_system import MapSystem

class StateDynamics:
    def __init__(self, map_system: MapSystem):
        self.map_system = map_system
        
        # 定义动作对数值的影响 (每 Tick 或 单次结算)
        # 这里简化为单次结算或每小时结算的数值，具体取决于调用频率。
        # 假设 apply_action_effect 是在 Action 完成或 Tick 时调用。
        # 如果是持续性动作，应该由 Tick 驱动。
        # 文档 ENV-002: WORK_996 持续4小时 -> Energy < 20.
        # 假设 1 Tick = 1 Min. 4 Hours = 240 Ticks.
        # 如果是每次 Tick 调用，数值应该很小。
        # 如果是事件结算，数值大。
        # 文档 imply "Action.WORK_996 (Duration 4h)".
        # Let's assume apply_action_effect is called per Tick for continuous actions,
        # or once for instant actions.
        # For simplicity in this phase, let's assume it's called PER TICK for continuous states.
        
        self.effects = {
            ActionType.WORK_996: {"health": -0.05, "sanity": -0.05, "wealth": 0.5, "energy": -0.4},
            ActionType.WORK_965: {"health": -0.01, "sanity": -0.01, "wealth": 0.2, "energy": -0.1},
            ActionType.REST_PARK: {"health": 0.02, "sanity": 0.1, "wealth": 0.0, "energy": 0.1},
            ActionType.CONSUME_ENT: {"health": 0.0, "sanity": 0.5, "wealth": -1.0, "energy": -0.05},
            ActionType.SLEEP: {"health": 0.05, "sanity": 0.05, "wealth": 0.0, "energy": 0.5},
            ActionType.IDLE: {"health": 0.0, "sanity": 0.0, "wealth": 0.0, "energy": -0.01}
        }

    def apply_action_effect(self, agent_id: str, action_type: ActionType):
        """根据动作类型结算数值变化 (Per Tick)"""
        agent = self.map_system.entities.get(agent_id)
        if not agent or not isinstance(agent, Agent):
            return # Agent not found

        if not agent.is_active:
            return # Dead or inactive

        effect = self.effects.get(action_type, {})
        
        stats = agent.stats
        
        # Apply deltas
        stats.health += effect.get("health", 0)
        stats.sanity += effect.get("sanity", 0)
        stats.wealth += effect.get("wealth", 0)
        stats.energy += effect.get("energy", 0)
        
        # Clamp values
        stats.health = max(0.0, min(100.0, stats.health))
        stats.sanity = max(0.0, min(100.0, stats.sanity))
        stats.energy = max(0.0, min(100.0, stats.energy))
        # Wealth has no upper bound, but min 0? Docs say "Bankruptcy". Let's allow negative or clamp 0.
        # ENV-004 implies transactions fail if wealth < price.
        # So wealth acts as a resource.
        
        # Check Critical States
        if stats.health <= 0:
            agent.is_active = False
            # Trigger Death Event (TODO)
            
        if stats.energy <= 0:
            # Trigger Fainting (Force Sleep) (TODO)
            pass
