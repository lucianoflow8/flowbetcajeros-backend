from fastapi import FastAPI, Form
import requests
import csv
import os

app = FastAPI()

USERNAME = "rosario"
PASSWORD = "luciano151418"
CLIENT_ID = "1_5i50wo24kpcscc0okw0ww4gsc8kwg0k8gs0ok44skooww4swcg"
CLIENT_SECRET = "18qxs6584gw08scg8wsk8gow44oc4gcw40c4o8w44880g0gkcg"

def get_token():
    url = "https://admin.flowbets.co/oauth/v2/token"
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "password",
        "source": "pn"
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        print("Error al obtener el token:", e)
        return None

def guardar_telefono(username, telefono):
    archivo = "telefonos.csv"
    existe = os.path.isfile(archivo)
    with open(archivo, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["username", "telefono"])
        writer.writerow([username, telefono])

@app.post("/crear_usuario")
def crear_usuario(
    username: str = Form(...),
    password: str = Form(...),
    telefono: str = Form(...)
):
    print(f"Creando usuario: {username} con teléfono {telefono}")
    token = get_token()
    if not token:
        return {"error": "No se pudo obtener el token"}

    # ✅ Guardar teléfono para marketing futuro
    guardar_telefono(username, telefono)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "username": username,
        "password": password,
        "email": "",
        "firstname": "-",
        "login_Id": 2017,
        "site": "86240",
        "token": token,
        "proveedores": {
            "poker": {"comision": 0, "status": True},
            "casinolive": {"comision": 0, "status": True}
        }
    }

    try:
        res = requests.post("https://admin.flowbets.co/api/player/create", json=payload, headers=headers)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {
            "error": "Error en la creación",
            "detalle": str(e),
            "response": res.text if 'res' in locals() else "No hay respuesta"
        }
