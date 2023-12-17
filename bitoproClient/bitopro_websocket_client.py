# -*- coding: utf-8 -*-

import threading
import time
from loguru import logger
import websocket
from .bitopro_util import build_headers,get_current_timestamp

BitoproWebsocketEndpoint = "wss://stream.bitopro.com:443/ws/v1"

class BitoproExWebsocket():
    def __init__(self, account:str, api_key:str, api_secret:str, callback):
        self._connect_endpoint: str = ""
        self.send_opening_message:str = ""
        self._account:str = account
        self._api_key:str = api_key
        self._api_secret:str = api_secret

        self.callback = callback 

        self._ws: websocket.WebSocketApp = None
        self.wst: threading.Thread = None
        
    def init_websocket(self):
        if self._account and self._api_key and self._api_secret:
            params = {"identity": self._account, "nonce": ""}
            ws_headers = build_headers(self._api_key, self._api_secret, params=params)
        else:
            ws_headers = None

        self._ws = websocket.WebSocketApp(
            self._connect_endpoint,
            on_message=lambda ws, msg:self._on_message(ws, msg),
            on_close=lambda ws, status_code, msg: self._on_close(ws, status_code, msg),
            on_error=lambda ws, error:self._on_error(ws, error),
            on_open=lambda ws: self._on_open(ws),
            header=ws_headers
        )
        self.wst = threading.Thread(target=self._ws.run_forever)

    def start(self):
        if self.wst != None:
            self.wst.start()

    def _on_open(self, ws):
        if self.send_opening_message != "":
            ws.send(self._send_opening_message)
        logger.debug(f"{self.__class__.__name__} connected")

    def _on_message(self, ws, message):
        self.callback(message)

    def _on_close(self, ws, close_status_code, msg):
        log_message = f"{self._connect_endpoint} closed connection, reconnecting...\n"
        logger.info(log_message)
        time.sleep(3)
        self.init_websocket()
        self.wst.start()

    def _on_error(self, ws, error):
        logger.error(error)

class BitoproOrderBookWs(BitoproExWebsocket):
    def __init__(self, symbols_limit: dict, callback):
        super().__init__("", "", "", callback)
        self._connect_endpoint = BitoproWebsocketEndpoint + "/pub/order-books/"
        for symbol, limit in symbols_limit.items():
            self._connect_endpoint = self._connect_endpoint + f"{str.lower(symbol)}:{limit},"
        self._connect_endpoint = self._connect_endpoint[:-1]  # remove last ','

class BitoproTickerkWs(BitoproExWebsocket):
    def __init__(self, symbols: list, callback):
        super().__init__("", "", "", callback)

        self._connect_endpoint = BitoproWebsocketEndpoint + "/pub/tickers/"
        for symbol in symbols:
            self._connect_endpoint = self._connect_endpoint + f"{str.lower(symbol)},"
        self._connect_endpoint = self._connect_endpoint[:-1]  # remove last ','

class BitoproTradesWs(BitoproExWebsocket):
    def __init__(self, symbols: list, callback):
        super().__init__("", "", "", callback)

        self._connect_endpoint = BitoproWebsocketEndpoint + "/pub/trades/"
        for symbol in symbols:
            self._connect_endpoint = self._connect_endpoint + f"{str.lower(symbol)},"
        self._connect_endpoint = self._connect_endpoint[:-1]  # remove last ','

class BitoproUserOrdersWs(BitoproExWebsocket):
    def __init__(self, account: str, api_key: str, api_secret: str, callback):
        super().__init__(account, api_key, api_secret, callback)

        self._connect_endpoint = BitoproWebsocketEndpoint + "/pub/auth/orders"

class BitoproUserBlanceWs(BitoproExWebsocket):
    def __init__(self, account: str, api_key: str, api_secret: str, callback):
        super().__init__(account, api_key, api_secret, callback)

        self._connect_endpoint = BitoproWebsocketEndpoint + "/pub/auth/account-balance"
        
class BitoproUserTradeWs(BitoproExWebsocket):
    def __init__(self, account: str, api_key: str, api_secret: str, callback):
        super().__init__(account, api_key, api_secret, callback)

        self._connect_endpoint = BitoproWebsocketEndpoint + "/pub/auth/user-trades"

class BitoproHistoryOrders(BitoproExWebsocket):
    def __init__(self, account: str, api_key: str, api_secret: str, callback):
        super().__init__(account, api_key, api_secret, callback)

        self._connect_endpoint = BitoproWebsocketEndpoint + "/pub/auth/orders/histories"
        