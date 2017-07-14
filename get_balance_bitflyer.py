# coding: utf-8

"""
Acquire balance information from bitflyer.
------------------------------------------

* About the api:
 * https://lightning.bitflyer.jp/docs

"""

import os.path
import time
import hmac
import hashlib
import json
import requests


SERVER='api.bitflyer.jp'

# JSON file: Includes api key and api secret.
#
# {
#     "api_key": "[API_KEY]",
#     "api_secret": "[API_SECRET]"
# }
CREDENTIAL_FILE = os.path.join(os.path.dirname(__file__),
                               "bitflyer.credential.json")


def main():
    credential = json.load(open(CREDENTIAL_FILE, "r"))
    api_key = credential['api_key']
    api_secret = credential['api_secret']

    timestamp = str(time.time())
    path = '/v1/me/getbalance'
    method = 'GET'

    message = timestamp + method + path
    access_sign = hmac.new(api_secret.encode('ascii'),
                           message.encode('ascii'),
                           hashlib.sha256).hexdigest()

    url = 'https://' + SERVER + path
    headers = {
        'ACCESS-KEY': api_key,
        'ACCESS-TIMESTAMP': timestamp,
        'ACCESS-SIGN': access_sign,
        'Content-Type': 'application/json',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    print(json.dumps(r.json(), indent=4))


if __name__ == '__main__':
    main()
