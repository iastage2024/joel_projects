import datetime, csv
from typing import Tuple

def read_bdd(path='./bdd/clients.csv') -> list:
    with open(path) as f:
        lines = f.readlines()
        keys = lines[0].strip().split(",")
        clients = []
        for line in lines[1:]:
            dict_client = {}
            values = line.strip().split(",")
            for idx, key in enumerate(keys):
                dict_client[key] = values[idx]
            clients.append(dict_client)
    return clients

def now() -> str:
    now = datetime.datetime.now()
    return str(now)[:10]

def write_new_line_bdd(new_row: list, path="./bdd/clients.csv"):
    with open(path, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(new_row)

def write_csv(data, headers=["client_id", "nom", "prenom", "email", "date_inscription", "pays"], path="./bdd/clients.csv"):
    with open(path, mode="w", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def filter_by_id(data_list: list, target_id: int) -> Tuple[list, dict]:
    found_dict = next((item for item in data_list if item.get('client_id') == target_id), None)
    return data_list, found_dict

def update_dict_in_list(data_list: list, updated_dict: dict) -> list[dict]:
    target_id = updated_dict.get("client_id")
    if target_id is None:
        raise ValueError("Le dictionnaire mis à jour doit contenir une clé 'client_id'.")

    for index, item in enumerate(data_list):
        if item.get("client_id") == target_id:
            updated_fields = {k: v for k, v in updated_dict.items() if v is not None}
            data_list[index] = {**item, **updated_fields}
            return data_list
        else:
            raise ValueError(f"Aucun dictionnaire avec l'id {target_id} trouvé dans la liste.")
        
def remove_client_by_id(clients: list, client_id: str) -> Tuple[str, list]:
    updated_clients = [client for client in clients if client.get("client_id") != client_id] 
    if len(clients) == len(updated_clients):
        return f"Aucun client avec client_id={client_id} n'a été trouvé.", updated_clients
    else:
        return f"Le client avec client_id={client_id} a été supprimé.", updated_clients




