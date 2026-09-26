from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    database_url:str='sqlite:///./fraudshield.db'; jwt_secret:str='change-this-in-production'; jwt_algorithm:str='HS256'; jwt_expire_minutes:int=60; cors_origins:list[str]=['http://localhost:5173']; model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()
