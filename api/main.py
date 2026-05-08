from fastapi import FastAPI
from api.producao.router import router

app = FastAPI(
    title="Foco e Producao API",
    version="1.0.0",
    description="API desenvolvida para o teste tecnico da Sou Junior, colode /docs na url e acesse a API no swagger"
)

@app.get("/")
def home():
    return {
        "message": "Bem-vindo a Foco e Producao API ",
        "docs": "/docs",
        "redoc": "/redoc",
        "routes": {
            "/registro-foco": "Registro de foco",
            "/diagnostico-produtividade": "diagnostico de produtividade",
        }
    }

app.include_router(router)