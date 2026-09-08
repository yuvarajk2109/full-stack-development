#!/usr/bin/env python3
"""
Generate an HS256 JWT without external deps.
Reads secret from env `JWT_SHARED_SECRET` or falls back to the repo default.
Usage:
  python scripts/generate_jwt.py --sub alice --roles MISSION_OPERATOR
"""
import os
import sys
import json
import time
import hmac
import hashlib
import base64
import argparse

DEFAULT_SECRET = "mission-control-shared-secret-key-32-bytes-minimum"

def b64url(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data).rstrip(b"=")

def make_jwt(secret: str, sub: str, roles, expiry_seconds: int):
    header = {"alg": "HS256", "typ": "JWT"}
    iat = int(time.time())
    payload = {"sub": sub, "iat": iat, "exp": iat + expiry_seconds, "roles": roles}

    header_b = b64url(json.dumps(header, separators=(",",":")).encode())
    payload_b = b64url(json.dumps(payload, separators=(",",":")).encode())
    signing_input = header_b + b"." + payload_b

    sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    sig_b = b64url(sig)

    return (signing_input + b"." + sig_b).decode()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--sub", default="alice", help="subject (sub) claim")
    p.add_argument("--roles", default="MISSION_OPERATOR", help="comma-separated roles")
    p.add_argument("--exp", type=int, default=3600, help="expiry in seconds (default 3600)")
    p.add_argument("--secret", help="override shared secret (otherwise use env JWT_SHARED_SECRET or repo default)")
    args = p.parse_args()

    secret = args.secret or os.environ.get("JWT_SHARED_SECRET") or DEFAULT_SECRET
    roles = [r.strip() for r in args.roles.split(",") if r.strip()]

    token = make_jwt(secret, args.sub, roles, args.exp)
    print(token)
