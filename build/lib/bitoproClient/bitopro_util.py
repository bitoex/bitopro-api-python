# -*- coding: utf-8 -*-
import json
import hmac
import hashlib
import base64
import time

def get_current_timestamp() -> int:
        return int(time.time() * 1000)


def build_payload(params:dict) -> bytes:
    return base64.urlsafe_b64encode(json.dumps(params).encode("utf-8")).decode("utf-8")


def build_headers(api_key:str, api_secret:str, params={}) -> dict:
    signature = hmac.new(bytes(api_secret, "utf-8"), bytes(build_payload(params), "utf-8"), hashlib.sha384,).hexdigest()
    return {
        "X-BITOPRO-APIKEY": api_key,
        "X-BITOPRO-PAYLOAD": build_payload(params),
        "X-BITOPRO-SIGNATURE": signature,
    }
