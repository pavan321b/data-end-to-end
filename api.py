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
from flask import Flask,render_template,request,redirect,url_for


import os
from datetime import datetime

from api_keys import url, headers
from bert import analyse



app = Flask(__name__)

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

def average_scores(file):
    file_type=type(file)
    if file_type is not dict:
        data=json.load(file)
    else:
        data=file
    avg_scores={'Positive':0,'Neutral':0,'Negative':0}
    for i in data.keys():
            try:
                int(i)
                if 'sentiment_score' in data[i].keys():
                    for j in data[i]['sentiment_score'].keys():
                        avg_scores[j]+=data[i]['sentiment_score'][j]
                
            except:
                pass
    return avg_scores
    

def API(companies):
    
    print('Comapnies: ',companies)
    
    
    html_response={key:{} for key in companies}
    for company in companies:
        file_path=f"Data/{company}_news.json"
        print('Company in search:',company)
        if os.path.isfile(file_path):
            print(f'File Already Exists for {company}')
            json_file=open(file_path,'r',encoding='UTF-8')
            
            data=json.load(json_file)
            json_file.close()
            if (datetime.now()-datetime.strptime(data['Last_Modified'],"%m-%d-%Y %H:%M:%S")).seconds < 86400:
    
                #Extract data from file and return

                html_response[company]=data_extract(company,file_path,file_exists=True) 
                
                
            else:
                
                #Extract data from url and update the file
                
                html_response[company]=data_extract(company,file_path,file_exists=False) 
        else:
            #File doesn't exist. So, create one
            html_response[company]=data_extract(company,file_path,file_exists=False)
    return html_response

def data_extract(company,file_path,file_exists=True):
    '''Data extract from url or file'''
    if file_exists:
       
        with open(file_path,"r",encoding='UTF-8') as jsonfile:
            return average_scores(file=jsonfile)

        
    else:

        parameters = ["headline", "url", "shortDateFirstPublished"]
        querystring = {"symbol": company, "page": "1", "pageSize": "30"}
        response = requests.get(url, headers=headers, params=querystring, timeout=10)

        df = pd.DataFrame.from_dict(response.json())
        print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!{company}')
        print(df.head())
        with open(file_path, "w+", encoding="UTF-8") as jsonfile:
            dict_dump = {}
            INDEX = 1
            
            for i in df["data"]["symbolEntries"]["results"]:
                if len(i["tickerSymbols"]) < 3:
                    if not i["premium"]:
                        if i["__typename"] == "cnbcnewsstory":
                            data = {parameter: i[parameter] for parameter in parameters}
                            
                            data["Text"] = text_extract(i["url"])
                            if len(data['Text'].split(" "))<300:
                                data["sentiment_score"] = analyse(data["Text"])
                            else:
                                print(f"{company}: {data['url']}")
                                
                            dict_dump[f"{INDEX}"] = data
                            INDEX += 1

            current_time=datetime.now()
            dict_dump["Last_Modified"]=current_time.strftime("%m-%d-%Y %H:%M:%S")

            json.dump(dict_dump, jsonfile, indent=4, separators=(",", ": "))

            return average_scores(dict_dump)


@app.route('/success/')
def success():

    '''Success data read from index and return to data.html'''
    data=request.args.getlist('data')
    stock_names={'Tesla':'TSLA','Nvidia':'NVDA','Intel':'INTC','TSMC':'TSMC'}
    data=[stock_names[company] for company in data]


    final_data=API(data)
    #news_items=[{'Stock_Name':} for data in final_data]
    return render_template('data.html', news_items=final_data)

@app.route('/',methods = ['POST', 'GET'])
def index():
    '''Route the data appropriately fom index.html'''
    if request.method == 'POST':
        selected_companies = request.form.getlist('company')
        return redirect(url_for('success', data=selected_companies))
    return render_template('index.html')



if __name__=="__main__":
    app.run()
