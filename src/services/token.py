from google.cloud import firestore
import hashlib
from datetime import datetime
from core.settings import Settings
import requests, json

settings = Settings()

db = firestore.Client()

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def store_refresh_token(uid: str, token: str, environment: str):
    doc_id = hash_token(token)
    doc_ref = db.collection(settings.refresh_token_store).document(doc_id)
    doc_ref.set({
        "uid": uid,
        "environment": environment,
        "created_at": datetime.utcnow()
    })

def lookup_refresh_token(token: str):
    doc_id = hash_token(token)
    doc_ref = db.collection(settings.refresh_token_store).document(doc_id)
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
    try:
        res = requests.post(url, data=data,headers={"Content-Type": "application/x-www-form-urlencoded"})
        if res.status_code != 200:
            raise Exception("Refresh failed")
    except Exception as e:
        print(e)
        raise e

    return res.json()


def revoke_token(uid: str):
    doc_ref = db.collection(settings.revoked_token_store).document(uid)
    doc_ref.set({
        "revoked_at": datetime.utcnow()
    }, merge=True)


def is_token_revoked(uid:str, issued_at:int) -> bool:
    doc = db.collection(settings.revoked_token_store).document(uid).get()
    if not doc.exists:
        return False

    data = doc.to_dict()
    revoked_at = data.get("revoked_at")
    if not revoked_at:
        return False

    # issued_at は秒単位、revoked_atはdatetimeなので変換
    revoked_timestamp = revoked_at.timestamp()

    return issued_at < int(revoked_timestamp)
