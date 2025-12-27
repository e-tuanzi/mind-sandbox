"""
后端翻译字典，用于支持多语言输出
"""

TRANSLATIONS = {
    "en": {
        # Agent thoughts - Mock mode
        "thought.too_tired": "I am too tired. I need to sleep.",
        "thought.broke": "I am broke. I need to work hard.",
        "thought.chill": "I have some money and energy. I will chill at the park.",
        "thought.no_thought": "No thought recorded yet.",
        
        # Agent actions
        "action.WORK_996": "Working hard (996 schedule)",
        "action.WORK_965": "Working (9-5 schedule)",
        "action.REST_PARK": "Resting at park",
        "action.CONSUME_ENT": "Consuming entertainment",
        "action.SLEEP": "Sleeping",
        "action.IDLE": "Idling",
        
        # Agent values
        "values.default": "Survival first, health is most important.",
        
        # Messages
        "message.action_set": "Agent {agent_id} action set to {action}",
        "message.agent_created": "Agent {agent_id} created successfully.",
        "message.event_injected": "Event '{event_type}' injected successfully.",
        "message.world_reset": "World reset successfully.",
        "message.advanced_ticks": "Advanced {ticks} tick(s).",
        
        # Memory events
        "memory.failed_move": "Failed to move to ({x}, {y})",
        "memory.woke_up": "I woke up.",
        
        # Status
        "status.no_memory": "No memory recorded yet.",
    },
    "zh": {
        # Agent thoughts - Mock mode
        "thought.too_tired": "我太累了，需要休息一下。",
        "thought.broke": "我没钱了，需要努力工作。",
        "thought.chill": "我有了一些钱和精力，我会在公园放松一下。",
        "thought.no_thought": "还没有记录想法。",
        
        # Agent actions
        "action.WORK_996": "努力工作（996 作息）",
        "action.WORK_965": "工作（朝九晚五）",
        "action.REST_PARK": "在公园休息",
        "action.CONSUME_ENT": "消费娱乐",
        "action.SLEEP": "睡觉",
        "action.IDLE": "发呆",
        
        # Agent values
        "values.default": "生存第一，健康最重要。",
        
        # Messages
        "message.action_set": "Agent {agent_id} 的动作已设置为 {action}",
        "message.agent_created": "Agent {agent_id} 创建成功。",
        "message.event_injected": "事件 '{event_type}' 注入成功。",
        "message.world_reset": "世界已重置。",
        "message.advanced_ticks": "推进了 {ticks} 个时间片。",
        
        # Memory events
        "memory.failed_move": "移动到 ({x}, {y}) 失败",
        "memory.woke_up": "我醒了。",
        
        # Status
        "status.no_memory": "还没有记录记忆。",
    }
}


def get_translation(key: str, language: str = "en", **kwargs) -> str:
    """
    根据语言键和语言代码获取翻译文本
    
    Args:
        key: 翻译键（如 "thought.too_tired"）
        language: 语言代码（"en" 或 "zh"）
        **kwargs: 用于格式化字符串的参数
    
    Returns:
        翻译后的文本
    """
    language = language if language in ["en", "zh"] else "en"
    
    if language not in TRANSLATIONS:
        language = "en"
    
    translation = TRANSLATIONS[language].get(key, key)
    
    if kwargs:
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError):
            return translation
    
    return translation
