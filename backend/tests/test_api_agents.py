from fastapi.testclient import TestClient
from app.main import app
from app.services.world import world
from app.models.agent import ActionType

client = TestClient(app)

def test_get_all_agents():
    """测试获取所有 Agent 列表"""
    world.create_agent("api_test_1", 0, 0)
    world.create_agent("api_test_2", 1, 0)
    
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    agent = data[0]
    assert "id" in agent
    assert "x" in agent
    assert "y" in agent
    assert "stats" in agent
    assert "current_action" in agent
    assert "is_active" in agent
    assert "values" in agent

def test_get_agent_by_id():
    """测试获取指定 Agent 的详细状态"""
    world.create_agent("api_test_detail", 0, 0)
    
    response = client.get("/api/v1/agents/api_test_detail")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == "api_test_detail"
    assert data["type"] == "Agent"
    assert "health" in data["stats"]
    assert "sanity" in data["stats"]
    assert "wealth" in data["stats"]
    assert "energy" in data["stats"]

def test_get_agent_thought():
    """测试获取 Agent 的最新思维内容"""
    agent = world.create_agent("api_test_thought", 0, 0)
    agent.decide_and_act()
    
    response = client.get("/api/v1/agents/api_test_thought/thought")
    assert response.status_code == 200
    
    data = response.json()
    assert "content" in data
    assert "timestamp" in data
    assert "action" in data

def test_get_agent_history():
    """测试获取 Agent 的历史日记记录"""
    agent = world.create_agent("api_test_history", 0, 0)
    agent.daily_log = "Today was a long day."
    
    response = client.get("/api/v1/agents/api_test_history/history")
    assert response.status_code == 200
    
    data = response.json()
    assert data["agent_id"] == "api_test_history"
    assert "history" in data
    assert "values" in data

def test_set_agent_action():
    """测试手动设置 Agent 的当前动作"""
    world.create_agent("api_test_action", 0, 0)
    
    response = client.post(
        "/api/v1/agents/api_test_action/action",
        json={"action": "WORK_996"}
    )
    assert response.status_code == 200
    
    agent = world.get_agent("api_test_action")
    assert agent.current_action == ActionType.WORK_996

def test_get_nonexistent_agent():
    """测试获取不存在的 Agent"""
    response = client.get("/api/v1/agents/nonexistent")
    assert response.status_code == 404