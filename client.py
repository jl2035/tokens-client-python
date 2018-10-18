import json, time, hmac, hashlib
from urllib import request, parse


class TokensClient:

    def __init__(self, api_key, api_secret, url = 'https://api.tokens.net'):
        self.server_url = url
        self.api_key = api_key
        self.api_secret = api_secret

    def get_nonce(self):
        return int(time.time() * 10**7)

    def get_signature(self, nonce):
        return hmac.new(self.api_secret.encode('utf8'), '{}{}'.format(nonce, self.api_key).encode('utf8'), hashlib.sha256).hexdigest().upper()

    def api_request(self, method, data = None):
        req = request.Request(self.server_url + method)

        if data is not None:
            data = parse.urlencode(data).encode("utf-8")

        if method.startswith('/private/'):
            nonce = self.get_nonce()
            signature = self.get_signature(nonce)
            req.add_header('KEY', self.api_key)
            req.add_header('NONCE', nonce)
            req.add_header('SIGNATURE', signature)

        resp = request.urlopen(req, data)
        content = resp.read().decode('utf-8')

        return json.loads(content)

    def get_trading_pairs(self):
        method = '/public/trading-pairs/get/all/'

        return self.api_request(method)

    def get_ticker(self, trading_pair):
        method = '/public/ticker/%s/' % trading_pair

        return self.api_request(method)

    def get_hourly_ticker(self, trading_pair):
        method = '/public/ticker/hour/%s/' % trading_pair

        return self.api_request(method)

    def get_balance(self, currency):
        method = '/private/balance/%s/' % currency

        data = self.api_request(method)

        if data['status'] == 'error':
            raise Exception(data['reason'])

        return {'total' : data['total'],
                'available' : data['available'],
                'currency': data['currency']}

    def get_order(self, order_id):
        method = '/private/orders/get/%s/' % order_id

        data = self.api_request(method)

        if data['status'] == 'error':
            raise Exception(data['reason'])

        return data

    def cancel_all_orders(self, trading_pair=None):
        open_orders = self.get_open_orders(trading_pair)

        for order in open_orders:
            self.cancel_order(order['id'])

        return True

    def get_open_orders(self, trading_pair=None):
        if trading_pair == None:
            method = '/private/orders/get/all/'
        else:
            method = '/private/orders/get/%s/' % trading_pair

        data = self.api_request(method)

        if data['status'] == 'error':
            raise Exception(data['reason'])

        return data['openOrders']

    def get_order_book(self, trading_pair):
        method = '/public/order-book/%s/' % trading_pair

        data = self.api_request(method)

        return {'bids': data['bids'], 'asks': data['asks'], 'timestamp': data['timestamp']}

    def new_limit_order(self, trading_pair, side, amount, price, take_profit=None, expire_date=None):
        method = '/private/orders/add/limit/'

        data = {'tradingPair': trading_pair, 'side': side, 'amount': amount, 'price': price}

        if take_profit:
            data['takeProfit'] = take_profit
        if expire_date:
            data['expireDate'] = expire_date

        data = self.api_request(method, data)

        if data['status'] == 'error':
            raise Exception(data['reason'])

        return data['orderId']

    def cancel_order(self, order_id):
        method = '/private/orders/cancel/%s/' % order_id

        return self.api_request(method, '')

    # time frames available: 'minute', 'hour', 'day'
    def trades(self, trading_pair, timeframe):
        method = '/public/trades/%s/%s/' % timeframe, trading_pair

        return self.api_request(method)
