import requests
import sqlite3
import datetime

# API endpoint URL
url = 'https://api.breezometer.com/pollen/v2/forecast/daily?lat=48.857456&lon=2.354611&days=3&key=7ca2640fbc58462ea0698af01079813d'

#auto-increment
#organize data 

#dictionary 
#new longitude, latitude
# key is number, lat& long is value

locations = {
    0: (42.28, -83.74),  # Ann Arbor
    1: (33.75, -117.83),  # Tustin, California
    2: (47.61, -122.33),  # Seattle
    3: (35.69, 139.69),  # Tokyo, Japan
    4: (-33.87, 151.21),  # Sydney, Australia
    5: (40.71, -74.01),  # New York
    6: (51.51, -0.13)  # London, UK
}


# API parameters
# params = {
#     'latitude': 51.5072,
#     'longitude': 0.1276,
#     'YOUR_API_KEY': '7ca2640fbc58462ea0698af01079813d',
#     'Features_List': 'types_information',
#     'Number_of_Days': 5
# }


#for loop
#auto increment

# Make API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Extract relevant data from the API response
    data = response.json()
    
    # Connect to SQLite database
    conn = sqlite3.connect('breezometer.db')
    c = conn.cursor()

    # Drop the existing table if it exists
    c.execute('''DROP TABLE IF EXISTS pollen_forecast''')

    # Create table to store pollen forecast data
    c.execute('''CREATE TABLE IF NOT EXISTS pollen_forecast (id INTEGER PRIMARY KEY, date TEXT, grass_index_value INTEGER, grass_index_category TEXT, tree_index_value INTEGER, tree_index_category TEXT)''')

    # Insert data into the pollen forecast table
    for day in data['data']:
        date = day['date']
        grass_index_value = day['types']['grass']['index']['value']
        grass_index_category = day['types']['grass']['index']['category']
        tree_index_value = day['types']['tree']['index']['value']
        tree_index_category = day['types']['tree']['index']['category']
        c.execute('''INSERT INTO pollen_forecast (date, grass_index_value, grass_index_category, tree_index_value, tree_index_category) VALUES (?, ?, ?, ?, ?)''', (date, grass_index_value, grass_index_category, tree_index_value, tree_index_category))

    conn.commit()
    conn.close()

else:
    print('API request failed with status code', response.status_code)