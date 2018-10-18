import decimal
from client import TokensClient

API_KEY = 'YOURKEYXXX'
API_SECRET = 'YOURSECRETXXX'

TRADING_PAIR = 'dtrusdt'

client = TokensClient(API_KEY, API_SECRET)

print ('***********************************')
print ('AVAILABLE TRADING PAIRS')
trading_pairs = client.get_trading_pairs()
for trading_pair in trading_pairs:
    print (trading_pair)

print ('***********************************')
print ('TICKERS FOR ALL TRADING PAIRS')
for trading_pair in trading_pairs:
    ticker = client.get_ticker(trading_pair['name'])
    print (ticker)

print ('***********************************')
print ('HOURLY TICKERS FOR ALL PAIRS')
for trading_pair in trading_pairs:
    ticker = client.get_hourly_ticker(trading_pair['name'])
    print (ticker)

print ('***********************************')
print ('AVAILABLE BALANCES')
for currency in ['dtr', 'btc', 'usdt', 'eth']:
    balance = client.get_balance(currency)
    print(balance)

print ('***********************************')
print ('%s ORDER BOOK' % TRADING_PAIR.upper())
order_book = client.get_order_book(TRADING_PAIR)
for x in range(0, 5):
    try:
        print ('%s - %s | %s - %s' % (order_book['bids'][x][0], order_book['bids'][x][1], order_book['asks'][x][0], order_book['asks'][x][1]))
    except:
        continue

# Create one buy order and one sell order
buy_order = client.new_limit_order(TRADING_PAIR, 'buy', decimal.Decimal('100'), decimal.Decimal('0.10'))
sell_order = client.new_limit_order(TRADING_PAIR, 'sell', decimal.Decimal('100'), decimal.Decimal('0.11'))

# Display currently open orders
print ('***********************************')
print ('OPEN ORDERS')
open_orders = client.get_open_orders()
for order in open_orders:
    print (order)

# Cancel orders created above
client.cancel_order(buy_order)
client.cancel_order(sell_order)

client.cancel_all_orders()
