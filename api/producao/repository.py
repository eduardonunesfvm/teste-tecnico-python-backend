from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.producao.models import Registros
from api.producao.schemas import RegistroSchema

def buscar_registro_por_id(registro_id: int, session: Session):
    return (
        session.query(Registros)
        .filter(Registros.id == registro_id)
        .first()
    )

def buscar_todos_registros(session: Session):
    return session.query(Registros).all()

def buscar_diagnostico_produtividade(diagnostico_id: int, session: Session):
    registros = buscar_registro_por_id(diagnostico_id, session)
    if not registros:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return {
        "id": registros.id,
        "nivel_foco": registros.nivel_foco,
        "tempo_minutos": registros.tempo_minutos,
        "comentario": registros.comentario,
        "categoria": registros.categoria
    }

def inserir_diagnostico_produtividade(registro: Registros, session: Session): #essa funcao armazena no banco
    novo_diagnostico = Registros(
        nivel_foco=registro.nivel_foco,
        tempo_minutos=registro.tempo_minutos,
        comentario=registro.comentario,
        categoria=registro.categoria
    )
    session.add(novo_diagnostico)
    session.commit()
    session.refresh(novo_diagnostico)
    return novo_diagnostico
    