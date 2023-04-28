from dotenv import load_dotenv
load_dotenv()

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import base64
import os
import requests

@api_view(['POST'])
def wallet_authorization(request):
    wallet_address = request.data.get('wallet_address')
    scope = os.environ['SCOPE']
    claims = os.environ['CLAIMS']

    if not wallet_address:
        return Response({'detail': 'wallet_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    auth = base64.b64encode(f"{os.environ['CLIENT_ID']}:{os.environ['CLIENT_SECRET']}".encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth}',
    }

    data = {
        'scope': scope,
        'wallet_address': wallet_address,
        'claims': claims
    }

    response = requests.post(f"{os.environ['API_URL']}wallet_authorization/", json=data, headers=headers)
    return Response(response.json(), status=response.status_code)

@api_view(['POST'])
def token(request):
    code = request.data.get('code')
    wallet_signature = request.data.get('wallet_signature')

    if not code or not wallet_signature:
        return Response({'detail': 'code and wallet_signature are required'}, status=status.HTTP_400_BAD_REQUEST)

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
    return Response(response.json(), status=response.status_code)