from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.world import world
from app.models.agent import Agent, ActionType
from app.core.translations import get_translation
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
def get_all_agents(language: str = Query("zh", description="语言代码: 'en' 或 'zh'")):
    """
    获取所有 Agent 列表
    
    Args:
        language: 语言代码（"en" 或 "zh"）
    """
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
            current_action=get_translation(f"action.{a.current_action.value}", language),
            is_active=a.is_active,
            is_sleeping=a.is_sleeping,
            values=a.values
        )
        for a in agents
    ]

@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str, language: str = Query("zh", description="语言代码: 'en' 或 'zh'")):
    """
    获取指定 Agent 的详细状态
    
    Args:
        agent_id: Agent ID
        language: 语言代码（"en" 或 "zh"）
    """
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
        current_action=get_translation(f"action.{agent.current_action.value}", language),
        is_active=agent.is_active,
        is_sleeping=agent.is_sleeping,
        values=agent.values
    )

@router.get("/{agent_id}/thought", response_model=ThoughtResponse)
def get_agent_thought(agent_id: str, language: str = Query("zh", description="语言代码: 'en' 或 'zh'")):
    """
    获取 Agent 的最新思维内容
    
    Args:
        agent_id: Agent ID
        language: 语言代码（"en" 或 "zh"）
    """
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
                    action=get_translation(f"action.{agent.current_action.value}", language)
                )
    
    return ThoughtResponse(
        content=get_translation("thought.no_thought", language),
        timestamp=timestamp,
        action=get_translation(f"action.{agent.current_action.value}", language)
    )

@router.get("/{agent_id}/history")
def get_agent_history(agent_id: str, language: str = Query("zh", description="语言代码: 'en' 或 'zh'")):
    """
    获取 Agent 的历史日记记录
    
    Args:
        agent_id: Agent ID
        language: 语言代码（"en" 或 "zh"）
    """
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
def set_agent_action(agent_id: str, request: SetActionRequest, language: str = Query("zh", description="语言代码: 'en' 或 'zh'")):
    """
    手动设置 Agent 的当前动作（用于测试）
    
    Args:
        agent_id: Agent ID
        request: 动作请求
        language: 语言代码（"en" 或 "zh"）
    """
    agent = world.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        agent.current_action = ActionType(request.action)
        return {
            "message": get_translation("message.action_set", language, agent_id=agent_id, action=request.action)
        }
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid action type")