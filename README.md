# bitopro-api-python

SDK for the [BitoPro](https://www.bitopro.com/) API.

[Bitopro official API document](https://github.com/bitoex/bitopro-offical-api-docs)

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
  
### Getting started

Create BitoPro client. Pass api keys only if
you are going to do authenticated calls. You can create an api key
[here](https://www.bitopro.com/api).

```python
bitopro_client = BitoproRestfulClient('apiKey', 'apiSecret')
```

### Limitations

#### Rate Limit

There is rate limits applied to each API, please check [API documentation](https://developer.bitopro.com/docs) for more detail.

#### Precisions

Both price and amount are subject to decimal restrictions, please check [official settings](https://www.bitopro.com/fees) for more detail.

#### Minimum order amount

Checkout the [official settings](https://www.bitopro.com/fees) of minimum amount.

### Public restful enpoint example

```python
from bitopro_restful_client import BitoproRestfulClient, CandlestickResolutin

if __name__ == '__main__':
    bitopro_client = BitoproRestfulClient('apiKey', 'apiSecret')

    '''
    Open restful test
    '''
    # [GET] list of currencies
    response = bitopro_client.get_currencies()
    print("List of currencies: ", response)

    # [GET] limitations and fees
    response = bitopro_client.get_limitations_and_fees()
    print("List of currencies: ", response)

    # [GET] order book
    pair = "BTC_USDT"
    response = bitopro_client.get_order_book(pair)
    print("Order book: ", response)

    # [GET] tickers
    response = bitopro_client.get_tickers(pair)
    print("Tickers: ", response)

    # [GET] trades
    response = bitopro_client.get_trades(pair)
    print("Trades: ", response)

    # [GET] candlestick
    response = bitopro_client.get_candlestick(pair, CandlestickResolutin._1d, 1650707415, 1678355415)
    print("Candlestick: ", response)

    # [GET] trading pairs
    response = bitopro_client.get_trading_pairs()
    print("Trading pairs: ", response)
```


