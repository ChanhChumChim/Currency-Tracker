from dotenv import load_dotenv
import requests
import os

load_dotenv()

url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD&base=XAU"

payload = {}

headers= {
  "apikey": os.getenv("EXCHANGE_RATE_API_KEY")
}

response = requests.request("GET", url, headers=headers, data = payload)

result = response.json()

print(result)