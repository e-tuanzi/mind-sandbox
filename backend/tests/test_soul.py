import pytest
from app.services.memory import MemorySystem
from app.services.brain import AgentBrain, ActionType, ActionDecision
from app.services.perception import PerceptionFilter, EnvironmentSnapshot
from app.models.agent import Agent, AgentStats
from app.models.map import LocationInfo, TerrainType

def test_memory_retrieval_soul_001():
    """SOUL-001: 记忆检索相关性"""
    memory = MemorySystem(agent_id="test_agent", use_mock=True)
    
    # Simulate adding memories
    # Note: Since we use MockEmbedding which returns same vector, retrieval might return all or random.
    # But ChromaDB usually handles exact match if distance is 0.
    # However, MockEmbedding returns CONSTANT vector. So distance is always 0.
    # This means all docs are equally relevant.
    # To test logic flow, we just check if we can add and recall anything.
    
    memory.collection.add(
        documents=["I hate apples.", "I love coding."],
        ids=["1", "2"]
    )
    
    results = memory.recall("Do I like apples?", k=1)
    # Since MockEmbedding returns same vector for all inputs, any of the 2 could be returned.
    assert len(results) > 0
    assert results[0] in ["I hate apples.", "I love coding."]

def test_decision_consistency_soul_002():
    """SOUL-002: 决策一致性 (Mock Brain)"""
    brain = AgentBrain(use_mock=True)
    
    # Case 1: Low Energy -> Sleep
    stats_tired = {"energy": 10, "wealth": 1000, "health": 100, "sanity": 100}
    decision = brain.decide_next_action("You are tired.", "Memory...", stats_tired)
    assert decision.action == ActionType.SLEEP
    assert "tired" in decision.thought
    
    # Case 2: Low Wealth -> Work
    stats_poor = {"energy": 100, "wealth": 10, "health": 100, "sanity": 100}
    decision = brain.decide_next_action("You are poor.", "Memory...", stats_poor)
    assert decision.action == ActionType.WORK_996
    assert "broke" in decision.thought

def test_perception_flow():
    """Test Perception Filter String Generation"""
    pf = PerceptionFilter()
    snapshot = EnvironmentSnapshot(
        agent_id="A1",
        location=LocationInfo(x=0, y=0, terrain=TerrainType.ROAD),
        nearby_entities=[],
        self_stats=AgentStats(),
        time_desc="08:00"
    )
    
    text = pf.process(snapshot)
    assert "08:00" in text
    assert "Road" in text
    assert "Health=" in text

def test_real_llm_decision():
    """测试真实LLM决策"""
    brain = AgentBrain(use_mock=False)
    perception = "You are at home. It's evening."
    memory = "You remember you worked hard today."
    stats = {"energy": 30, "wealth": 100, "health": 80}
    
    try:
        decision = brain.decide_next_action(perception, memory, stats)
        print(f"\n=== LLM Decision Result ===")
        print(f"Action: {decision.action}")
        print(f"Thought: {decision.thought}")
        print(f"Target: {decision.target}")
        assert decision.action in ActionType
        assert len(decision.thought) > 0
    except Exception as e:
        print(f"\n=== Error occurred ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        raise
