from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.services.world import world
from app.models.agent import Agent, ActionType
from pydantic import BaseModel

router = APIRouter()

class AgentResponse(BaseModel):
    id: str
    x: int
    y: int
    type: str
    stats: dict
    current_action: str
    is_active: bool
    is_sleeping: bool
    values: str

class ThoughtResponse(BaseModel):
    content: str
    timestamp: str
    action: str

class SetActionRequest(BaseModel):
    action: str

@router.get("", response_model=List[AgentResponse])
def get_all_agents():
    """获取所有 Agent 列表"""
    agents = world.get_all_agents()
    return [
        AgentResponse(
            id=a.id,
            x=a.x,
            y=a.y,
            type=a.type,
            stats={
                "health": a.stats.health,
                "sanity": a.stats.sanity,
                "wealth": a.stats.wealth,
                "energy": a.stats.energy
            },
            current_action=a.current_action.value,
            is_active=a.is_active,
            is_sleeping=a.is_sleeping,
            values=a.values
        )
        for a in agents
    ]

@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str):
    """获取指定 Agent 的详细状态"""
    agent = world.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return AgentResponse(
        id=agent.id,
        x=agent.x,
        y=agent.y,
        type=agent.type,
        stats={
            "health": agent.stats.health,
            "sanity": agent.stats.sanity,
            "wealth": agent.stats.wealth,
            "energy": agent.stats.energy
        },
        current_action=agent.current_action.value,
        is_active=agent.is_active,
        is_sleeping=agent.is_sleeping,
        values=agent.values
    )

@router.get("/{agent_id}/thought", response_model=ThoughtResponse)
def get_agent_thought(agent_id: str):
    """获取 Agent 的最新思维内容"""
    agent = world.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    from app.models.time import GameTime
    current_time = world.time_system.get_current_time()
    timestamp = f"{current_time.hour:02d}:{current_time.minute:02d}"
    
    if agent._memory:
        recent_context = agent._memory.get_recent_context()
        lines = recent_context.split("\n") if recent_context else []
        for line in reversed(lines):
            if line.startswith("Thought:"):
                return ThoughtResponse(
                    content=line.replace("Thought:", "").strip(),
                    timestamp=timestamp,
                    action=agent.current_action.value
                )
    
    return ThoughtResponse(
        content="No thought recorded yet.",
        timestamp=timestamp,
        action=agent.current_action.value
    )

@router.get("/{agent_id}/history")
def get_agent_history(agent_id: str):
    """获取 Agent 的历史日记记录"""
    agent = world.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    history = []
    if agent._memory:
        results = agent._memory.recall("diary summary", k=10)
        for result in results:
            history.append({"content": result})
    
    if agent.daily_log:
        history.append({"content": f"Current Day Log:\n{agent.daily_log}"})
    
    return {
        "agent_id": agent_id,
        "history": history,
        "values": agent.values
    }

@router.post("/{agent_id}/action")
def set_agent_action(agent_id: str, request: SetActionRequest):
    """手动设置 Agent 的当前动作（用于测试）"""
    agent = world.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        agent.current_action = ActionType(request.action)
        return {"message": f"Agent {agent_id} action set to {request.action}"}
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid action type")