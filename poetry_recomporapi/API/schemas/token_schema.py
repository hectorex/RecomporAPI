from pydantic import BaseModel

class Token(BaseModel):
    # Estrutura padrão para resposta de autenticação JWT.
    access_token: str
    token_type: str