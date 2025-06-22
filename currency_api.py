from dotenv import load_dotenv
import requests
import os

load_dotenv()


def get_result(base_name, symbols_name):
  url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols_name}&base={base_name}"

  payload = {}

  headers= {
    "apikey": os.getenv("EXCHANGE_RATE_API_KEY")
  }

  response = requests.request("GET", url, headers=headers, data = payload)

  if response.status_code != 200:
    return None

  return response.json()