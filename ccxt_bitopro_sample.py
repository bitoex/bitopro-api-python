# -*- coding: utf-8 -*-
import asyncio
from ccxt.bitopro import bitopro as rest_bito
from ccxt.pro.bitopro import bitopro as ws_bito
from typing import List
from ccxt.base.types import Balances, Int, Market, OrderBook, Str, Ticker, Trade

account = ""
api_key = ""
api_secret = ""
pair = "btc_usdt"

'''
restful api sample
'''
def ccxt_restful():
    bitopro_rest:rest_bito = rest_bito()
    bitopro_rest.apiKey = api_key
    bitopro_rest.secret = api_secret

    '''
    Open restful
    '''

    # [GET] list of currencies
    response = bitopro_rest.fetch_currencies()
    print(f"List of currencies: {response}\n")

    # [GET] limitations and fees
    response = bitopro_rest.load_fees()
    print(f"List limitations and fees: {response}\n")

    # [GET] order book
    response = bitopro_rest.fetch_order_book("btc_twd")
    print(f"Order book:{response}\n")

    # [GET] tickers
    response = bitopro_rest.fetch_tickers(["btc_twd", "eth_twd"])
    print(f"Tickers: {response}\n")

    # [GET] trades
    response = bitopro_rest.fetch_trades("btc_twd")
    print(f"Trades: {response}\n")

    # [GET] candlestick
    start_time = 1650707415
    end_time = 1678355415
    limit = int((1678355415 - 1650707415) / 60 / 60 / 24)
    response = bitopro_rest.fetch_ohlcv("btc_twd", "1d", start_time * 1000, limit)
    print(f"Candlestick: {response}\n")

    # [GET] trading pairs
    response = bitopro_rest.fetch_markets()
    print(f"Trading pairs: {response}\n")

    '''
    Auth restful
    '''
    # [GET] account balance
    response = bitopro_rest.fetch_balance()
    print(f"Account balance: {response}\n")

    # [POST] Create a limit order
    create_order_response = bitopro_rest.create_order(pair, "limit", "buy", amount=0.0001, price=10500)
    if create_order_response is not None:
        order_id = create_order_response["id"]
    print(f"Limit order created:{create_order_response}\n")

    # [GET] get open orders
    response = bitopro_rest.fetch_open_orders(pair)
    print(f"fetch open orders:{response}\n")

    # [GET] get closed orders
    response = bitopro_rest.fetch_closed_orders(pair)
    print(f"fetch closed orders:{response}\n")

    # [GET] Get an order
    get_an_order_response = bitopro_rest.fetch_order(order_id, pair)
    print(f"Get an order:{get_an_order_response}\n")

    # [DELETE] Cancel the order
    cancel_order_response = bitopro_rest.cancel_order(order_id, pair)
    print(f"Order cancelled:{cancel_order_response}\n")

    # [GET] get all orders
    response = bitopro_rest.fetch_orders(pair)
    print(f"All orders:{response}\n")

    # [GET] get all trades
    response = bitopro_rest.fetch_my_trades(pair)
    print(f"All trades:{response}\n")

    # [DELETE] Cancel all symbol order
    response = bitopro_rest.cancel_all_orders(pair)
    print(f"All order cancelled:{response}\n")

    # [POST] Withdraw
    response = bitopro_rest.withdraw(pair, 0.0, "", "")
    print(f"All order cancelled:{response}\n")

'''
websocket sample
'''

def ccxt_websocket_sample():
    bitopro_ws:ws_bito = ws_bito()
    bitopro_ws.login = account
    bitopro_ws.apiKey = api_key
    bitopro_ws.secret = api_secret

    loop = asyncio.new_event_loop()
    tasks = []
    tasks.append(loop.create_task(watch_order_book_info(pair, bitopro_ws)))
    tasks.append(loop.create_task(watch_ticker_info(pair, bitopro_ws)))
    tasks.append(loop.create_task(watch_trade_info(pair, bitopro_ws)))
    tasks.append(loop.create_task(watch_balance_info(bitopro_ws)))
    tasks.append(loop.create_task(watch_my_trades_info(pair, bitopro_ws)))
    loop.run_until_complete(asyncio.wait(tasks))

# public order book info
async def watch_order_book_info(pair:str, bitopro_ws:ws_bito):  
    while True:
        try:
            orderbook:OrderBook = await bitopro_ws.watch_order_book(pair)
            print(f"orderbook: {orderbook}\n")
        except Exception as e:
            print(type(e).__name__, str(e))
            break

# public ticker info
async def watch_ticker_info(pair:str, bitopro_ws:ws_bito):
    while True:
        try:
            ticker:Ticker = await bitopro_ws.watch_ticker(pair)
            print(f"ticker: {ticker}\n")
        except Exception as e:
            print(type(e).__name__, str(e))
            break

# public trade info
async def watch_trade_info(pair:str, bitopro_ws:ws_bito):
    while True:
        try:
            trade:List[Trade] = await bitopro_ws.watch_trades(pair)
            print(f"trade: {trade}\n")
        except Exception as e:
            print(type(e).__name__, str(e))
            break

# auth user balance info
async def watch_balance_info(bitopro_ws:ws_bito):
    while True:
        try:
            balance:Balances = await bitopro_ws.watch_balance()
            print(f"balance: {balance}\n")
        except Exception as e:
            print(type(e).__name__, str(e))
            break

# auth user trade info
async def watch_my_trades_info(pair:str, bitopro_ws:ws_bito):
    while True:
        try:
            my_trades:List[Trade] = await bitopro_ws.watch_my_trades(pair)
            print(f"my trades: {my_trades}\n")
        except Exception as e:
            print(type(e).__name__, str(e))
            break

if __name__ == "__main__":
    ccxt_restful()
    ccxt_websocket_sample()
    

