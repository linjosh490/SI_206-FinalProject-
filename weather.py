import requests
import sqlite3
import datetime


#this gets the weather information that we want

def get_weather_info(api_data):
    #the base url for the weather API 
    base_url = "https://api.open-meteo.com/v1/forecast?"
    api_url = base_url + api_data

    #check if the response was successful 
    response = requests.get(api_url)

    if response.status_code == 200: 
        data = response.json() 
        return data

    else: 
        print('API request failed with status code', response.status_code)

def create_db_table(table_name): 
    conn = sqlite3.connect(table_name)
    curr = conn.cursor() 

    curr.execute('''DROP TABLE IF EXISTS weather_data''')
    curr.execute('''CREATE TABLE IF NOT EXISTS weather_data(latitude real, longitude real, generationtime_ms real, utc_offset_seconds integer, elevation real, time text, temperature_2m_max real,
             temperature_2m_min real, windspeed_10m_max real)''')


def database_processing(data):
    ##Connect to sqlite3 database
    conn = sqlite3.connect("openmateo.db")
    curr = conn.cursor() 

    latitude = data['latitude']
    longitude = data['longitude']
    generationtime_ms = data['generationtime_ms']
    utc_offset_seconds = data['utc_offset_seconds']
    elevation = data['elevation']

    for i in range(len(data['daily']['time'])):
        time = data['daily']['time'][i]
        temp_max = data['daily']['temperature_2m_max'][i]
        temp_min = data['daily']['temperature_2m_min'][i]
        windspeed_max = data['daily']['windspeed_10m_max'][i]

        curr.execute('''INSERT INTO weather_data (latitude, longitude, generationtime_ms, utc_offset_seconds,
        elevation, time, temperature_2m_max, temperature_2m_min, windspeed_10m_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (latitude, longitude, generationtime_ms, utc_offset_seconds, elevation, time,
        temp_max, temp_min, windspeed_max))

    conn.commit()
    conn.close()


  



def main(): 
    #gets the weather info from designated area for the dates 4/17 - 4/21, EST time zone 

    # locations = {
    #     0: (42.28, -83.74),  # Ann Arbor
    #     1: (33.75, -117.83),  # Tustin, California
    #     2: (47.61, -122.33),  # Seattle
    #     3: (35.69, 139.69),  # Tokyo, Japan
    #     4: (-33.87, 151.21),  # Sydney, Australia
    #     5: (40.71, -74.01),  # New York
    #     6: (51.51, -0.13)  # London, UK
    # }
    
    ann_arbor_weather = get_weather_info("latitude=42.28&longitude=-83.74&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max&temperature_unit=fahrenheit&start_date=2023-04-17&end_date=2023-04-21&timezone=America%2FNew_York")
    tustin_weather = get_weather_info("latitude=33.75&longitude=-117.83&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max&temperature_unit=fahrenheit&start_date=2023-04-17&end_date=2023-04-21&timezone=America%2FNew_York")
    seattle_weather = get_weather_info("latitude=47.61&longitude=-122.33&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max&temperature_unit=fahrenheit&start_date=2023-04-17&end_date=2023-04-21&timezone=America%2FNew_York")
    tokyo_weather = get_weather_info("latitude=35.69&longitude=139.69&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max&temperature_unit=fahrenheit&start_date=2023-04-17&end_date=2023-04-21&timezone=America%2FNew_York")
    sydney_weather = get_weather_info("latitude=-33.87&longitude=151.21&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max&temperature_unit=fahrenheit&start_date=2023-04-17&end_date=2023-04-21&timezone=America%2FNew_York")
    new_york_weather = get_weather_info("latitude=40.71&longitude=-74.01&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max&temperature_unit=fahrenheit&start_date=2023-04-17&end_date=2023-04-21&timezone=America%2FNew_York")
    london_weather = get_weather_info("latitude=51.51&longitude=-0.13&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max&temperature_unit=fahrenheit&start_date=2023-04-17&end_date=2023-04-21&timezone=America%2FNew_York")

    create_db_table("openmateo.db")

    database_processing(ann_arbor_weather)
    database_processing(tustin_weather)
    database_processing(seattle_weather)
    database_processing(tokyo_weather)
    database_processing(sydney_weather)
    database_processing(new_york_weather)
    database_processing(london_weather)

if __name__ == "__main__":
    main()