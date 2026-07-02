from pydantic import BaseModel

# criando uma Localizacao/ post
class LocalizacaoCreate(BaseModel):
    predio: str
    sala: str
    armario: str
    prateleira: str
    gaveta: str

# resposta da Localizacao/ get
class LocalizacaoResponse(BaseModel):
    id: int
    predio: str
    sala: str
    armario: str
    prateleira: str
    gaveta: str

    class Config:
        from_attributes = True

# Listagem de Localizacaos/ get
class LocalizacaoListResponse(BaseModel):
    localizacoes: list[LocalizacaoResponse]

# atualizacao da Localizacao/ patch
class LocalizacaoUpdate(BaseModel):
    predio: str | None = None
    sala: str | None = None
    armario: str | None = None
    prateleira: str | None = None
    gaveta: str | None = None