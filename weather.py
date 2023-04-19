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

def database_processing(data):
    #Connect to sqlite3 database
    conn = sqlite3.connect("openmateo.db")
    curr = conn.cursor() 

    curr.execute('''DROP TABLE IF EXISTS weather_forecast''')
    curr.execute('''CREATE TABLE IF NOT EXISTS weather_forecast ()''')





def main(): 
    #gets the weather infor for ann arbor for the next 16 days 
    ann_arbor_weather = get_weather_info("latitude=42.28&longitude=-83.74&daily=temperature_2m_max,windspeed_10m_max&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York")




if __name__ == "__main__":
    main()