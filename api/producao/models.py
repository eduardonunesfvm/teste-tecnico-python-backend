from sqlalchemy import Column, String, Integer
from api.database import Base

# Registro de foco
class Registros(Base):
    __tablename__ = "registros"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nivel_foco = Column("nivel_foco", Integer, nullable=False)
    tempo_minutos = Column("tempo_minutos", Integer, nullable=False)
    comentario = Column("comentario", String, nullable=True) #usuario digita o que fez durante o tempo de foco ou o que causou distração.
    categoria = Column("categoria", String, nullable=True) #opcional, o usuario pode categorizar o registro como trabalho, estudo, lazer, etc.

    def __init__(self, nivel_foco, tempo_minutos, comentario, categoria=None):
        self.nivel_foco = nivel_foco
        self.tempo_minutos = tempo_minutos
        self.comentario = comentario
        self.categoria = categoria
