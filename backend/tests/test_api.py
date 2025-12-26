from fastapi.testclient import TestClient
from app.main import app
from app.services.world import world

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to" in response.json()["message"]

def test_get_world_status():
    response = client.get("/api/v1/world/status")
    assert response.status_code == 200
    data = response.json()
    assert "time" in data
    assert "weather" in data
    assert "active_agents" in data
    assert "is_night" in data
    
    # Check if time format matches
    # "2024-01-01 07:00"
    assert "2024" in data["time"]
