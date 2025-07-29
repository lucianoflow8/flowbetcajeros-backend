from fastapi import FastAPI, Form
import requests

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

@app.post("/crear_usuario")
def crear_usuario(username: str = Form(...), password: str = Form(...)):
    print(f"Creando usuario: {username}")
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
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Error al crear usuario:", e)
        return {
            "error": "Error en la creación",
            "detalle": str(e),
            "response": res.text if 'res' in locals() else "No hay respuesta"
        }
