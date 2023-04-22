import requests
import sqlite3
import datetime
import csv
import matplotlib.pyplot as plt
import numpy as np

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
        return('API request failed with status code', response.status_code)

def create_db_table(db_name): 
    #Connects to the sqlite3 database
    conn = sqlite3.connect(db_name)
    curr = conn.cursor() 

    #Creates a new table in the database 
    curr.execute('''DROP TABLE IF EXISTS weather_data''')
    curr.execute('''CREATE TABLE IF NOT EXISTS weather_data
                 (lat REAL, long REAL, hourly_time INTEGER, elevation REAL, relativehumidity_2m REAL,
                  visibility REAL, temperature_2m REAL)''')


def database_processing(data, db_name):
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
    conn = sqlite3.connect(db_name)
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


def calculate_pollen_relations(lat, longi):
    conn = sqlite3.connect('air_quality.db')
    curr = conn.cursor()
    curr.execute( '''SELECT 
                    strftime('%Y-%m-%d', hourly_time, 'unixepoch') AS day,
                    AVG(temperature_2m) AS avg_temperature,
                    AVG(relativehumidity_2m) AS avg_relativehumidity
                FROM weather_data
                WHERE lat = ? AND long = ?
                GROUP BY lat, long''', (lat, longi))
    result = curr.fetchall()

    conn.close()
    pollen_correlation = [row[1] * row[2] for row in result]

    return pollen_correlation

def create_bar_graph(cities, list_of_items):
    fig, ax = plt.subplots()
    ax.bar(cities, np.ravel(list_of_items), color = 'green')

    ax.set_title('Temperature and Relative Humidity Relations by City')
    ax.set_xlabel('City')
    ax.set_ylabel('Avg Temp and Relative Humidity')

    plt.show()

def write_csv(filename, handtlist, cities): 
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['City', 'Correlation with Pollen'])
        for i in range(len(handtlist)):
            writer.writerow([cities[i], handtlist[i][0]])

def main(): 
    ann_arbor_weather = get_weather_info("latitude=42.28&longitude=-83.74&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    tustin_weather = get_weather_info("latitude=33.75&longitude=-117.83&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    shanghai_weather = get_weather_info("latitude=31.22&longitude=121.46&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    tokyo_weather = get_weather_info("latitude=35.69&longitude=139.69&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    sydney_weather = get_weather_info("latitude=-33.87&longitude=151.21&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    new_york_weather = get_weather_info("latitude=40.71&longitude=-74.01&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")
    london_weather = get_weather_info("latitude=51.51&longitude=-0.13&hourly=temperature_2m,relativehumidity_2m,visibility,windspeed_120m&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&start_date=2023-04-19&end_date=2023-04-19&timezone=America%2FNew_York")

    # create_db_table("openmateo.db")
    # omdb = "openmateo.db"

    create_db_table("air_quality.db")
    aqdb = "air_quality.db"

    database_processing(ann_arbor_weather, aqdb)
    database_processing(tustin_weather, aqdb)
    database_processing(shanghai_weather,aqdb)
    database_processing(tokyo_weather, aqdb)
    database_processing(sydney_weather, aqdb)
    database_processing(new_york_weather, aqdb)
    database_processing(london_weather, aqdb)


    # database_processing(ann_arbor_weather, omdb)
    # database_processing(tustin_weather, omdb)
    # database_processing(shanghai_weather,omdb)
    # database_processing(tokyo_weather, omdb)
    # database_processing(sydney_weather, omdb)
    # database_processing(new_york_weather, omdb)
    # database_processing(london_weather, omdb)

    pollen_relations_list = []
    aa_pollen = calculate_pollen_relations(42.292328, -83.736755)
    tustin_pollen = calculate_pollen_relations(33.752544, -117.81802)
    shanghai_pollen = calculate_pollen_relations(31.2, 121.4375)
    tokyo_pollen = calculate_pollen_relations(35.7, 139.6875)
    sydney_pollen = calculate_pollen_relations(-33.75, 151.125)
    ny_pollen = calculate_pollen_relations(40.710335, -73.99307)
    london_pollen = calculate_pollen_relations(51.5, -0.120000124)

    pollen_relations_list.append(aa_pollen)
    pollen_relations_list.append(tustin_pollen)
    pollen_relations_list.append(shanghai_pollen)
    pollen_relations_list.append(tokyo_pollen)
    pollen_relations_list.append(sydney_pollen)
    pollen_relations_list.append(ny_pollen)
    pollen_relations_list.append(london_pollen)

    cities = ['Ann Arbor', 'Tustin', 'Shanghai', 'Tokyo', 'Sydney', 'New York', 'London']
    write_csv("weather_data.csv", pollen_relations_list, cities)
    create_bar_graph(cities, pollen_relations_list)
    

if __name__ == "__main__":
    main()