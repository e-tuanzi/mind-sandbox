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
    
    # LLM API Configuration (OpenAI Compatible)
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Language Configuration: "en" or "zh"
    LANGUAGE: str = "zh"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
