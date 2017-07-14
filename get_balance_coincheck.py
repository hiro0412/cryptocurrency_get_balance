# coding: utf-8

"""
Acquire balance information from coincheck.
-------------------------------------------

* About the api:
 * https://coincheck.com/ja/documents/exchange/api

"""

import os.path
import time
import hmac
import hashlib
import json
import requests


SERVER='coincheck.com'

# JSON file: Includes api key and api secret.
# 
# {
#     "api_key": "[API_KEY]",
#     "api_secret": "[API_SECRET]"
# }
CREDENTIAL_FILE = os.path.join(os.path.dirname(__file__),
                               "coincheck.credential.json")


def main():
    credential = json.load(open(CREDENTIAL_FILE, "r"))
    api_key = credential['api_key']
    api_secret = credential['api_secret']

    nonce = str(int(time.time() * 1000000))
    path = '/api/accounts/balance'
    method = 'GET'

    url = 'https://' + SERVER + path

    message = nonce + url
    access_sign = hmac.new(API_SECRET.encode('ascii'),
                           message.encode('ascii'),
                           hashlib.sha256).hexdigest()

    headers = {
        'ACCESS-KEY': api_key,
        'ACCESS-NONCE': nonce,
        'ACCESS-SIGNATURE': access_sign,
        'Content-Type': 'application/json',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    print(json.dumps(r.json(), indent=4))


if __name__ == '__main__':
    main()
