# -*- coding: utf-8 -*-
import json
from bitopro_util import build_headers, get_current_timestamp
from bitopro_restful_client import BitoproRestfulClient, CandlestickResolutin, OrderStatus, WithdrawProtocol
from bitopro_websocket_client import BitoproExWebsocket, BitoproWebsocketEndpoint

account = ""
apiKey = ""
apiSecret = ""


def bitopro_restful_test():
    bitopro_client = BitoproRestfulClient(apiKey, apiSecret)

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

    '''
    Auth restful test
    '''
    # [GET] account balance
    response = bitopro_client.get_account_balance()
    print("Account balance:", response)

    pair = "BTC_USDT"
    order_id = ""

    # [POST] Create an order
    create_order_response = bitopro_client.create_an_order(action="BUY", amount=0.0001, price=10500, pair=pair)
    if create_order_response is not None:
        order_id = create_order_response["orderId"]
    print("Order created:", create_order_response)
    
    # [GET] Get an order
    get_an_order_response = bitopro_client.get_an_order(pair, order_id)
    print("Get an order:", get_an_order_response)

    # [DELETE] Cancel the order
    if create_order_response is not None:
        order_id = create_order_response["orderId"]
        cancel_order_response = bitopro_client.cancel_an_order(order_id=order_id, pair=pair)
        print("Order cancelled:", cancel_order_response)

    # [GET] get all orders
    response = bitopro_client.get_all_orders(pair, status=OrderStatus.Completed)
    print("All orders:", response)

    # [GET] get all trades
    response = bitopro_client.get_trades_list(pair)
    print("All trades:", response)

    # [POST] Create batch order, create 10 orders at once
    pair = "BTC_USDT"
    batch_orders:dict = {}
    batch_orders[pair] = []
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    batch_orders[pair].append({
                **{"pair": pair},
                **{"action": "BUY"},
                **{"amount": str(0.0001)},
                **({"price": str(10500)}),
                **{"timestamp": get_current_timestamp()},
                **{"type": "LIMIT"},
             })
    create_batch_orders_response = bitopro_client.create_batch_order(batch_orders[pair])
    reply = None
    if create_batch_orders_response is not None:
        batch_orders[pair] = []
        reply = create_batch_orders_response["data"]
        for order in reply:
            batch_orders[pair].append(order["orderId"])
    print("Batch orders created:", reply)
    
    # [PUT] Cancel multiple orders
    cancel_multiple_orders_response = bitopro_client.cancel_multiple_orders(batch_orders)
    print("Cancel multiple orders:", cancel_multiple_orders_response)

    # [DELETE] Cancel all order
    cancel_all_orders_response = bitopro_client.cancel_all_orders("all")
    print("Cancel all order:", cancel_all_orders_response)

    # [GET] Deposit history
    deposit_history_response = bitopro_client.get_deposit_history("USDT")
    print("Deposit history:", deposit_history_response)
    
    # [GET] Withdraw history
    withdraw_history_response = bitopro_client.get_withdraw_history("BTC")
    print("Withdraw history:", withdraw_history_response)

    # [GET] GET Withdraw
    get_withdraw_response = bitopro_client.get_withdraw("USDT", "")
    print("GET withdraw:", get_withdraw_response)

    # [POST] Withdraw
    get_withdraw_response = bitopro_client.withdraw("USDT", WithdrawProtocol.ERC20, "", 50.5, "")
    print("GET withdraw:", get_withdraw_response)

def bitopro_websocket_test():
    # [PUBLIC] GET Order book
    bito_websocket_order_book = BitoproExWebsocket(BitoproWebsocketEndpoint + "/v1/pub/order-books/eth_btc:1", websocket_handler)
    bito_websocket_order_book.init_websocket()
    bito_websocket_order_book.start()

    # [PUBLIC] GET Ticket
    bito_websocket_ticker = BitoproExWebsocket(BitoproWebsocketEndpoint + "/v1/pub/tickers/eth_btc", websocket_handler)
    bito_websocket_ticker.init_websocket()
    bito_websocket_ticker.start()

    # [PUBLIC] GET Trade
    bito_websocket_trades = BitoproExWebsocket(BitoproWebsocketEndpoint + "/v1/pub/trades/eth_btc", websocket_handler)
    bito_websocket_trades.init_websocket()
    bito_websocket_trades.start()
    
    # [Private] GET active orders
    bito_websocket_order_book = BitoproExWebsocket(BitoproWebsocketEndpoint + "/v1/pub/auth/orders", websocket_handler, account, apiKey, apiSecret)
    bito_websocket_order_book.init_websocket()
    bito_websocket_order_book.start()

    # [Private] GET account balance
    bito_websocket_order_book = BitoproExWebsocket(BitoproWebsocketEndpoint + "/v1/pub/auth/account-balance", websocket_handler, account, apiKey, apiSecret)
    bito_websocket_order_book.init_websocket()
    bito_websocket_order_book.start()
    
    

def websocket_handler(message:str):
    reply = json.loads(message)
    if reply["event"] == "ACCOUNT_BALANCE":
        print(reply, end="\n\n")
    elif reply["event"] == "ACTIVE_ORDERS":
        print(reply, end="\n\n")
    elif reply["event"] == "ORDER_BOOK":
        print(reply, end="\n\n")
    elif reply["event"] == "TICKER":
        print(reply, end="\n\n")
    elif reply["event"] == "TRADE":
        print(reply, end="\n\n")
        
if __name__ == "__main__":
    bitopro_restful_test()
    bitopro_websocket_test()

    
    