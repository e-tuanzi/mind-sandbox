from app.models.time import GameTime
from app.core.config import settings

class TimeSystem:
    def __init__(self):
        # Initial time: Year 2024, Month 1, Day 1, 07:00 (Morning)
        self.current_time = GameTime(year=2024, month=1, day=1, hour=7, minute=0)
        self.minutes_per_tick = settings.MINUTES_PER_TICK

    def tick(self) -> GameTime:
        """推进一个时间片"""
        self.current_time.minute += self.minutes_per_tick
        self._normalize_time()
        return self.current_time

    def get_current_time(self) -> GameTime:
        """获取当前游戏时间"""
        return self.current_time

    def is_night(self) -> bool:
        """判断是否为夜晚（用于触发休眠）。假设 22:00 到 06:00 为夜晚"""
        hour = self.current_time.hour
        return hour >= 22 or hour < 6

    def _normalize_time(self):
        """处理时间进位"""
        while self.current_time.minute >= 60:
            self.current_time.minute -= 60
            self.current_time.hour += 1
        
        while self.current_time.hour >= 24:
            self.current_time.hour -= 24
            self.current_time.day += 1
            
        # 简化版日历：每月30天
        while self.current_time.day > 30:
            self.current_time.day -= 30
            self.current_time.month += 1
            
        while self.current_time.month > 12:
            self.current_time.month -= 12
            self.current_time.year += 1
