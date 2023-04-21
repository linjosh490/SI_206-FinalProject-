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
    #Connects to the sqlite3 database
    conn = sqlite3.connect(table_name)
    curr = conn.cursor() 

    #Creates a new table in the database 
    curr.execute('''DROP TABLE IF EXISTS weather_data''')
    curr.execute('''CREATE TABLE IF NOT EXISTS weather_data
                 (lat REAL, long REAL, hourly_time INTEGER, elevation REAL, relativehumidity_2m REAL,
                  visibility REAL, temperature_2m REAL)''')


def database_processing(data, table_name):
    hours = {
        "2023-04-19T00:00": 0,
        "2023-04-19T01:00": 1,
        "2023-04-19T02:00": 2,
        "2023-04-19T03:00": 3,
        "2023-04-19T04:00": 4,
        "2023-04-19T05:00": 5,
        "2023-04-19T06:00": 6,
        "2023-04-19T07:00": 7,
        "2023-04-19T08:00": 8,
        "2023-04-19T09:00": 9,
        "2023-04-19T10:00": 10,
        "2023-04-19T11:00": 11,
        "2023-04-19T12:00": 12,
        "2023-04-19T13:00": 13,
        "2023-04-19T14:00": 14,
        "2023-04-19T15:00": 15,
        "2023-04-19T16:00": 16,
        "2023-04-19T17:00": 17,
        "2023-04-19T18:00": 18,
        "2023-04-19T19:00": 19,
        "2023-04-19T20:00": 20,
        "2023-04-19T21:00": 21,
        "2023-04-19T22:00": 22,
        "2023-04-19T23:00": 23
    }

    #Connect to sqlite3 database
    conn = sqlite3.connect(table_name)
    curr = conn.cursor() 

    #Get the information from the data json 
    lat = data['latitude']
    longi = data['longitude']
    elevation = data['elevation']

    for i in range(len(data['hourly']['time'])):
        time = data['hourly']['time'][i]
        value = hours.get(time)
        temp = data['hourly']['temperature_2m'][i]
        humidity = data['hourly']['relativehumidity_2m'][i]
        windspeed = data['hourly']['windspeed_120m'][i]

        curr.execute('''INSERT INTO weather_data (lat, long, hourly_time, elevation, relativehumidity_2m, visibility, temperature_2m) VALUES (?, ?, ?, ?, ?, ?, ?)''', (lat, longi, value, elevation, temp, humidity, windspeed))

    conn.commit()
    conn.close()

def getlatandlong(link): 
    pairs = link.split("&")

    # Loop through the list of pairs to find the latitude and longitude
    for pair in pairs:
        key, value = pair.split("=")
        if key == "latitude":
            latitude = value
        elif key == "longitude":
            longitude = value

    # Print the latitude and longitude
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    
    latandlong = (latitude, longitude)
    return latandlong

def main(): 
    #gets the weather info from designated area for the date, hourly 4/19, EST

    # locations
    #     0: (42.28, -83.74),  # Ann Arbor
    #     1: (33.75, -117.83),  # Tustin, California
    #     2: (47.61, -122.33),  # Seattle
    #     3: (35.69, 139.69),  # Tokyo, Japan
    #     4: (-33.87, 151.21),  # Sydney, Australia
    #     5: (40.71, -74.01),  # New York
    #     6: (51.51, -0.13)  # London, UK



    ann_arbor_weather = get_weather_info("latitude=42.28&longitude=-83.74&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    tustin_weather = get_weather_info("latitude=33.75&longitude=-117.83&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    seattle_weather = get_weather_info("latitude=47.61&longitude=-122.33&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    tokyo_weather = get_weather_info("latitude=35.69&longitude=139.69&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    sydney_weather = get_weather_info("latitude=-33.87&longitude=151.21&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    new_york_weather = get_weather_info("latitude=40.71&longitude=-74.01&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    london_weather = get_weather_info("latitude=51.51&longitude=-0.13&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")

    aa_latandlong = getlatandlong("latitude=42.28&longitude=-83.74&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    print(aa_latandlong)
    
    create_db_table("openmateo.db")
    omdb = "openmateo.db"

    database_processing(ann_arbor_weather, omdb)
    database_processing(tustin_weather, omdb)
    database_processing(seattle_weather,omdb)
    database_processing(tokyo_weather, omdb)
    database_processing(sydney_weather, omdb)
    database_processing(new_york_weather, omdb)
    database_processing(london_weather, omdb)

if __name__ == "__main__":
    main()