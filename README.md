# How to generate API key and secret?

- Log in to the tokens.net platform.
- Click “settings” in top menu and then click on the “API Access” tab.
- Use the drop down menu to select for which account you want to generate API key and then click on the “Generate new API key” button.
- New API key and secret will be generated. They will only be displayed for a short amount of time so make sure to copy them to a secure place and then click on the “Got it” button when you are done.
- You will receive a confirmation email from tokens.net. You have to click on the confirmation link to confirm your API key before you can start using it.

*For additional security we recommend locking your API keys to specific IP address or range and to disable or delete your API keys once you are done using them.*


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
