from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from bdd.schemas import ClientsSerializer, UserSerializer
from auth.auth import (
    encrypt_and_hash_password,
    check_password,
    jwt_create
)
from auth.middlewares import JWTMiddleware
from utils.utils import (
    read_bdd,
    now,
    write_new_line_bdd,
    filter_by_id,
    update_dict_in_list,
    write_csv,
    remove_client_by_id
)

app = FastAPI()
app.add_middleware(JWTMiddleware)

@app.api_route("/clients", methods=["GET", 'POST', 'PATCH', "DELETE"])
def clients(request: Request, infos: ClientsSerializer=None) -> list:
    try:
        methodes = request.method
        clients = read_bdd()
        if methodes == "GET":
            params = request.query_params
            is_filter = params.get("filter", None)
            if is_filter == "oui":
                id_client = params.get("client_id", None)
                if id_client is not None:
                    _, filter = filter_by_id(clients, id_client)
                    return JSONResponse(filter, status_code=200)
            else:
                return JSONResponse(clients, status_code=200)
        elif methodes == "POST":
            values = [len(clients)+1, infos.nom, infos.prenom, infos.email, now(), infos.pays]
            write_new_line_bdd(values)
            return JSONResponse({"message": f"Client id:{values[0]} créé avec succès"}, status_code=201)
        elif methodes == "PATCH":
            dict_recup = infos.model_dump()
            if dict_recup["client_id"] is not None:
                initial, _ = filter_by_id(clients, infos.client_id)
                modified_list = update_dict_in_list(initial, dict_recup)
                write_csv(modified_list)
                return JSONResponse({"message": f"Client id:{infos.client_id} modifié avec succès"}, status_code=200)
        elif methodes == "DELETE":
            message, update_list = remove_client_by_id(clients, infos.client_id)
            write_csv(update_list)
            return JSONResponse({
                "message": message
            }, status_code=200)
    except Exception as e:
        return JSONResponse({
            "message": "Une erreur s'est produite"
        }, status_code=500)
    
@app.post('/register')
def enregistrement(request: Request, user_info: UserSerializer):
    password, email = user_info.password, user_info.email
    write_new_line_bdd([email, encrypt_and_hash_password(password)], path='./bdd/utilisateurs.csv')

@app.post('/login')
def login(request: Request, user_info: UserSerializer):
    bdd = read_bdd('./bdd/utilisateurs.csv')
    for user in bdd:
        if user['email'] == user_info.email:
            is_authenticated = check_password(user['password'], user_info.password)
            if is_authenticated:
                connection = jwt_create({"sub": user_info.email, "is_authenticated": True})
                return JSONResponse(connection, status_code=200)
            else:
                return JSONResponse({
                    "message": "Identifiants non corrects"
                }, status_code=401)
    return JSONResponse({
        "message": "Utilisateur inconnu"
    }, status_code=400)

