import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
import os
from dotenv import load_dotenv

load_dotenv()

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key=None, secret_key=None, passphrase=None):
        self.api_key = api_key if api_key else os.getenv('COINBASE_CLIENT_ID')
        self.secret_key = secret_key if secret_key else os.getenv('COINBASE_CLIENT_SECRET')
        self.passphrase = passphrase if passphrase else os.getenv('COINBASE_CLIENT_PASSPHRASE')

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.pro.coinbase.com/'
auth = CoinbaseExchangeAuth()

# Get accounts
response = requests.get(api_url + 'accounts', auth=auth)
# print(json.dumps(response.json(),sort_keys=True,indent=4,default=str))

accounts = []

for account in response.json():
    if float(account['balance']) != 0.0000000000000000:
        accounts.append(account)

print(json.dumps(accounts,sort_keys=True,indent=4,default=str))

