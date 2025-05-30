from pydantic import BaseModel

class DadosUser(BaseModel):
    username: str
    password: str
    email: str
    