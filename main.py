# BACKEND (main.py con FastAPI)
# Este es el backend que debe estar ya funcionando en Railway, lo dejamos final listo

from fastapi import FastAPI, Form, UploadFile, File
import requests
import csv
import os
import shutil
from fastapi.responses import JSONResponse

app = FastAPI()

USERNAME = "rosario"
PASSWORD = "luciano151418"
CLIENT_ID = "1_5i50wo24kpcscc0okw0ww4gsc8kwg0k8gs0ok44skooww4swcg"
CLIENT_SECRET = "18qxs6584gw08scg8wsk8gow44oc4gcw40c4o8w44880g0gkcg"
LOGIN_ID = 2017
SITE_ID = "86240"

TELEFONOS_CSV = "telefonos.csv"
COMPROBANTES_CSV = "comprobantes.csv"
COMPROBANTES_DIR = "comprobantes"
os.makedirs(COMPROBANTES_DIR, exist_ok=True)

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
    existe = os.path.exists(TELEFONOS_CSV)
    with open(TELEFONOS_CSV, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["username", "telefono"])
        writer.writerow([username, telefono])

def comprobar_comprobante_usado(nombre_archivo):
    if not os.path.exists(COMPROBANTES_CSV):
        return False
    with open(COMPROBANTES_CSV, mode="r") as f:
        reader = csv.reader(f)
        for fila in reader:
            if nombre_archivo in fila:
                return True
    return False

def guardar_comprobante(username, nombre_archivo):
    existe = os.path.exists(COMPROBANTES_CSV)
    with open(COMPROBANTES_CSV, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["username", "comprobante"])
        writer.writerow([username, nombre_archivo])

@app.post("/crear_usuario")
def crear_usuario(
    username: str = Form(...),
    password: str = Form(...),
    telefono: str = Form("")
):
    token = get_token()
    if not token:
        return {"success": False, "message": "No se pudo obtener el token."}

    guardar_telefono(username, telefono)

    headers = {
        "origin": "https://panel-skin2.jcasino.live",
        "referer": "https://panel-skin2.jcasino.live/",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "content-type": "application/json"
    }

    payload = {
        "username": username,
        "email": "",
        "firstname": "-",
        "password": password,
        "phone": telefono,
        "login_Id": LOGIN_ID,
        "site": SITE_ID,
        "token": token,
        "proveedores": {
            "poker": {"comision": 0, "status": True},
            "casinolive": {"comision": 0, "status": True}
        }
    }

    try:
        res = requests.post("https://local-admin.flowbets.co/crear_jugador", json=payload, headers=headers)
        res.raise_for_status()
        return {"success": True, "message": "Usuario creado con éxito"}
    except requests.HTTPError:
        if res.status_code == 400 and "ya existe" in res.text.lower():
            return {"success": False, "message": "El nombre de usuario ya existe. Por favor intente con otro!"}
        return {
            "success": False,
            "message": "Error en la creación del usuario",
            "detalle": res.text
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error inesperado",
            "detalle": str(e)
        }

@app.post("/cargar")
def cargar_fichas(
    username: str = Form(...),
    monto: int = Form(...),
    comprobante: UploadFile = File(...)
):
    if monto < 1000:
        return JSONResponse(status_code=400, content={"success": False, "message": "El monto mínimo es de $1.000."})

    filename = comprobante.filename
    if comprobar_comprobante_usado(filename):
        return JSONResponse(status_code=400, content={"success": False, "message": "Este comprobante ya fue usado."})

    ruta_archivo = os.path.join(COMPROBANTES_DIR, filename)
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(comprobante.file, buffer)

    guardar_comprobante(username, filename)

    return {"success": True, "message": "Fichas cargadas exitosamente"}
