
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
    response = requests.post(login_url, data=data)
    return response.json()["access_token"]

@app.post("/crear_usuario")
def crear_usuario(username: str = Form(...), password: str = Form(...)):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "UserName": username,
        "Password": password,
        "ConfirmPassword": password,
        "PhoneNumber": "",
        "Email": ""
    }
    res = requests.post("https://local-admin.flowbets.co/crear_jugador", json=payload, headers=headers)
    return res.json()
