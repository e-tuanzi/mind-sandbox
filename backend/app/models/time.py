from pydantic import BaseModel

class GameTime(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    
    def __str__(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}"
