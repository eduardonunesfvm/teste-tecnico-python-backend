from pydantic import BaseModel, ConfigDict, Field

class RegistroSchema(BaseModel):
    nivel_foco: int = Field(ge=1, le=5, description="Nível de foco de 1 a 5")
    tempo_minutos: int = Field(gt=0, description="Tempo em minutos")
    comentario: str
    categoria: str | None = None
    
class RegistroResponse(BaseModel):
    id: int
    nivel_foco: int
    tempo_minutos: int
    comentario: str
    categoria: str | None

    model_config = ConfigDict(from_attributes=True)
    
# class DiagnosticoResponse(BaseModel):
#     media_foco: float
#     tempo_total_minutos: int
#     total_registros: int
#     mensagem: str