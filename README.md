# tokens-client-python
Python library for Tokens.net

## Quick usage example

```
from client import TokensClient

API_KEY = 'YOURKEYXXX'
API_SECRET = 'YOURSECRETXXX'

client = TokensClient(API_KEY, API_SECRET)

trading_pairs = client.get_trading_pairs()

for trading_pair in trading_pairs:
    print(trading_pair)
```
