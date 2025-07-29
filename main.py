
from fastapi import FastAPI, Form
import requests

app = FastAPI()

USERNAME = "rosario"
PASSWORD = "luciano151418"

def get_token():
    login_url = "https://agentes.flowbets.co/api/auth/login"
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "client_id": "web_client",
        "client_secret": "123456",
        "grant_type": "password"
    }
    try:
        response = requests.post(login_url, data=data)
        print("Login status:", response.status_code)
        print("Login response:", response.text)
        response.raise_for_status()
        return response.json().get("access_token")
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
