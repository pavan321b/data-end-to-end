import json
import requests
import pandas as pd


url = "https://cnbc.p.rapidapi.com/news/v2/list-by-symbol"

headers = {
    "X-RapidAPI-Key": "888ca61bdcmsha51178159dd4b1ep14aea5jsn41edc42f9c54",
    "X-RapidAPI-Host": "cnbc.p.rapidapi.com",
}

companies = ["NVDA",]
parameters = ["headline", "url", "id", "shortDateFirstPublished"]
for company in companies:
    querystring = {"symbol": f"{company}", "page": "1", "pageSize": "30"}
    response = requests.get(url, headers=headers, params=querystring, timeout=10)
    df = pd.DataFrame.from_dict(response.json())
    listObj = [
        {parameter: i[parameter] for parameter in parameters}
        for i in df["data"]["symbolEntries"]["results"]
        if len(i["tickerSymbols"]) < 5
        if not i["premium"]
    ]

    with open(f"Data/{company}_news.json", "w") as jsonfile:
        json.dump(listObj, jsonfile, indent=4, separators=(",", ": "))
        print(listObj)
