# -*- coding: utf-8 -*-

import threading
from loguru import logger
import websocket

BitoproWebsocketEndpoint = "wss://stream.bitopro.com:9443/ws"

class BitoproExWebsocket():
    def __init__(self, endpoint: str, callback):
        self.__connect_endpoint: str = endpoint
        self.send_opening_message:str = ""
        self.callback = callback 

        self.__ws: websocket.WebSocketApp = None
        self.wst: threading.Thread = None
        
    def init_websocket(self):
        self.__ws = websocket.WebSocketApp(
            self.__connect_endpoint,
            on_message=lambda ws, msg: self.__on_message(ws, msg),
            on_close=lambda ws: self.__on_close(ws),
            on_error=lambda msg: self.__on_error(msg),
            on_open=lambda ws: self.__on_open(ws),
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

    def __on_close(self, ws):
        self._set_websocket()
        self.wst.start()

    def __on_error(self, ws, error):
        logger.error(error)
        log_message = f"{self.self.__connect_endpoint} closed connection, reconnecting...\n"
        logger.info(log_message)