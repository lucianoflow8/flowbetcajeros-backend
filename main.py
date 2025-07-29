from fastapi import FastAPI, Form
import requests

app = FastAPI()

USERNAME = "rosario"
PASSWORD = "luciano151418"

def get_token():
    token_url = "https://agentes.flowbets.co/token"
    params = {
        "username": USERNAME,
        "password": PASSWORD,
        "client_id": "1_5i80w24kpcssc0okw0ww4gsc8kwg0k8gs0ok44skooww4swcg",
        "client_secret": "18qxs6584gw08scg8wsk8gow44oc4gcw40c4o8w44880g0kgcg",
        "grant_type": "password"
    }
    try:
        response = requests.get(token_url, params=params)
        print("Login status:", response.status_code)
        print("Login response:", response.text)
        response.raise_for_status()
        return response.json().get("token")  # OJO: el campo se llama "token"
    except Exception as e:
        print("Error al obtener el token:", e)
        return None

@app.post("/crear_usuario")
def crear_usuario(username: str = Form(...), password: str = Form(...)):
    print(f"Intentando crear usuario: {username}")
    token = get_token()
    if not token:
        return {"error": "No se pudo obtener el token. Revisá credenciales o login."}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "UserName": username,
        "Password": password,
        "ConfirmPassword": password,
        "PhoneNumber": "",
        "Email": ""
    }

    try:
        res = requests.post("https://local-admin.flowbets.co/crear_jugador", json=payload, headers=headers)
        print("Creación status:", res.status_code)
        print("Respuesta:", res.text)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Error al crear usuario:", e)
        return {"error": "Error en la creación", "detalle": str(e)}
