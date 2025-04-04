from datetime import datetime as dt
from fastapi import Depends, HTTPException, status
from fastapi.security import (APIKeyHeader,
                              HTTPBearer,
                              HTTPAuthorizationCredentials)
from core.settings import Settings
from services.token import is_token_revoked
from jose import jwt, JWTError
import requests

settings = Settings()

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)
auth_header = HTTPBearer()


def verify_api_key(auth_header: str = Depends(api_key_header)):
    if auth_header != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized"
        )


def verify_token(cred: HTTPAuthorizationCredentials
                 = Depends(auth_header)) -> dict:
    token = cred.credentials

    # エミュレータ有無でトークン検証を切り替え
    verify = (verify_unsigned_token
              if settings.firebase_emulator_host else verify_signed_token)
    # print(f"verify_token(): trying with {verify}")
    claims = verify(token=token)
    if is_token_revoked(uid=claims["sub"], issued_at=claims["iat"]):
        raise HTTPException(status_code=401, detail="Token has been revoked")
    return claims


# トークン検証：トークンの有効期限のみを検査する(FirebaseEmulator用)
def verify_unsigned_token(token: str):
    try:
        claims = jwt.get_unverified_claims(token)
        if "sub" not in claims:
            raise ValueError("Missing 'sub' claim")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token")
    if int(dt.now().timestamp()) > claims["exp"]:
        raise HTTPException(status_code=401, detail="Expired token")
    return claims


# トークン検証：本番側FireBaseAuthから公開鍵を取得しトークンを検出する
def verify_signed_token(token):
    config = settings.get_firebase_auth_config()
    try:
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        if not kid:
            raise HTTPException(
                status_code=401, detail="Missing 'kid' in token header")

        # 公開鍵群を取得（キャッシュ推奨）
        res = requests.get(config["certs_url"])
        if res.status_code != 200:
            raise HTTPException(
                status_code=500, detail="Failed to fetch Firebase certs")
        certs = res.json()

        # 該当する公開鍵を探す
        x509_key = certs.get(kid)
        if not x509_key:
            raise HTTPException(
                status_code=401, detail="Matching public key not found")

        # 公開鍵を使ってトークン検証
        claims = jwt.decode(
            token,
            x509_key,
            algorithms=[config["algorithm"]],
            audience=config["audience"],
            issuer=config["issuer"]
        )

        # 有効期限を検証
        if int(dt.now().timestamp()) > claims["exp"]:
            raise HTTPException(status_code=401, detail="Expired token")

        return claims  # {sub: UID, email: ..., etc}

    except JWTError as e:
        raise HTTPException(
            status_code=401, detail=f"Token verification failed: {str(e)}")
