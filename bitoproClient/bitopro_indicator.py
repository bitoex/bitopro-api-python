from .bitopro_restful_client import (
    BitoproRestfulClient,
)
from loguru import logger

import pandas as pd
import numpy as np


def get_candlestick_data(pair, resolution, start_timestamp, end_timestamp):
    try:
        apiKey = ""
        apiSecret = ""
        bitopro_client = BitoproRestfulClient(apiKey, apiSecret)
        response = bitopro_client.get_candlestick(pair, resolution, start_timestamp, end_timestamp)
        if isinstance(response, dict) and "data" in response:
            data_list = response["data"]
            df = pd.DataFrame(data_list)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            return df
        else:
            print(response)
            return None
    except Exception as e:
        logger.exception(e)
        return None


def calculate_indicator(df, indname, **kwargs):
    try:
        import pandas_ta

        df = df.astype(float)
        getattr(pd.DataFrame().ta, indname)
        attr = lambda df, **kwargs: getattr(df.ta, indname)(**kwargs)
        return attr(df, **kwargs)
    except Exception as e:
        logger.exception(e)
        raise Exception("Indicator '{}' not found in pandas_ta.".format(indname))


def indicator(indname, pair, resolution, start_timestamp, end_timestamp, **kwargs):
    df = get_candlestick_data(pair, resolution, start_timestamp, end_timestamp)
    try:
        if df is not None:
            s = calculate_indicator(df, indname, **kwargs)
            if isinstance(s, list):
                s = {i: series for i, series in enumerate(s)}
            if isinstance(s, np.ndarray):
                s = {0: s}
            if isinstance(s, pd.Series):
                s = {s.name: s.values}
            if isinstance(s, pd.DataFrame):
                s = {i: series.values for i, series in s.items()}
            dfs = {}
            for colname, series in s.items():
                if colname not in dfs:
                    dfs[colname] = {}
                dfs[colname] = series if isinstance(series, pd.Series) else series
            for key, series in dfs.items():
                df[key] = series
            return df
        else:
            return None
    except Exception as e:
        logger.exception(e)
        return None
