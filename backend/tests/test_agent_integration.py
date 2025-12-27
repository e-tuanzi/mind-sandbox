from app.services.world import WorldEngine
from app.models.agent import ActionType

def test_agent_creation_and_binding():
    """测试 Agent 创建和意识层绑定"""
    world_engine = WorldEngine()
    
    agent = world_engine.create_agent(agent_id="test_agent", x=0, y=0)
    
    assert agent.id == "test_agent"
    assert agent.x == 0
    assert agent.y == 0
    assert agent._memory is not None
    assert agent._brain is not None
    assert agent._perception is not None

def test_agent_decision_loop():
    """测试 Agent 完整决策循环"""
    world_engine = WorldEngine()
    
    agent = world_engine.create_agent(agent_id="tired_agent", x=0, y=0)
    agent.stats.energy = 10
    agent.stats.wealth = 100
    
    action = agent.decide_and_act()
    
    assert action == ActionType.SLEEP
    assert agent.current_action == ActionType.SLEEP

def test_multiple_agents_simulation():
    """测试多个 Agent 并发决策"""
    world_engine = WorldEngine()
    
    agent1 = world_engine.create_agent(agent_id="agent1", x=0, y=0)
    agent1.stats.energy = 100
    agent1.stats.wealth = 0
    
    agent2 = world_engine.create_agent(agent_id="agent2", x=1, y=0)
    agent2.stats.energy = 100
    agent2.stats.wealth = 100
    
    world_engine.run_agent_loop(ticks=1)
    
    assert agent1.current_action != ActionType.IDLE
    assert agent2.current_action != ActionType.IDLE
    assert agent1.current_action == ActionType.WORK_996

def test_night_time_reflection():
    """测试夜间反思机制"""
    world_engine = WorldEngine()
    
    world_engine.time_system.current_time.hour = 23
    world_engine.time_system.current_time.minute = 0
    
    agent = world_engine.create_agent(agent_id="reflective_agent", x=0, y=0)
    agent.daily_log = "Today I worked hard and earned money."
    
    for _ in range(60):
        world_engine.tick()
    
    assert agent.is_sleeping == True
    assert len(agent.values) > 0

def test_event_injection():
    """测试事件注入"""
    world_engine = WorldEngine()
    
    agent = world_engine.create_agent(agent_id="event_agent", x=0, y=0)
    
    world_engine.inject_event(
        event_type="Crisis",
        description="Stock market crash! Everyone lost money.",
        target_agents=["event_agent"]
    )
    
    recent_memory = agent._memory.get_recent_context()
    assert "Stock market crash" in recent_memory or "EVENT" in recent_memory

def test_agent_wake_up():
    """测试 Agent 唤醒机制"""
    world_engine = WorldEngine()
    
    # 设置时间为晚上 23:00
    world_engine.time_system.current_time.hour = 23
    world_engine.time_system.current_time.minute = 0
    
    agent = world_engine.create_agent(agent_id="sleepy_agent", x=0, y=0)
    
    # 运行一个 tick，应该进入睡眠
    world_engine.tick()
    assert agent.is_sleeping == True
    
    # 设置时间为早晨 06:59，tick 后会变成 07:00
    world_engine.time_system.current_time.hour = 6
    world_engine.time_system.current_time.minute = 59
    
    # 运行 tick，时间推进到 07:00，系统应自动唤醒 Agent
    world_engine.tick()
    assert agent.is_sleeping == False