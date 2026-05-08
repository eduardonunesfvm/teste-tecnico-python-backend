from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import pegar_sessao
from api.producao.service import obter_diagnostico_produtividade, obter_todos_registros, registrar_foco
from api.producao.schemas import RegistroSchema


router = APIRouter(prefix="/producao", tags=["producao"])

@router.get("/get")
def home():
    return {"mensagem": "Você acessou a rota padrão da api"}

@router.get("/obter_diagnostico/visualizar", status_code=200)
def visualizar_diagnostico( session: Session = Depends(pegar_sessao)):
    return obter_diagnostico_produtividade(session)

@router.get("/obter_todos_registros", status_code=200)
def visualizar_todos_registros(session: Session = Depends(pegar_sessao)):
    return obter_todos_registros(session)

@router.post("/registrar_foco", status_code=201)
def registrar_foco_endpoint(registro: RegistroSchema, session: Session = Depends(pegar_sessao)):
    return registrar_foco(registro, session)



