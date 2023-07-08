"""
Using RapidAPI, latest News from CNBC about the compaines mentioned 
is extracted and stored in respective json files.
"""
# Import Dependencies
import json
import requests
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from api_keys import url, headers


def text_extract(cnbc_url) -> str:
    """
    Given an open url from CNBC website, all the relevant text is extracted
    """
    session = HTMLSession()
    html_response = session.get(cnbc_url)
    final_text = ""

    soup = BeautifulSoup(html_response.content, "html.parser")
    result = soup.find_all(class_="group")
    for ele in result:
        for text in ele.find_all("p"):
            final_text += text.text.strip()
    return final_text


if __name__ == "__main__":
    companies = ["NVDA", "INTC", "TSM"]
    parameters = ["headline", "url", "shortDateFirstPublished"]

    for idx, company in enumerate(companies):
        querystring = {"symbol": f"{company}", "page": "1", "pageSize": "30"}
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        df = pd.DataFrame.from_dict(response.json())

        with open(f"Data/{company}_news.json", "w+", encoding="UTF-8") as jsonfile:
            dict_dump = {}
            INDEX = 1
            for i in df["data"]["symbolEntries"]["results"]:
                if len(i["tickerSymbols"]) < 5:
                    if not i["premium"]:
                        if i["__typename"] == "cnbcnewsstory":
                            data = {parameter: i[parameter] for parameter in parameters}
                            data["Text"] = text_extract(i["url"])
                            dict_dump[f"{INDEX}"] = data
                            INDEX += 1
            json.dump(dict_dump, jsonfile, indent=4, separators=(",", ": "))
            print(
                f"{idx+1}. Data Extracted from {company} is Extracted and stored as shown:"
            )
            for keys, values in dict_dump.items():
                print("\t", keys, ":")
                print("\t" * 2, values, "\n")
