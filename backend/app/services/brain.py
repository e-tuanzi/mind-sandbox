from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.models.agent import ActionType
from app.core.config import settings
from app.core.translations import get_translation
from openai import OpenAI
import json

class ActionDecision(BaseModel):
    action: ActionType
    target: Optional[Dict[str, Any]] = None # e.g. {"x": 10, "y": 20} or {"entity_id": "..."}
    thought: str

class AgentBrain:
    def __init__(self, use_mock: bool = True, language: str = None):
        """
        初始化 AgentBrain
        
        Args:
            use_mock: 是否使用 mock 模式
            language: 语言代码（"en" 或 "zh"），为 None 时使用配置中的默认语言
        """
        self.use_mock = use_mock
        self.language = language or settings.LANGUAGE
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

    def decide_next_action(self, perception_text: str, memory_context: str, stats: Dict, language: str = None) -> ActionDecision:
        """
        决策下一个动作
        
        Args:
            perception_text: 感知文本
            memory_context: 记忆上下文
            stats: 状态数据
            language: 语言代码，为 None 时使用初始化时的语言
        Returns:
            ActionDecision
        """
        current_language = language or self.language
        
        if self.use_mock:
            return self._mock_decision(perception_text, stats, current_language)
        
        return self._llm_decision(perception_text, memory_context, stats, current_language)

    def _mock_decision(self, perception_text: str, stats: Dict, language: str = "en") -> ActionDecision:
        """
        基于规则的 mock 决策逻辑
        
        Args:
            perception_text: 感知文本
            stats: 状态数据
            language: 语言代码
        """
        # Logic: 
        # 1. If Energy < 20 -> SLEEP
        # 2. If Wealth < 10 -> WORK_996
        # 3. Else -> IDLE or REST
        
        energy = stats.get("energy", 100)
        wealth = stats.get("wealth", 0)
        
        if energy < 20:
            return ActionDecision(
                action=ActionType.SLEEP,
                thought=get_translation("thought.too_tired", language)
            )
        
        if wealth < 50:
             return ActionDecision(
                action=ActionType.WORK_996,
                thought=get_translation("thought.broke", language)
            )
            
        return ActionDecision(
            action=ActionType.REST_PARK,
            thought=get_translation("thought.chill", language)
        )

    def _llm_decision(self, perception_text: str, memory_context: str, stats: Dict, language: str = "en") -> ActionDecision:
        """
        使用真实LLM进行决策
        
        Args:
            perception_text: 感知文本
            memory_context: 记忆上下文
            stats: 状态数据
            language: 语言代码
        """
        prompts = prompt_manager.get_decision_prompt(perception_text, memory_context, stats, language)
        
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
