from currency_api import *
from auth import *
from datetime import datetime

def get_currency_data(result):
    try:
        time_info = result["timestamp"]
        time = datetime.fromtimestamp(time_info).strftime("%H:%M:%S")
        date = datetime.fromtimestamp(time_info).strftime("%Y-%m-%d")

        lst = list(result["rates"].keys())
        val = list(result["rates"].values())

        curr_pairs = result["base"] + lst[0]
        curr_prices = val[0]

        return {
            "curr_pairs": curr_pairs,
            "curr_prices": curr_prices,
            "time": time,
            "date": date
        }
    except Exception as e:
        return {"Error": f"Invalid data: {str(e)}"}