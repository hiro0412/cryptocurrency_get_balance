# coding: utf-8

"""
Acquire balance information from zaif.jp.
-----------------------------------------

* About the api:
 * http://techbureau-api-document.readthedocs.io

"""

import os.path
import time
import hmac
import hashlib
import urllib.parse
import json
import requests


SERVER = 'api.zaif.jp'
ENDPOINT = 'https://{}/tapi'.format(SERVER)

# JSON file: Includes api key and api secret.
# 
# {
#     "api_key": "[API_KEY]",
#     "api_secret": "[API_SECRET]"
# }
CREDENTIAL_FILE = os.path.join(os.path.dirname(__file__),
                               "zaif.credential.json")


def main():
    credential = json.load(open(CREDENTIAL_FILE, "r"))
    api_key = credential['api_key']
    api_secret = credential['api_secret']
    
    nonce = time.time()
    params = {'method': 'get_info2', 'nonce': nonce}
    message = urllib.parse.urlencode(params)
    signature = hmac.new(bytearray(api_secret.encode('ascii')),
                         digestmod=hashlib.sha512)
    signature.update(message.encode('ascii'))

    headers = {
        'key': api_key,
        'sign': signature.hexdigest(),
    }
    r = requests.post(ENDPOINT, data=message, headers=headers)
    r.raise_for_status()

    print(json.dumps(r.json(), indent=4))


if __name__ == '__main__':
    main()
