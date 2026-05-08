from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.producao.schemas import RegistroSchema
from api.producao.repository import buscar_todos_registros, inserir_diagnostico_produtividade


def obter_diagnostico_produtividade(session: Session):
    registros = buscar_todos_registros(session)

    if not registros:
        return {
            "media_foco": 0,
            "tempo_total_minutos": 0,
            "total_registros": 0,
            "mensagem": "Nenhum registro encontrado para gerar diagnóstico."
        }

    total_registros = len(registros)
    media_foco = sum(registro.nivel_foco for registro in registros) / total_registros
    tempo_total = sum(registro.tempo_minutos for registro in registros)

    if media_foco <= 3:
        mensagem = (
            "O diagnóstico indica que sua produtividade está baixa. "
            "Considere identificar e minimizar distrações, estabelecer metas claras "
            "e criar um ambiente de trabalho mais focado."
    )
    else:
        mensagem = (
            "O diagnóstico indica que sua produtividade está boa. "
            "Continue mantendo seus hábitos produtivos e busque aprimorar "
            "sua gestão de tempo e foco."
        )

    return {
        "media_foco": round(media_foco, 2),
        "tempo_total_minutos": tempo_total,
        "total_registros": total_registros,
        "mensagem": mensagem
    }
    
def obter_todos_registros(session: Session):
    registros = buscar_todos_registros(session)
    return {
        "registros": registros
    }
    

def registrar_foco(registroSchema: RegistroSchema, session: Session):
    novo_registro = inserir_diagnostico_produtividade(registroSchema, session)
    return novo_registro
    