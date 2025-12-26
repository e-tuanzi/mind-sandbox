from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Digital Soul"
    API_V1_STR: str = "/api/v1"
    
    # Time System Configuration
    # 1 real second = X game minutes (Default: 1 tick = 1 minute)
    MINUTES_PER_TICK: int = 1
    
    # Map Configuration
    MAP_WIDTH: int = 100
    MAP_HEIGHT: int = 100
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
