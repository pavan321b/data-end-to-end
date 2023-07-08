import requests
import json
import pandas as pd


url = "https://cnbc.p.rapidapi.com/news/v2/list-by-symbol"

headers = {
    "X-RapidAPI-Key": "888ca61bdcmsha51178159dd4b1ep14aea5jsn41edc42f9c54",
    "X-RapidAPI-Host": "cnbc.p.rapidapi.com",
}

companies=['NVDA']

for company in companies:
    querystring = {"symbol": f"{company}", "page": "1", "pageSize": "30"}
    response = requests.get(url, headers=headers, params=querystring, timeout=10)

print(response.json())
