from currency_api import *
from datetime import datetime


time_info = result["timestamp"]
time = datetime.fromtimestamp(time_info).strftime("%H:%M:%S")

date = datetime.fromtimestamp(time_info).strftime("%Y-%m-%d")

lst = list(result["rates"].keys())
val = list(result["rates"].values())

curr_pairs = result["base"] + lst[0]
curr_prices = val[0]