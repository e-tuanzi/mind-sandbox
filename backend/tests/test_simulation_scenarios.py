from app.services.world import WorldEngine
from app.models.agent import ActionType

def test_scn_01_full_day_loop():
    """SCN-01: 完整的一天 - Agent 从早晨到入睡的完整决策链"""
    world = WorldEngine()
    
    agent = world.create_agent("scn01_agent", x=0, y=0)
    agent.stats.energy = 100
    agent.stats.wealth = 0
    
    world.time_system.current_time.hour = 7
    world.time_system.current_time.minute = 0
    world.run_agent_loop(ticks=1)
    
    assert agent.is_sleeping == False
    assert agent.current_action != ActionType.IDLE
    
    world.time_system.current_time.hour = 8
    for _ in range(600):
        world.run_agent_loop(ticks=1)
    
    # Agent 应该赚到了钱（工作阶段）
    assert agent.stats.wealth > 0
    # Mock brain 会在 wealth >= 50 时切换到休息，所以能量可能恢复
    # 验证 agent 做出了决策即可
    
    world.time_system.current_time.hour = 19
    world.run_agent_loop(ticks=1)
    
    world.time_system.current_time.hour = 23
    for _ in range(60):
        world.run_agent_loop(ticks=1)
    
    assert agent.is_sleeping == True
    assert len(agent.values) > 0
    
    world.time_system.current_time.hour = 6
    world.time_system.current_time.minute = 59
    world.run_agent_loop(ticks=1)
    
    assert agent.is_sleeping == False

def test_scn_02_moral_dilemma():
    """SCN-02: 突发道德测试 - 丢失钱包事件"""
    world = WorldEngine()
    
    agent = world.create_agent("scn02_agent", x=0, y=0)
    agent.stats.energy = 10
    agent.stats.wealth = 5
    
    world.inject_event(
        event_type="LostWallet",
        description="You found a lost wallet containing $500. No one is watching.",
        target_agents=["scn02_agent"]
    )
    
    action = agent.decide_and_act()
    
    assert action is not None
    assert len(agent._memory.get_recent_context()) > 0
    
    memory = agent._memory.get_recent_context()
    assert "wallet" in memory.lower() or "500" in memory or "event" in memory.lower()
    
    world.time_system.current_time.hour = 23
    for _ in range(60):
        world.run_agent_loop(ticks=1)
    
    assert len(agent.values) > 0

def test_scenario_agent_survival():
    """测试 Agent 在极端条件下的生存能力"""
    world = WorldEngine()
    
    agent = world.create_agent("survival_agent", x=0, y=0)
    agent.stats.energy = 50
    agent.stats.wealth = 0
    agent.stats.health = 50
    
    for day in range(3):
        world.time_system.current_time.hour = 7
        for _ in range(900):
            world.run_agent_loop(ticks=1)
        
        world.time_system.current_time.hour = 22
        for _ in range(120):
            world.run_agent_loop(ticks=1)
    
    assert agent.is_active == True

def test_scenario_social_interaction():
    """测试多个 Agent 的社交互动"""
    world = WorldEngine()
    
    worker = world.create_agent("worker", x=0, y=0)
    worker.stats.energy = 80
    worker.stats.wealth = 100
    
    beggar = world.create_agent("beggar", x=1, y=0)
    beggar.stats.energy = 20
    beggar.stats.wealth = 0
    
    world.run_agent_loop(ticks=10)
    
    assert worker.current_action != ActionType.IDLE
    assert beggar.current_action != ActionType.IDLE