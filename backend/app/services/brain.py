from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.models.agent import ActionType
from app.core.config import settings
from openai import OpenAI
import json

class ActionDecision(BaseModel):
    action: ActionType
    target: Optional[Dict[str, Any]] = None # e.g. {"x": 10, "y": 20} or {"entity_id": "..."}
    thought: str

class AgentBrain:
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        if not use_mock:
            self.client = OpenAI(
                api_key=settings.LLM_API_KEY,
                base_url=settings.LLM_BASE_URL,
                timeout=60.0
            )
            self.model = settings.LLM_MODEL
        else:
            self.client = None
            self.model = None

    def decide_next_action(self, perception_text: str, memory_context: str, stats: Dict) -> ActionDecision:
        """
        Input: 
            - perception_text: "You are at..."
            - memory_context: "You remember..."
            - stats: {"health": 80...}
        Output: ActionDecision
        """
        
        if self.use_mock:
            return self._mock_decision(perception_text, stats)
        
        return self._llm_decision(perception_text, memory_context, stats)

    def _mock_decision(self, perception_text: str, stats: Dict) -> ActionDecision:
        """Rule-based mock brain for testing"""
        # Logic: 
        # 1. If Energy < 20 -> SLEEP
        # 2. If Wealth < 10 -> WORK_996
        # 3. Else -> IDLE or REST
        
        energy = stats.get("energy", 100)
        wealth = stats.get("wealth", 0)
        
        if energy < 20:
            return ActionDecision(
                action=ActionType.SLEEP,
                thought="I am too tired. I need to sleep."
            )
        
        if wealth < 50:
             return ActionDecision(
                action=ActionType.WORK_996,
                thought="I am broke. I need to work hard."
            )
            
        return ActionDecision(
            action=ActionType.REST_PARK,
            thought="I have some money and energy. I will chill at the park."
        )

    def _llm_decision(self, perception_text: str, memory_context: str, stats: Dict) -> ActionDecision:
        """
        使用真实LLM进行决策
        """
        prompts = prompt_manager.get_decision_prompt(perception_text, memory_context, stats)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompts["system"]},
                {"role": "user", "content": prompts["user"]}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        decision_data = json.loads(content)
        
        return ActionDecision(
            action=ActionType(decision_data["action"]),
            target=decision_data.get("target"),
            thought=decision_data.get("thought", "")
        )
    
    def reflect(self, daily_log: str) -> str:
        """
        每日反思
        """
        if self.use_mock:
            return "Health is wealth." if settings.LANGUAGE == "en" else "健康就是财富。"
        
        prompts = prompt_manager.get_reflection_prompt(daily_log)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompts["system"]},
                {"role": "user", "content": prompts["user"]}
            ],
            temperature=0.8
        )
        
        return response.choices[0].message.content
