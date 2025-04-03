from google.cloud import firestore
import hashlib
from datetime import datetime
from core.settings import Settings
import requests

settings = Settings()

db = firestore.Client()

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def store_refresh_token(uid: str, token: str, environment: str):
    doc_id = hash_token(token)
    doc_ref = db.collection("refresh_tokens").document(doc_id)
    doc_ref.set({
        "uid": uid,
        "environment": environment,
        "created_at": datetime.utcnow()
    })

def lookup_refresh_token(token: str):
    doc_id = hash_token(token)
    doc_ref = db.collection("refresh_tokens").document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

def refresh_token_with_env(token: str, environment: str):
    config = settings.get_firestore_config(environment=environment)
    if not config:
        raise ValueError(f"Invalid environment: {environment}")

    url = f"{config['refresh_url']}?key={config['api_key']}"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token
    }

    res = requests.post(url, data=data)
    if res.status_code != 200:
        raise Exception("Refresh failed")

    return res.json()