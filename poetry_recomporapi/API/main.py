from fastapi import FastAPI
from API.routes.composteira_routes import router as composteira_router
from API.routes.compostagem_routes import router as compostagem_router
from API.routes.user_routes import router as user_router

app = FastAPI(                                 
    title = "Recompor - API",
    description = "A compostagem doméstica é um processo que ajuda a diminuir a emissão de gás carbônico no meio ambiente. " \
    "Atualmente existem dois projetos focados em desenvolver sistemas que ajudem as pessoas a entenderem o que é compostagem e como executá-la em casa, um sistema web e outro mobile. " \
    "O Projeto consiste no desenvolvimento de uma API (Application Programming Interface) para integrar e unificar esses dois sistemas. " \
    "O intuito desse projeto é democratizar o uso dos sistemas, " \
    "permitindo que os usuários acessem o sistema no dispositivo que eles tiverem disponível no momento. Além disso, a API garante melhor segurança dos dados e facilita o processo de atualização dos sistemas.",
    version = "pre-alfa", 
    contact = {
        "name": "the developers",
        "email": "luizfelipemam2007@gmail.com",
        "email": "celsohectorhm@gmail.com",
    },
) 

app.include_router(compostagem_router)
app.include_router(composteira_router)
app.include_router(user_router)

@app.get("/")
def welcome():
    return {"mensagem": "Está é a API do projeto Recompor"}

@app.get("/status")
def api_status():
    return {"status": "online",
            "versão": "pre-alfa"}

#luiz-endpoits