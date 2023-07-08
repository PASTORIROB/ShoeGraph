import requests
import json
import time
import sqlite3
import pandas as pd
import bokeh
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
from graphNIKEtimeseries import Graphit 


def get_Prices():
        count = 60
        anchor = 5
        while anchor < 60:
                        nikeurl = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=518E2C2B1F04C6B973C24531CF389567&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C0f64ecc7-d624-4e91-b171-b83a03dd8550%2C4f918ac7-2598-4b21-a46f-99c2db422867)%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D{count}&language=en&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
                        #get JSON data from nike
                        html = requests.get(url=nikeurl)
                        output = json.loads(html.text)
                        print(anchor)
                        anchor = anchor + count
                        time.sleep(2)
                        if count >= 100: # Break
                                break 
                        products = output['data']['products']['products']

                        #Connect to DB
                        conn = sqlite3.connect("nike_data.db")
                        cursor = conn.cursor()
                        cursor.execute("CREATE TABLE IF NOT EXISTS products (date TEXT, name TEXT, current_price REAL)")                           
        #enter prices into DB
        current_date = date.today()
        if products is not None:                          
         for item in products:
                        name = item['title']
                        name = name.replace("'", "")
                        
                        subtitle = item['subtitle']
                        current_price = float(item['colorways'][0]['price']['currentPrice'])
                        if subtitle is not None and current_price is not None:
                                print(f'{name} Subtitle: {subtitle} Current price: {current_price}')
                                #name = product["title"]
                                #price = product["price"]["regularPrice"]
                                cursor.execute(f"INSERT INTO products VALUES ('{current_date}', '{name}', {current_price})")
                        conn.commit()
                        

                        
                   
         #Graphs prices for the day
        cursor.execute("SELECT name, current_price FROM products")
        results = cursor.fetchall()
        if len(results) > 0:
         name, current_price = zip(*results)

        else: print('results length =0')
        
        sns.scatterplot(x=name, y=current_price)
        # Add labels and title
        plt.xlabel('Shoes')
        plt.ylabel('Price')
        plt.title('Nike Shoes available')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        # Display the plot
        plt.show()
        conn.close()
        
                                

if __name__ == "__main__":
    get_Prices()
    Graphit()
    
                   