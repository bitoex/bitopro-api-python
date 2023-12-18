# bitopro-api-python

SDK for the [BitoPro](https://www.bitopro.com/) API.

[Bitopro official API document](https://github.com/bitoex/bitopro-offical-api-docs)

## Installation

```bash
pip install bitopro-client
```

### Linux

```bash
cd ~/ && git clone https://github.com/bitoex/bitopro-api-python.git
cd ~/bitopro-api-python && cp bitopro/sample_test.py .

# update API key and secret
# vim sample_test.py

python3 sample_test.py
```

### Windows

```batch
cd %USERPROFILE%\Downloads
git clone https://github.com/bitoex/bitopro-api-python.git

cd bitopro-api-python
cd bitopro

# update API key and secret
# notepad sample_test.py

python3 sample_test.py
```

### Limitations

#### Rate Limit

There is rate limits applied to each API, please check [API documentation](https://github.com/bitoex/bitopro-offical-api-docs) for more detail.

#### Precisions

Both price and amount are subject to decimal restrictions, please check [official settings](https://www.bitopro.com/fees) for more detail.

#### Minimum order amount

Checkout the [official settings](https://www.bitopro.com/fees) of minimum amount.

### Getting started

#### Please go to [BitoPro Official Website](https://www.bitopro.com/) to create an API key

![api apply](api%20apply.png)

#### We use the official [bitopro-api-python](https://github.com/bitoex/bitopro-api-python) package

```python
from bitoproClient.bitopro_restful_client import BitoproRestfulClient
from bitoproClient.bitopro_util import get_current_timestamp

account = ''  # Fill in your BitoPro account (email) here
apiKey = ''
apiSecret = ''
# Create and initialize an instance of BitoproRestfulClient
bitopro_client = BitoproRestfulClient(apiKey, apiSecret)
```

**Note:**
public: Public API, does ==not need== an API KEY.
private: Private API, does ==require== an API KEY.

### Public restful enpoint example

#### Query order book prices (highest bid price, lowest ask price)

Please refer to [Get Orderbook](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/public/get_orderbook_data.md)

```pythonc
# Set trading pair to btc_usdt
pair = "btc_usdt" 
# We retrieve the first level bid and ask from the order book
orderbook = bitopro_client.get_order_book(pair=pair, limit=1, scale=0)
print(orderbook, '\n')

# Highest bid price
bid = float(orderbook['bids'][0]['price']) if len(orderbook['bids']) > 0 else None

# Lowest ask price
ask = float(orderbook['asks'][0]['price']) if len(orderbook['asks']) > 0 else None

# Spread
spread = (ask - bid) if (bid and ask) else None

# Mid price
mid = 0.5 * (bid + ask) if (bid and ask) else None

# Print market data
print(f"Highest bid price: {bid:.2f}, Lowest ask price: {ask:.2f}, Mid price: {mid:.2f}, Spread: {spread:.2f}")
```

#### Candlestick Data Retrieval

Please refer to [Get OHLC Data](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/public/get_ohlc_data.md)

```python
dt_string = '2023/01/01 00:00:00'
start_ts = int(datetime.strptime(dt_string, "%Y/%m/%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp())
end_ts = int(datetime.now(timezone.utc).timestamp())
response = bitopro_client.get_candlestick(pair, CandlestickResolution._1d, start_ts, end_ts)
print(response)
print(len(response['data'])) # Retrieve the number of candlesticks

# Here we use pandas and matplotlib
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(response['data'])
df["Datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
df.set_index("Datetime", inplace=True)
df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
print(df.dtypes)
print(df.tail())

# Plotting the closing price trend
df[['Close']].plot(figsize=(15, 8))
plt.show()
```

![candlestick](candlestick%20data.png)

#### Get Trading Pair Limitations

[Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/public/get_limitations_and_fees.md)

```python
def get_trading_limit(pair):
    base_precision, quote_precision, minLimit_base_amount = None, None, None
    r = bitopro_client.get_trading_pairs()  # get pairs status
    for i in r['data']:
        if i['pair'] == pair.lower():
            base_precision = i['basePrecision']  # Decimal places for Base Currency
            quote_precision = i['quotePrecision']  # Decimal places for Quoted Currency
            minLimit_base_amount = i['minLimitBaseAmount']  # Minimum order amount
            break
    return base_precision, quote_precision, minLimit_base_amount

r = get_trading_limit('btc_usdt')
print(r)
```

### Private restful enpoint example

#### Get balance (two methods)

##### The first method, using the API to query

[Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/get_account_balance.md)

```python
r = bitopro_client.get_account_balance()
print(r)
```

##### The second method, using websocket

[Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/ws/private/user_balance_stream.md)

```python
import time

account_balance_dict: dict = {}

def websocket_handler(message: str):
    global account_balance_dict
    response = json.loads(message)
    if response["event"] == "ACCOUNT_BALANCE":
        for _, curr in response['data'].items():
            account_balance_dict[curr['currency'].lower()] = {'amount': eval(curr['amount']), 'available': eval(curr['available'])}

bito_websocket_user_balance = bitopro_ws.BitoproUserBlanceWs(account, apiKey, apiSecret, websocket_handler)
bito_websocket_user_balance.init_websocket()
bito_websocket_user_balance.start()
time.sleep(2) # Rest a bit right after websocket starts, to wait for balance to be written into the variable.
print(account_balance_dict['btc']) # Query btc balance
print(account_balance_dict['eth']) # Query eth balance
print(account_balance_dict['usdt']) # Query usdt balance
```

#### Placing an order [Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/create_an_order.md)

```python
# Limit buy order
r = bitopro_client.create_an_order(pair='btc_usdt', action='buy', amount='0.0001', price='36000', type=OrderType.Limit)
print(r)

# Limit sell order
r = bitopro_client.create_an_order(pair='btc_usdt', action='sell', amount='0.0001', price='50000', type=OrderType.Limit)
print(r)
```

#### Batch Orders, up to 10 orders. [Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/create_batch_orders.md)

**Highly recommended!!**

```python
batch_orders: list = []
batch_orders.append(
    {
        **{'pair': 'BTC_USDT'},
        **{'action': 'BUY'},
        **{'amount': str(0.0001)},
        **({'price': str(38000)}),
        **{'timestamp': get_current_timestamp()},
        **{'type': 'LIMIT'},
        })
batch_orders.append(
    {
        **{'pair': 'BTC_USDT'},
        **{'action': 'BUY'},
        **{'amount': str(0.0001)},
        **({'price': str(38001)}),
        **{'timestamp': get_current_timestamp()},
        **{'type': 'LIMIT'},
        })
r = bitopro_client.create_batch_order(batch_orders)
print(r)
```

#### Query Unfilled Orders [Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/get_orders_data.md)

```python
r = bitopro_client.get_all_orders(pair='btc_usdt', status_kind=StatusKind.OPEN, ignoreTimeLimitEnable=True)
print(r)
```

#### Query Order by Order ID [Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/get_an_order_data.md)

```python
pair: str = "btc_usdt"
order_id: str = '1296613577'
r = bitopro_client.get_an_order(pair=pair, order_id=order_id)
print(r)
```

#### Batch Cancel Order [Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/cancel_batch_orders.md)

**Highly recommended!!**

```python
pair: str = 'BTC_USDT'
order_id_lst: list = ['7433602697', '2556744303']
batch_orders_dict: dict = {pair: order_id_lst}
r = bitopro_client.cancel_multiple_orders(batch_orders_dict)
print(r)
```

#### Cancel Order by Order ID [Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/cancel_an_order.md)

```python
pair: str = "btc_usdt"
order_id: str = '1296613577'
r = bitopro_client.cancel_an_order(pair=pair, order_id=order_id)
print(r)
```

#### Cancel All Orders [Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/cancel_all_orders.md)

```python
r = bitopro_client.cancel_all_orders('all')
print(r)
```

#### Cancel All Orders for a Specific Trading Pair [Please refer to](https://github.com/bitoex/bitopro-offical-api-docs/blob/master/api/v3/private/cancel_all_orders.md)

``` python
r = bitopro_client.cancel_all_orders('btc_usdt')
print(r)
```

#### A Simple Buy and Sell Strategy

```python
def strategy(base, quote):
    pair = f"{base.lower()}_{quote.lower()}"
    # Get trading pair limitations
    base_precision, quote_precision, min_limit_base_amount = get_trading_limit(pair)
    # Query balance
    r = bitopro_client.get_account_balance()
    bal_base, bal_quote = None, None
    for curr in r['data']:
        if curr['currency'] == base.lower():
            bal_base = eval(curr['amount'])
        if curr['currency'] == quote.lower():
            bal_quote = eval(curr['amount'])
        if bal_base is not None and bal_quote is not None:
            break
    print(f"Balance: {base}: {bal_base}, {quote}: {bal_quote}")
    orderbook = bitopro_client.get_order_book(pair=pair, limit=1, scale=0)
    # Highest buying price
    bid = float(orderbook['bids'][0]['price']) if len(orderbook['bids']) > 0 else None
    # Lowest selling price
    ask = float(orderbook['asks'][0]['price']) if len(orderbook['asks']) > 0 else None
    # Mid-price
    mid = 0.5 * (bid + ask) if (bid and ask) else None
    # Place an order, limit buy order (at mid-price)
    amount = round(0.0001, base_precision)
    price = round(mid, quote_precision)
    if float(amount) >= float(min_limit_base_amount):
        r = bitopro_client.create_an_order(pair=pair, action='buy', amount=str(amount), price=str(price), type=OrderType.Limit)
        print(r)
        # Or place a market order (take order)
        # price = round(ask, quote_precision)
        # r = bitopro_client.create_an_order(pair=pair, action='buy', amount=str(amount), price=str(price), type=OrderType.Limit)
        # print(r)
        order_id: str = r['orderId']
        time.sleep(2)
        # Query order
        while True:
            r = bitopro_client.get_an_order(pair=pair, order_id=order_id)
            print(r)
            if r['status'] == 2:
                break
            else:
                time.sleep(10)
        print('Order completed!')
        price_sell = round(float(r['avgExecutionPrice']) * (1 + 0.01), quote_precision)
        # Place a limit sell order (for profit margin)
        r = bitopro_client.create_an_order(pair=pair, action='sell', amount=str(amount), price=str(price_sell), type=OrderType.Limit)
        print(r)

if __name__ == '__main__':
    strategy('btc', 'usdt')         
```

#### A Simple Indicator Strategy (SMA)

```python
from datetime import datetime, timezone

from bitoproClient.bitopro_restful_client import CandlestickResolutin
from bitoproClient.bitopro_indicator import indicator

def strategy(base, quote):
    pair = f"{base.lower()}_{quote.lower()}"
    signal_entry_long: bool = False
    signal_exit_long: bool = False
    resolution = CandlestickResolutin._1d
    dt_string = '2023/01/01 00:00:00'
    start_ts = int(datetime.strptime(dt_string, "%Y/%m/%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp())
    end_ts = int(datetime.now(timezone.utc).timestamp())
    sma_df = indicator("sma", pair, resolution, start_ts, end_ts, length=7)
    sma21_df = indicator("sma", pair, resolution, start_ts, end_ts, length=21)
    sma_df["SMA_21"] = sma21_df["SMA_21"]
    sma_7_last = sma_df['SMA_7'].iloc[-1]
    sma_7_penultimate = sma_df['SMA_7'].iloc[-2]
    sma_21_last = sma_df['SMA_21'].iloc[-1]
    sma_21_penultimate = sma_df['SMA_21'].iloc[-2]
    if (
        float(sma_7_penultimate) < float(sma_21_penultimate) and
        float(sma_7_last) > float(sma_21_last)
    ):
        signal_entry_long = True  # Entry signal
    elif (
        float(sma_7_penultimate) > float(sma_21_penultimate) and
        float(sma_7_last) < float(sma_21_last)
    ):
        signal_exit_long = True  # Exit signal
    if signal_entry_long:
        # Please check the balance and place a buy order
        signal_entry_long = False
    if signal_exit_long:
        # Please check the balance and place a sell order, if unable to do so, don't proceed.
        signal_exit_long = False
        
if __name__ == '__main__':
    strategy('btc', 'usdt')     
```
