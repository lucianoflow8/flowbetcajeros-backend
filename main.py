from fastapi import FastAPI, Form
import requests

app = FastAPI()

USERNAME = "rosario"
PASSWORD = "luciano151418"

def get_token():
    session = requests.Session()

    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "client_id": "1_5i80w2o4kpcssc0okw0ww4gsc8kwg8k8gs0ok44skooww4swc8",
        "client_secret": "18qxs6584g8w085cg8wsk8gow440c4gcw4c40w44880g8gkcg",
        "grant_type": "password",
        "source": "pn"
    }

    token_url = "https://admin.flowbets.co/oauth/v2/token"
    response = session.post(token_url, data=data)

    if response.status_code != 200:
        print("Login error:", response.text)
        return None

    tokens = response.json()
    return tokens.get("access_token")

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
