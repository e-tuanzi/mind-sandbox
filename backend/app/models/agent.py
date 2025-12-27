from pydantic import BaseModel, Field, PrivateAttr
from enum import Enum
from typing import Optional, Any, Tuple
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
    values: str = Field(default="生存第一，健康最重要。")
    daily_log: str = Field(default="")
    is_sleeping: bool = Field(default=False)
    
    # Runtime components (not serialized directly usually, but for simplicity here)
    # We use PrivateAttr so Pydantic ignores them for JSON serialization by default
    _memory: Any = PrivateAttr(default=None)
    _brain: Any = PrivateAttr(default=None)
    _perception: Any = PrivateAttr(default=None)
    _map_system: Any = PrivateAttr(default=None)

    def bind_soul(self, memory, brain, perception, map_system):
        self._memory = memory
        self._brain = brain
        self._perception = perception
        self._map_system = map_system

    def decide_and_act(self, language: str = None) -> Optional[ActionType]:
        """
        完整决策循环：感知 -> 检索 -> 思考 -> 行动 -> 记录
        
        Args:
            language: 语言代码（"en" 或 "zh"）
        
        Returns: 执行的动作类型
        """
        if not self.is_active or self.is_sleeping:
            return None
        
        if not all([self._memory, self._brain, self._perception, self._map_system]):
            return None
        
        # 1. 感知 - 生成环境快照
        location = self._map_system.get_location((self.x, self.y))
        nearby_entities = self._map_system.get_nearby_entities((self.x, self.y), radius=3)
        
        snapshot = self._perception.snapshot_cls(
            agent_id=self.id,
            location=location,
            nearby_entities=nearby_entities,
            self_stats=self.stats,
            time_desc=self._perception._get_time_desc(),
            weather="Sunny"
        )
        
        # 2. 感知过滤器 - 转化为自然语言
        perception_text = self._perception.process(snapshot)
        
        # 3. 检索 - 从记忆库获取相关经验
        memory_context = self._memory.get_recent_context()
        
        # 4. 思考 - 调用决策引擎
        stats_dict = {
            "health": self.stats.health,
            "sanity": self.stats.sanity,
            "wealth": self.stats.wealth,
            "energy": self.stats.energy
        }
        
        decision = self._brain.decide_next_action(perception_text, memory_context, stats_dict, language)
        
        # 5. 行动 - 执行决策
        self.current_action = decision.action
        action_result = self._execute_action(decision)
        
        # 6. 记录 - 存入短期记忆
        self._memory.add_short_term(f"Thought: {decision.thought}")
        self._memory.add_short_term(f"Action: {decision.action}")
        
        # 记录到每日日志
        self.daily_log += f"[{self._perception._get_time_desc()}] {decision.thought}\n"
        
        return decision.action

    def _execute_action(self, decision) -> bool:
        """
        将决策转换为物理指令并执行
        Returns: 是否执行成功
        """
        action = decision.action
        target = decision.target or {}
        
        # 移动类动作
        if hasattr(target, 'get') and 'x' in target and 'y' in target:
            success = self._map_system.move_entity(self.id, (target['x'], target['y']))
            if not success:
                self._memory.add_short_term(f"Failed to move to ({target['x']}, {target['y']})")
            return success
        
        # 睡眠动作
        if action == ActionType.SLEEP:
            self.is_sleeping = True
            return True
        
        # 其他动作在 StateDynamics 中通过 tick 结算
        return True

    def wake_up(self):
        """唤醒 Agent"""
        self.is_sleeping = False
        self._memory.add_short_term("I woke up.")
