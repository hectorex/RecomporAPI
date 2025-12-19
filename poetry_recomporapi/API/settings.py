from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações globais da aplicação utilizando Pydantic BaseSettings.
    Carrega automaticamente variáveis do arquivo .env ou variáveis de ambiente do SO.
    """
    model_config = SettingsConfigDict(
        # Garante compatibilidade de caracteres entre Windows/Linux
        env_file=".env", env_file_encoding="utf-8" #prevenção de erros de OS
    )

    # URL de conexão com o banco (ex: postgresql://user:pass@localhost/db)
    DATABASE_URL: str
