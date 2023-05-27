# -*- coding: utf-8 -*-

import threading
from loguru import logger
import websocket
from bitopro_util import build_headers,get_current_timestamp

BitoproWebsocketEndpoint = "wss://stream.bitopro.com:443/ws"

class BitoproExWebsocket():
    def __init__(self, endpoint: str, callback, account:str="", api_key:str="", api_secret:str=""):
        self.__connect_endpoint: str = endpoint
        self.send_opening_message:str = ""
        self.__account:str = account
        self.__api_key:str = api_key
        self.__api_secret:str = api_secret

        self.callback = callback 

        self.__ws: websocket.WebSocketApp = None
        self.wst: threading.Thread = None
        
    def init_websocket(self):
        if self.__account and self.__api_key and self.__api_secret:
            params = {"identity": self.__account, "nonce": get_current_timestamp()}
            ws_headers = build_headers(self.__api_key, self.__api_secret, params=params)
        else:
            ws_headers = None

        self.__ws = websocket.WebSocketApp(
            self.__connect_endpoint,
            on_message=self.__on_message,
            on_close=self.__on_close,
            on_error=self.__on_error,
            on_open=self.__on_open,
            header=ws_headers
        )
        self.wst = threading.Thread(target=self.__ws.run_forever)

    def start(self):
        if self.wst != None:
            self.wst.start()

    def __on_open(self, ws):
        if self.send_opening_message != "":
            ws.send(self._send_opening_message)
        logger.debug("connected")

    def __on_message(self, ws, message):
        self.callback(message)

    def __on_close(self, ws, close_status_code, msg):
        self.init_websocket()
        self.wst.start()

    def __on_error(self, ws, error):
        logger.error(error)
        log_message = f"{self.self.__connect_endpoint} closed connection, reconnecting...\n"
        logger.info(log_message)