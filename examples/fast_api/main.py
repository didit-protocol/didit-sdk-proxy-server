from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

import base64
import os
import requests

app = FastAPI()
# Configure CORS
origins = ['*']
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post('/wallet_authorization')
async def wallet_authorization(
    scope: Optional[str] = Form(None),
    wallet_address: str = Form(...),
    claims: Optional[str] = Form(None)
):
    auth = base64.b64encode(f"{os.environ['CLIENT_ID']}:{os.environ['CLIENT_SECRET']}".encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth}',
    }

    data = {
        'grant_type': 'https://gamium.world/oauth/grant_types/connectwallet',
        'scope': scope,
        'wallet_address': wallet_address,
        'claims': claims
    }

    response = requests.post(f"{os.environ['API_URL']}wallet_authorization/", json=data, headers=headers)

    response.raise_for_status()

    return response.json()

@app.post('/token')
async def token(
    code: str = Form(...),
    wallet_signature: str = Form(...)
):
    auth = base64.b64encode(f"{os.environ['CLIENT_ID']}:{os.environ['CLIENT_SECRET']}".encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth}',
    }

    data = {
        'code': code,
        'wallet_signature': wallet_signature,
        'grant_type': 'https://gamium.world/oauth/grant_types/connectwallet',
    }

    response = requests.post(f"{os.environ['API_URL']}token/", json=data, headers=headers)

    response.raise_for_status()

    return response.json()