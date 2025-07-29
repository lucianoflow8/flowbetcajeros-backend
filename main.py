from fastapi import FastAPI, Form
import requests

app = FastAPI()

# Credenciales
USERNAME = "rosario"
PASSWORD = "luciano151418"
CLIENT_ID = "1_5i50wo24kpcscc0okw0ww4gsc8kwg0k8gs0ok44skooww4swcg"
CLIENT_SECRET = "18qxs6584gw08scg8wsk8gow44oc4gcw40c4o8w44880g0gkcg"
LOGIN_ID = 2017  # Este es tu ID como cajero
SITE_ID = "86240"

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

@app.post("/crear_usuario")
def crear_usuario(username: str = Form(...), password: str = Form(...)):
    token = get_token()
    if not token:
        return {"error": "No se pudo obtener el token."}

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
        "phone": "",
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
        return res.json()
    except Exception as e:
        return {
            "error": "Error en la creación",
            "detalle": str(e),
            "response": res.text if 'res' in locals() else "No hay respuesta"
        }
