import base64
import hmac
import time
import requests
import requests.auth
import settings
from keys import BUDA
from exchange import Exchange


class BudaHMACAuth(requests.auth.AuthBase):
    """Adjunta la autenticación HMAC de Buda al objeto Request."""

    def __init__(self, api_key: str, secret: str):
        self.api_key = api_key
        self.secret = secret

    def get_nonce(self) -> str:
        # 1. Generar un nonce (timestamp en microsegundos)
        return str(int(time.time() * 1e6))

    def sign(self, r, nonce: str) -> str:
        # 2. Preparar string para firmar
        components = [r.method, r.path_url]
        if r.body:
            encoded_body = base64.b64encode(r.body).decode()
            components.append(encoded_body)
        components.append(nonce)
        msg = ' '.join(components)
        # 3. Obtener la firma
        h = hmac.new(key=self.secret.encode(),
                        msg=msg.encode(),
                        digestmod='sha384')
        signature = h.hexdigest()
        return signature

    def __call__(self, r):
        nonce = self.get_nonce()
        signature = self.sign(r, nonce)
        # 4. Adjuntar API-KEY, nonce y firma al header del request
        r.headers['X-SBTC-APIKEY'] = self.api_key
        r.headers['X-SBTC-NONCE'] = nonce
        r.headers['X-SBTC-SIGNATURE'] = signature
        return r

class Buda(Exchange):

    def __init__(self):
        Exchange.__init__(self, "buda", BUDA['key'], BUDA['secret'])
        self.auth = BudaHMACAuth(self.key, self.secret)

    def get_balances(self):
        url = f'https://www.buda.com/api/v2/balances'
        response = requests.get(url, auth=self.auth)
        res = response.json()
        balances = {}
        for b in res['balances']:
            if b['id'] in settings.TICKERS:
                balances[b['id']] = float(b['available_amount'][0])
        return balances

    def get_ticker(self, ticker):
        url = f"https://www.buda.com/api/v2/markets/{ticker}/ticker"
        response = requests.get(url, auth=self.auth)
        res = response.json()
        return res

    def get_order_book(self, ticker, n=None):
        url = f"https://www.buda.com/api/v2/markets/{ticker}/order_book"
        response = requests.get(url, auth=self.auth)
        res = response.json()
        order_book = {}
        order_book['bids'] = res['order_book']['bids'][:n]
        order_book['asks'] = res['order_book']['asks'][:n]
        for order_type in order_book:
            formatted_values = []
            for order in order_book[order_type]:
                formatted_values.append([float(x) for x in order])
            order_book[order_type] = formatted_values
        return {'bids': [[0.005057, 1]], 'asks': [[0.0051, 1]]}
        return order_book

    def make_buy_order(self, ticker, price, size):
        print('Placing Buy order in Buda')
        url = f"https://www.buda.com/api/v2/markets/{ticker}/orders"
        response = requests.post(url, auth=self.auth, json={
            'type': 'Bid',
            'price_type': 'limit',
            'limit': price,
            'amount': size,
        })
        res = response.json()
        print(res)

    def make_sell_order(self, ticker, price, size):
        print('Placing sell order in Buda')
        url = f"https://www.buda.com/api/v2/markets/{ticker}/orders"
        response = requests.post(url, auth=self.auth, json={
            'type': 'Ask',
            'price_type': 'limit',
            'limit': price,
            'amount': size,
        })
        res = response.json()
        print(res)
