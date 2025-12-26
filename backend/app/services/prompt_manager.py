from typing import Dict, Any
import json
from app.core.config import settings
from app.core.prompts import DECISION_PROMPTS, REFLECTION_PROMPTS

class PromptManager:
    """
    提示词管理器，负责根据配置的语言加载和格式化提示词模板。
    """
    
    def __init__(self, language: str = None):
        """
        初始化提示词管理器。
        
        :param language: 指定语言（"en" 或 "zh"），如果不指定则从配置中读取。
        """
        self.language = language or settings.LANGUAGE
        if self.language not in ["en", "zh"]:
            self.language = "en" # 默认回退到英文

    def get_decision_prompt(self, perception_text: str, memory_context: str, stats: Dict[str, Any]) -> Dict[str, str]:
        """
        获取并格式化决策提示词。
        
        :param perception_text: 感知文本
        :param memory_context: 记忆上下文
        :param stats: 状态数据
        :return: 包含 system 和 user 提示词的字典
        """
        templates = DECISION_PROMPTS.get(self.language, DECISION_PROMPTS["en"])
        
        user_prompt = templates["user"].format(
            perception_text=perception_text,
            memory_context=memory_context,
            stats_json=json.dumps(stats, indent=2, ensure_ascii=False)
        )
        
        return {
            "system": templates["system"],
            "user": user_prompt
        }

    def get_reflection_prompt(self, daily_log: str) -> Dict[str, str]:
        """
        获取并格式化反思提示词。
        
        :param daily_log: 当日日志
        :return: 包含 system 和 user 提示词的字典
        """
        templates = REFLECTION_PROMPTS.get(self.language, REFLECTION_PROMPTS["en"])
        
        user_prompt = templates["user"].format(daily_log=daily_log)
        
        return {
            "system": templates["system"],
            "user": user_prompt
        }

# 全局单例
prompt_manager = PromptManager()
