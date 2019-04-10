from client import TokensClient

SERVER_URL = 'https://api.tokens.net'
API_KEY = 'xxx'
API_SECRET = 'xxx'

client = TokensClient(API_KEY, API_SECRET, api_end_point=SERVER_URL)

print('Trading pairs:')
trading_pairs = client.get_trading_pairs()
for trading_pair_slug, trading_pair_data in trading_pairs.items():
    print('{}: {}'.format(trading_pair_slug, trading_pair_data.get('title')))

print('Open orders:')
open_orders = client.get_open_orders('dtrbtc').get('openOrders', [])
for open_order in open_orders:
    print('Id: {}, Price: {}, Amount: {}'
          .format(open_order.get('id'), open_order.get('price'), open_order.get('amount')))
