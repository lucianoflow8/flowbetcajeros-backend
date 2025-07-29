from fastapi import FastAPI, Form
import requests
import csv
import os
from datetime import datetime

app = FastAPI()

# 🔁 DATOS DEL CAJERO – CAMBIAR ESTO PARA CADA PANEL
USERNAME = "rosario"
PASSWORD = "luciano151418"
CLIENT_ID = "1_5i50wo24kpcscc0okw0ww4gsc8kwg0k8gs0ok44skooww4swcg"
CLIENT_SECRET = "18qxs6584gw08scg8wsk8gow44oc4gcw40c4o8w44880g0gkcg"
NOMBRE_CAJERO = "rosario"  # Nombre usado para guardar archivo único por cajero

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
    archivo = f"{NOMBRE_CAJERO}_telefonos.csv"
    existe = os.path.isfile(archivo)
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(archivo, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["username", "telefono", "fecha_hora"])
        writer.writerow([username, telefono, fecha_hora])

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

    guardar_telefono(username, telefono)  # ✅ Guarda también la hora

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
