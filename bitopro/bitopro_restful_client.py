# -*- coding: utf-8 -*-
from enum import Enum
import requests

from bitopro_util import build_headers, get_current_timestamp

class OrderType(Enum):
    Limit = 0,
    Market = 1

class OrderStatus(Enum):
    NotTriggered = -1
    InProgress = 0
    InProgressPartialDeal = 1
    Completed = 2
    CompletedPartialDeal = 3
    Cancelled = 4
    PostOnlyCancelled = 6

class StatusKind(Enum):
    ALL = 0
    OPEN = 1
    DONE = 1

class DepositStatus(Enum):
    CANCELLED = 0
    WAIT_PROCESS = 1

class WithdrawProtocol(Enum):
    MAIN = 0,
    ERC20 = 1, 
    OMNI = 2, 
    TRX = 3, 
    BSC = 4

class TimeInForce(Enum):
    GTC = 0,
    POST_ONLY = 1

class CandlestickResolutin(Enum):
    _1m = 0, 
    _5m = 1, 
    _15m = 2, 
    _30m = 3, 
    _1h = 4, 
    _3h = 5, 
    _6h = 6, 
    _12h = 7, 
    _1d = 8, 
    _1w = 9, 
    _1M = 10

class BitoproRestfulClient(object):
    def __init__(self, api_key:str="", api_secret:str="") -> None:
        self.baseUrl = "https://api.bitopro.com/v3"
        self.__api_key:str = api_key
        self.__api_secret:str = api_secret

    def send_request(self, method, url, headers:dict=None, data=None, timeout=None):
        try:
            session = requests.Session()
            response = None
            if method == "GET":
                response = session.get(url, headers=headers, params=data, timeout=timeout)
            elif method == "POST":
                response = session.post(url, headers=headers, json=data, timeout=timeout)
            elif method == "DELETE":
                response = session.delete(url, headers=headers, timeout=timeout)
            elif method == "PUT":
                response = session.put(url, headers=headers,json=data, timeout=timeout)

            if response is not None and response.status_code == requests.codes.ok:
                return response.json()
            else:
                return response.content.decode('utf8').replace("'", '"')

        except Exception as error:
            return error

    '''
    Open
    '''
    def get_currencies(self):
       """
       https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/open/currencies.md
       :return: the list of currencies
       """
       endpoint = f"/provisioning/currencies" 
       complete_url = self.baseUrl + endpoint
       return self.send_request(method="GET", url=complete_url)
    
    def get_limitations_and_fees(self):
       """
       https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/open/lims-fees.md
       :return: the limitations and fees
       """
       endpoint = f"/provisioning/limitations-and-fees" 
       complete_url = self.baseUrl + endpoint
       return self.send_request(method="GET", url=complete_url)
    
    def get_order_book(self, pair:str=None, limit:int=5, scale:int=0):
       """
       https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/open/order-book.md
       :param pair: the trading pair in format.
       :param limit: the limit for the response.
       :param scale: scale for the response. Valid scale values are different by pair.
       :return: the full order book of the specific pair
       """
       endpoint = f"/order-book/{pair}" 
       complete_url = self.baseUrl + endpoint
       params = {
            **{"limit": str(limit)},
            **({"scale": str(scale)}),
        }
       return self.send_request(method="GET", url=complete_url, data=params)
    
    def get_tickers(self, pair:str=None):
       """
       https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/open/tickers.md
       :param pair: the trading pair in format.
       :return: the ticker is a high level overview of the state of the market.
       """
       endpoint = f"/tickers/{pair}" 
       complete_url = self.baseUrl + endpoint
       return self.send_request(method="GET", url=complete_url)
    
    def get_trades(self, pair:str=None):
       """
       https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/open/trades.md
       :param pair: the trading pair in format.
       :return: a list of the most recent trades for the given symbol
       """
       endpoint = f"/trades/{pair}" 
       complete_url = self.baseUrl + endpoint
       return self.send_request(method="GET", url=complete_url)
    
    def get_candlestick(self, pair:str=None, resolution:CandlestickResolutin=CandlestickResolutin._1d, start_timestamp:int=None, end_timestamp:int=None):
       """
       https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/open/trading-history.md
       :param pair: the trading pair in format.
       :param resolution: the timeframe of the candlestick chart.
       :param start_timestamp: start time in unix timestamp.
       :param end_timestamp: end time in unix timestamp.
       :return: the open, high, low, close data in a period
       """
       endpoint = f"/trading-history/{pair}" 
       complete_url = self.baseUrl + endpoint
       params = {
            **{"resolution": resolution.name.replace("_","")},
            **({"from": str(start_timestamp)} if start_timestamp is not None else {}),
            **({"to": str(end_timestamp)} if end_timestamp is not None else {})
        }
       return self.send_request(method="GET", url=complete_url, data=params)
    
    def get_trading_pairs(self):
       """
       https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/open/trading-pairs.md
       :return: a list of pairs available for trade
       """
       endpoint = f"/provisioning/trading-pairs" 
       complete_url = self.baseUrl + endpoint
       return self.send_request(method="GET", url=complete_url)
    

    '''
    Auth
    '''
    def get_account_balance(self):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/account-balance.md
        :return: the account balance
        """
        endpoint = "/accounts/balance"
        complete_url = self.baseUrl + endpoint
        params = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=params)
        return self.send_request(method="GET", url=complete_url, headers=headers)

    def cancel_an_order(self, order_id:str, pair:str=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/cancel-batch.md
        :param pair: the trading pair in format.
        :param order_id: the id of the order.
        """
        endpoint = f"/orders/{pair}/{order_id}"
        complete_url = self.baseUrl + endpoint
        params = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=params)
        return self.send_request("DELETE", complete_url, headers=headers)

    def cancel_all_orders(self, pair:str=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/cancel-all.md
        :param pair: the trading pair in format.
        :cancel all your active orders of all pairs.
        """
        endpoint = f"/orders/{pair}"
        complete_url = self.baseUrl + endpoint
        params = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=params)
        return self.send_request("DELETE", complete_url, headers=headers)

    def cancel_multiple_orders(self, orders_request:dict=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/cancel-batch.md
        :param orders_request: multiple orders will be canceled
        :send a json format request to cancel multiple orders at a time.
        :example: {"BTC_USDT": ["12234566","12234567"],"ETH_USDT": ["44566712","24552212"]}
        """
        endpoint = f"/orders/"
        complete_url = self.baseUrl + endpoint
        headers = build_headers(self.__api_key, self.__api_secret, params=orders_request)
        return self.send_request("PUT", complete_url, headers=headers, data=orders_request)

    def create_an_order(self, action:str, amount:float, price:float=None, type:OrderType=OrderType.Limit, pair:str=None, stop_price:float=None, condition:str=None, time_in_force:TimeInForce=TimeInForce.GTC, client_id:int=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/create-order.md
        :param pair: the trading pair in format.
        :param action: the action type of the order.	
        :param amount: the amount of the order for the trading pair, please follow the link to see the limitations.
        :param price: the price of the order for the trading pair.	
        :param type: the order type.
        :param stop_price: the price to trigger stop limit order, only required when type is STOP_LIMIT.
        :param condition: the condition to match stop price, only required when type is STOP_LIMIT.
        :param time_in_force: condition for orders.
        :param client_id: this information help users distinguish their orders.
        :return: a dict contains an order info
        """
        endpoint = f"/orders/{pair}"
        complete_url = self.baseUrl + endpoint
        params = {
            **{"action": action},
            **{"amount": str(amount)},
            **({"price": str(price)} if price is not None else {}),
            **{"timestamp": get_current_timestamp()},
            **{"type": type.name},
            **({"stopPrice": str(stop_price)} if stop_price is not None else {}),
            **({"condition": condition} if condition is not None else {}),
            **({"timeInForce": time_in_force.name} if time_in_force is not None else {}),
            **({"clientId": client_id} if client_id is not None else {})
        }
        headers = build_headers(self.__api_key, self.__api_secret, params=params)
        return self.send_request(method="POST", url=complete_url, headers=headers, data=params)

    def create_batch_order(self, orders_request:list=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/create-batch-limitmarket.md
        :param orders_request: multiple orders will be created
        :example:
        [
            {
                pair: "BTC_TWD",
                action: "BUY",
                type: "LIMIT",
                price: "210000",
                amount: "1",
                timestamp: 1504262258000,
                timeInForce: "GTC",
            }, 
            {
                pair: "BTC_TWD",
                action: "SELL",
                type: "MARKET",
                amount: "2",
                timestamp: 1504262258000
            }
        ]
        """
        endpoint = f"/orders/batch"
        complete_url = self.baseUrl + endpoint
        headers = build_headers(self.__api_key, self.__api_secret, params=orders_request)
        return self.send_request(method="POST", url=complete_url, headers=headers, data=orders_request)

    def get_all_orders(self, pair:str=None, start_timestamp:int=None, end_timestamp:int=None, ignoreTimeLimitEnable:bool=False, status_kind:StatusKind=StatusKind.ALL, status:OrderStatus=None, order_id:str=None, limit:int=100, client_id:str=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/all-order.md
        :param pair: the trading pair in format.
        :param start_timestamp: start time in unix timestamp.
        :param end_timestamp: end time in unix timestamp.
        :param status_kind: filter order based on status kind, OPEN, DONE, ALL.
        :param status: filter order base on specific status.
        :param order_id: if specified, list starts with order with id >= orderId.
        :param limit: the number of records to retrieve.
        :param client_id: this information help users distinguish their orders.
        :return: the trade list
        """
        endpoint = f"/orders/all/{pair}"
        complete_url = self.baseUrl + endpoint
        params = {
            **({"startTimestamp": str(start_timestamp)} if start_timestamp is not None else {}),
            **({"endTimestamp": str(end_timestamp)} if end_timestamp is not None else {}),
             **({"ignoreTimeLimitEnable": ignoreTimeLimitEnable}),
            **({"statusKind": str(status_kind.name)} if status_kind is not None else {}),
            **({"status": str(status.value)} if status is not None else {}),
            **({"orderId": order_id} if order_id is not None else {}),
            **({"limit": str(limit)} if limit is not None else {}),
            **({"clientId": client_id} if client_id is not None else {}),
        }
        header = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=header)
        return self.send_request(method="GET", url=complete_url, headers=headers, data=params)

    def get_an_order(self, pair:str=None, order_id:str=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/get-order.md
        :param pair: the trading pair in format.
        :param order_id: the id of the order.	
        :return: an order infomation
        """   
        endpoint = f"/orders/{pair}/{order_id}"
        complete_url = self.baseUrl + endpoint
        header = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=header)
        return self.send_request(method="GET", url=complete_url, headers=headers)

    def get_trades_list(self, pair:str=None, start_timestamp:int=None, end_timestamp:int=None, order_id:str=None, trade_id:str=None, limit:int=100):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/all-trade.md
        :param pair: the trading pair in format.
        :param start_timestamp: start time in unix timestamp.
        :param end_timestamp: end time in unix timestamp.
        :param order_id: the id of the order.	
        :param trade_id: the id of the first trade in the response.
        :param limit: the limit for the response.
        :return: the all orders
        """        
        endpoint = f"/orders/trades/{pair}"
        complete_url = self.baseUrl + endpoint
        params = {
            **({"startTimestamp": str(start_timestamp)} if start_timestamp is not None else {}),
            **({"endTimestamp": str(end_timestamp)} if end_timestamp is not None else {}),
            **({"orderId": order_id} if order_id is not None else {}),
            **({"tradeId": trade_id} if trade_id is not None else {}),
            **({"limit": limit} if limit is not None else {}),
        }
        header = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=header)
        return self.send_request(method="GET", url=complete_url, headers=headers, data=params)

    def get_deposit_history(self, currency:str, start_timestamp:int=None, end_timestamp:int=None, limit:int=None, id:str=None, statuses:DepositStatus=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/get-deposit-history.md
        :param currency: the currency of the deposit to get.
        :param start_timestamp: start time in unix timestamp.
        :param end_timestamp: end time in unix timestamp.
        :param limit: the limit for the response.
        :param id: the id of the first data in the response.
        :param statuses: the status of the deposit.	
        :return: the deposit history information
        """        
        endpoint = f"/wallet/depositHistory/{currency}"
        complete_url = self.baseUrl + endpoint
        params = {
            **({"startTimestamp": str(start_timestamp)} if start_timestamp is not None else {}),
            **({"endTimestamp": str(end_timestamp)} if end_timestamp is not None else {}),
            **({"id": id} if id is not None else {}),
            **({"statuses": statuses.name} if statuses is not None else {}),
            **({"limit": limit} if limit is not None else {}),
        }
        header = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=header)
        return self.send_request(method="GET", url=complete_url, headers=headers, data=params)

    def get_withdraw_history(self, currency:str, start_timestamp:int=None, end_timestamp:int=None, limit:int=None, id:str=None, statuses:DepositStatus=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/get-withdraw-history.md
        :param currency: the currency of the withdraw to get.
        :param start_timestamp: start time in unix timestamp.
        :param end_timestamp: end time in unix timestamp.
        :param limit: the limit for the response.
        :param id: the id of the first data in the response.
        :param statuses: the status of the deposit.	
        :return: the withdraw history information
        """
        endpoint = f"/wallet/withdrawHistory/{currency}"
        complete_url = self.baseUrl + endpoint
        params = {
            **({"startTimestamp": str(start_timestamp)} if start_timestamp is not None else {}),
            **({"endTimestamp": str(end_timestamp)} if end_timestamp is not None else {}),
            **({"id": id} if id is not None else {}),
            **({"statuses": statuses.name} if statuses is not None else {}),
            **({"limit": limit} if limit is not None else {}),
        }
        header = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=header)
        return self.send_request(method="GET", url=complete_url, headers=headers, data=params)

    def get_withdraw(self, currency:str, serial:str=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/get-withdraw.md
        :param currency: the currency of the withdraw to get.
        :param serial: the serial of the withdraw.
        :return: the withdraw information
        """
        endpoint = f"/wallet/withdraw/{currency}/{serial}"
        complete_url = self.baseUrl + endpoint
        header = {"identity": "", "nonce": get_current_timestamp()}
        headers = build_headers(self.__api_key, self.__api_secret, params=header)
        return self.send_request(method="GET", url=complete_url, headers=headers)

    def withdraw(self, currency:str, protocol:WithdrawProtocol=WithdrawProtocol.MAIN, address:str=None, amount:float=None, message:str=None):
        """
        https://github.com/bitoex/bitopro-offical-api-docs/blob/master/v3-1/rest-1/auth/withdraw.md
        :param currency: the currency to withdraw.
        :param protocol: the protocol to send.
        :param address: the address or bank account to send fund.
        :param amount: the amount of fund to send.
        :param message: the message or note to be attached with withdraw.
        """
        endpoint = f"/wallet/withdraw/{currency}"
        complete_url = self.baseUrl + endpoint
        params = {
            **{"protocol": protocol.name},
            **({"amount": str(amount)} if amount is not None else {}),
            **{"timestamp": get_current_timestamp()},
            **({"message": message} if message is not None else {}),
        }
        headers = build_headers(self.__api_key, self.__api_secret, params=params)
        return self.send_request(method="POST", url=complete_url, headers=headers, data=params)

