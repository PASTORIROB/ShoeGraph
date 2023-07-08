import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns


#Filters by price level and graphs target group of shoes
def Graphit():
    #Keyword filter
    Target_shoe = 'Jordan'
    
    #Price Filter
    max_price = 130

    excluded_names = []
    conn = sqlite3.connect('nike_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, current_price, date FROM products")
    rows = cursor.fetchall()
    data_by_name = {}
    for row in rows:
        name, current_price, date = row
        if 'gift card' in name.lower():
            continue
        if max_price < current_price:
            continue
        if name.lower().find(Target_shoe.lower()) == -1:
            print(name + ' excluded')
            continue 
        if name not in data_by_name:
            data_by_name[name] = {'date': [], 'current_price': []}

        data_by_name[name]['current_price'].append(current_price)
        data_by_name[name]['date'].append(datetime.strptime(date, '%Y-%m-%d'))
        

    sns.set(style="darkgrid")
    # Create a figure and axis
    fig, ax = plt.subplots()


    for i, (name, data) in enumerate(data_by_name.items()):
        timestamps = data['date']
        prices = data['current_price']
        sorted_indices = sorted(range(len(timestamps)), key=lambda k: timestamps[k])
        data_by_name[name]['timestamps'] = [timestamps[i] for i in sorted_indices]
        data_by_name[name]['prices'] = [prices[i] for i in sorted_indices]
        last_index = len(timestamps) - 1
        plt.text(timestamps[last_index], prices[last_index], name, ha='center', va='center', fontsize=8)  
        
        
        
        
        
        
        
        plt.plot(timestamps, prices, label=f'{i+1}.{name}')

  
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.title(f'Prices of {Target_shoe} Shoes Over Time', fontdict={'fontsize': 16})
    
    plt.show()


