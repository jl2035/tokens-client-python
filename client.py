import json, time, hmac, hashlib
from urllib import request, parse


class TokensClient:
    API_END_POINT = 'https://api.tokens.net'

    TIME_FRAME_HOUR = 1
    TIME_FRAME_DAY = 2
    TIME_FRAMES = (
        (TIME_FRAME_HOUR, 'hour'),
        (TIME_FRAME_DAY, 'day'),
    )

    def __init__(self, api_key, api_secret, api_end_point=API_END_POINT):
        self.end_point = api_end_point
        self.api_key = api_key
        self.api_secret = api_secret

    @staticmethod
    def get_nonce():
        return int(time.time() * 10**7)

    def get_signature(self, nonce):
        return hmac.new(
            self.api_secret.encode('utf8'),
            '{}{}'.format(nonce, self.api_key).encode('utf8'),
            hashlib.sha256
        ).hexdigest().upper()

    def api_request(self, method, data=None):
        http_request = request.Request(self.end_point + method)

        if data is not None:
            data = parse.urlencode(data).encode('utf-8')

        if method.startswith('/private/'):
            nonce = TokensClient.get_nonce()
            signature = self.get_signature(nonce)
            http_request.add_header('KEY', self.api_key)
            http_request.add_header('NONCE', nonce)
            http_request.add_header('SIGNATURE', signature)

        http_response = request.urlopen(http_request, data)
        content = http_response.read().decode('utf-8')
        content = json.loads(content)

        if content.get('status') == 'error':
            raise Exception(content.get('reason', 'Api_request error occurred'))

        return content

    # Public API calls
    def get_currencies(self):
        method = '/public/currency/all/'

        return self.api_request(method)

    def get_trading_pairs(self):
        method = '/public/trading-pairs/get/all/'

        return self.api_request(method)

    def get_ticker(self, trading_pair):
        method = '/public/ticker/{}/'.format(trading_pair)

        return self.api_request(method)

    def get_ticker_all(self):
        return self.get_ticker('all')

    def get_hourly_ticker(self, trading_pair):
        method = '/public/ticker/hour/{}/'.format(trading_pair)

        return self.api_request(method)

    def get_hourly_ticker_all(self):
        return self.get_hourly_ticker('all')

    def get_order_book(self, trading_pair):
        method = '/public/order-book/{}/'.format(trading_pair)

        return self.api_request(method)

    def trades(self, trading_pair, time_frame):
        if time_frame not in dict(self.TIME_FRAMES):
            raise Exception('Invalid time frame {}'.format(time_frame))

        method = '/public/trades/{}/{}/'.format(dict(self.TIME_FRAMES).get(time_frame), trading_pair)

        return self.api_request(method)

    def get_voting_list(self):
        method = '/public/voting/get/all/'

        return self.api_request(method)

    # Private API calls
    def get_balance(self, currency):
        method = '/private/balance/{}/'.format(currency)

        return self.api_request(method)

    def get_balance_all(self):
        method = '/private/balance/all/'

        return self.api_request(method)

    def get_order(self, order_id):
        method = '/private/orders/get/{}/'.format(order_id)

        return self.api_request(method)

    def cancel_order_all(self, trading_pair=None):
        open_orders = self.get_open_orders(trading_pair)

        for order in open_orders:
            self.cancel_order(order['id'])

        return True

    def get_open_orders(self, trading_pair=None):
        if trading_pair is None:
            method = '/private/orders/get/all/'
        else:
            method = '/private/orders/get/{}/'.format(trading_pair)

        return self.api_request(method)

    def new_limit_order(self, trading_pair, side, amount, price, take_profit=None, expire_date=None):
        method = '/private/orders/add/limit/'

        data = {
            'tradingPair': trading_pair,
            'side': side,
            'amount': amount,
            'price': price,
        }

        if take_profit:
            data['takeProfit'] = take_profit
        if expire_date:
            data['expireDate'] = expire_date

        return self.api_request(method, data)

    def cancel_order(self, order_id):
        method = '/private/orders/cancel/{}/'.format(order_id)

        return self.api_request(method, '')

    def get_trades(self, trading_pair, page):
        method = '/private/trades/{}/{}/'.format(trading_pair, page)

        return self.api_request(method)

    def get_trades_all(self, page):
        return self.get_trades('all', page)

    def get_transactions(self, page):
        method = '/private/transactions/{}'.format(page)

        return self.api_request(method)
