from fastapi import FastAPI
from routes.composteira_routes import router as composteira_router
from routes.compostagem_routes import router as compostagem_router

app = FastAPI(                                 
    title = "API Composteira",
    description = "API ligação software web e mobile projeto Recompor",
    version = "0.1.1", 
    contact = {
        "name": "Celso Hector",
        "name": "Luiz Felipe",
        "email": "inserir-email-felipe",
        "email": "celsohectorhm@gmail.com",
    },
) 

app.include_router(compostagem_router)
app.include_router(composteira_router)

@app.get("/")
def welcome():
    return {"mensagem": "Está é a API do projeto Recompor"}

@app.get("/status")
def api_status():
    return {"status": "online",
            "versão": "0.1.1"}

