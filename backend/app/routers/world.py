from fastapi import APIRouter, Query
from app.services.world import world
from app.core.translations import get_translation

router = APIRouter()

@router.get("/status")
def get_world_status(language: str = Query("zh", description="语言代码: 'en' 或 'zh'")):
    """
    获取世界状态
    
    Args:
        language: 语言代码（"en" 或 "zh"）
    """
    current_time = world.time_system.get_current_time()
    active_agents = len([a for a in world.map_system.entities.values() if a.is_active])
    
    weather_map = {
        "Sunny": {"en": "Sunny", "zh": "晴天"},
        "Rainy": {"en": "Rainy", "zh": "雨天"},
        "Cloudy": {"en": "Cloudy", "zh": "多云"}
    }
    
    weather = "Sunny"  # Placeholder
    weather_translation = weather_map.get(weather, {}).get(language, weather)
    
    return {
        "time": str(current_time),
        "weather": weather,
        "weather_translation": weather_translation,
        "active_agents": active_agents,
        "is_night": world.time_system.is_night()
    }
