from pydantic import BaseModel

class ClientsSerializer(BaseModel):
    client_id: str = None
    nom: str = None
    prenom: str = None
    email: str = None
    pays: str = None
    date_inscription: str = None


class UserSerializer(BaseModel):
    email: str = None
    password: str = None