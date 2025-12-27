from app.services.time_system import TimeSystem
from app.services.map_system import MapSystem
from app.services.state_dynamics import StateDynamics
from app.services.memory import MemorySystem
from app.services.brain import AgentBrain
from app.services.perception import PerceptionFilter
from app.models.agent import Agent, ActionType
from typing import List, Optional

class WorldEngine:
    def __init__(self):
        self.time_system = TimeSystem()
        self.map_system = MapSystem()
        self.state_dynamics = StateDynamics(self.map_system)
        self.perception_filter = PerceptionFilter(self.time_system)

    def create_agent(self, agent_id: str, x: int, y: int, use_mock_brain: bool = True) -> Agent:
        """创建并初始化一个完整的 Agent"""
        agent = Agent(id=agent_id, x=x, y=y, type="Agent")
        
        # 创建意识层组件
        memory = MemorySystem(agent_id=agent_id, use_mock=True)
        brain = AgentBrain(use_mock=use_mock_brain)
        perception = PerceptionFilter(self.time_system)
        
        # 绑定到 Agent
        agent.bind_soul(memory, brain, perception, self.map_system)
        
        # 注册到地图系统
        self.map_system.register_entity(agent)
        
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """获取指定 Agent"""
        entity = self.map_system.entities.get(agent_id)
        if entity and isinstance(entity, Agent):
            return entity
        return None

    def get_all_agents(self) -> List[Agent]:
        """获取所有 Agent"""
        return [e for e in self.map_system.entities.values() if isinstance(e, Agent)]

    def tick(self):
        """推进一个时间片"""
        # 1. 时间推进
        current_time = self.time_system.tick()
        
        # 2. 检测夜间条件（22:00 - 06:00）
        is_night = self.time_system.is_night()
        
        # 3. 遍历所有 Agent
        for agent_id, agent in self.map_system.entities.items():
            if not isinstance(agent, Agent) or not agent.is_active:
                continue
            
            # 夜间处理：强制睡眠和反思
            if is_night:
                self._handle_night_time(agent, current_time)
            
            # 早晨唤醒（07:00）
            if current_time.hour == 7 and current_time.minute == 0:
                if agent.is_sleeping:
                    agent.wake_up()
            
            # 应用当前动作的效果
            self.state_dynamics.apply_action_effect(agent_id, agent.current_action)

    def run_agent_loop(self, ticks: int = 1):
        """运行 Agent 循环，驱动多个时间片"""
        for _ in range(ticks):
            # 1. 时间推进
            current_time = self.time_system.tick()
            
            # 2. 检测夜间条件（22:00 - 06:00）
            is_night = self.time_system.is_night()
            
            # 3. 遍历所有 Agent
            for agent in self.get_all_agents():
                if not agent.is_active:
                    continue
                
                # 夜间处理：强制睡眠和反思
                if is_night:
                    self._handle_night_time(agent, current_time)
                
                # 早晨唤醒（07:00）
                if current_time.hour == 7 and current_time.minute == 0:
                    if agent.is_sleeping:
                        agent.wake_up()
                
                # 执行决策（如果没睡觉）
                if not agent.is_sleeping:
                    agent.decide_and_act()
            
            # 4. 应用行动效果
            for agent in self.get_all_agents():
                if agent.is_active:
                    self.state_dynamics.apply_action_effect(agent.id, agent.current_action)

    def _handle_night_time(self, agent: Agent, current_time):
        """处理夜间逻辑：强制睡眠和反思"""
        # 如果 Agent 还没睡觉，强制进入睡眠
        if not agent.is_sleeping:
            agent.is_sleeping = True
            agent.current_action = ActionType.SLEEP
            agent._memory.add_short_term("It's night time, I must sleep.")
        
        # 在 00:00 触发反思机制
        if current_time.hour == 0 and current_time.minute == 0:
            self._trigger_reflection(agent)

    def _trigger_reflection(self, agent: Agent):
        """触发 Agent 的反思机制"""
        if not agent._brain or not agent._memory:
            return
        
        # 生成反思
        reflection = agent._brain.reflect(agent.daily_log)
        
        # 更新价值观
        agent.values = reflection
        
        # 归档记忆
        summary = f"Daily Log: {agent.daily_log}\nReflection: {reflection}"
        agent._memory.consolidate_daily(summary)
        
        # 清空每日日志
        agent.daily_log = ""

    def inject_event(self, event_type: str, description: str, target_agents: Optional[List[str]] = None):
        """注入全局事件"""
        targets = target_agents if target_agents else list(self.map_system.entities.keys())
        
        for agent_id in targets:
            agent = self.get_agent(agent_id)
            if agent and agent._memory:
                agent._memory.add_short_term(f"[EVENT] {event_type}: {description}")

# Singleton Instance
world = WorldEngine()
