import pytest
from app.services.time_system import TimeSystem
from app.services.map_system import MapSystem
from app.models.map import TerrainType
from app.models.agent import Agent, ActionType

def test_time_flow_env_001():
    """ENV-001: 时间流逝测试"""
    ts = TimeSystem()
    initial_hour = ts.current_time.hour
    
    # Tick 60 times (assuming 1 tick = 1 min)
    for _ in range(60):
        ts.tick()
        
    assert ts.current_time.hour == initial_hour + 1
    assert ts.current_time.minute == 0

def test_move_block_env_003():
    """ENV-003: 移动阻挡测试"""
    ms = MapSystem()
    
    # Set (1, 1) as Wall
    ms.set_terrain(1, 1, TerrainType.WALL, is_walkable=False)
    
    # Create Agent at (1, 0)
    agent = Agent(id="test_agent", x=1, y=0, type="Agent")
    ms.register_entity(agent)
    
    # Try move to (1, 1) - Should fail
    success = ms.move_entity(agent.id, (1, 1))
    assert success is False
    assert agent.x == 1
    assert agent.y == 0
    
    # Try move to (0, 0) - Should succeed (assuming (0,0) is empty/walkable default)
    success = ms.move_entity(agent.id, (0, 0))
    # Note: Diagonal move might be restricted in my impl logic `dx > 1 or dy > 1` allows diagonal (1,1).
    # Let's check my impl: `dx = abs(1-0)=1`, `dy = abs(0-0)=0`. This is valid.
    assert success is True
    assert agent.x == 0
    assert agent.y == 0

def test_state_dynamics_env_002():
    """ENV-002: 996工作数值结算 (Simplified)"""
    # Note: This test requires StateDynamics logic.
    from app.services.state_dynamics import StateDynamics
    
    ms = MapSystem()
    sd = StateDynamics(ms)
    
    agent = Agent(id="worker", x=0, y=0, type="Agent")
    # Initial stats
    agent.stats.energy = 100
    agent.stats.wealth = 0
    ms.register_entity(agent)
    
    # Apply WORK_996 effect once
    sd.apply_action_effect(agent.id, ActionType.WORK_996)
    
    assert agent.stats.energy < 100
    assert agent.stats.wealth > 0
    assert agent.stats.sanity < 100
