import requests
import sqlite3
import datetime


#auto-increment
#organize data 

def get_aqi_info(api_data):
    #the base url for the weather API 
    base_url = "https://api.breezometer.com/air-quality/v2/historical/hourly"
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

    curr.execute('''DROP TABLE IF EXISTS air_quality''')
    curr.execute('''CREATE TABLE IF NOT EXISTS air_quality (id INTEGER PRIMARY KEY, latitute REAL, longitude REAL, hour_id INTEGER, aqi INTEGER, category_id INTEGER)''')


def getlatandlong(link): 
    link = link[1:]
    pairs = link.split("&")

    # Loop through the list of pairs to find the latitude and longitude
    for pair in pairs:
        key, value = pair.split("=")
        if key == "lat":
            latitude = value
        elif key == "lon":
            longitude = value
    
    latandlong = (latitude, longitude)
    return latandlong

def database_processing(data, latandlong):
# create the database and table
    conn = sqlite3.connect("air_quality.db")
    cursor = conn.cursor()

    # insert the categories as an id into the table
    categories = {
        "Excellent air quality": 1,
        "Good air quality": 2,
        "Moderate air quality": 3,
        "Low air quality": 4,
        "Poor air quality": 5
    }

    # insert the date as a hour_id into the table
    hours = {
        "2023-04-19T00:00:00Z": 0,
        "2023-04-19T01:00:00Z": 1,
        "2023-04-19T02:00:00Z": 2,
        "2023-04-19T03:00:00Z": 3,
        "2023-04-19T04:00:00Z": 4,
        "2023-04-19T05:00:00Z": 5,
        "2023-04-19T06:00:00Z": 6,
        "2023-04-19T07:00:00Z": 7,
        "2023-04-19T08:00:00Z": 8,
        "2023-04-19T09:00:00Z": 9,
        "2023-04-19T10:00:00Z": 10,
        "2023-04-19T11:00:00Z": 11,
        "2023-04-19T12:00:00Z": 12,
        "2023-04-19T13:00:00Z": 13,
        "2023-04-19T14:00:00Z": 14,
        "2023-04-19T15:00:00Z": 15,
        "2023-04-19T16:00:00Z": 16,
        "2023-04-19T17:00:00Z": 17,
        "2023-04-19T18:00:00Z": 18,
        "2023-04-19T19:00:00Z": 19,
        "2023-04-19T20:00:00Z": 20,
        "2023-04-19T21:00:00Z": 21,
        "2023-04-19T22:00:00Z": 22,
        "2023-04-19T23:00:00Z": 23
    }



    for item in data["data"]:
        datetime = item["datetime"]
        hour_id = hours.get(datetime)
        aqi = item["indexes"]["baqi"]["aqi"]
        category = item["indexes"]["baqi"]["category"]
        category_id = categories.get(category)
        latitute = latandlong[0]
        longitude = latandlong[1]
        cursor.execute("INSERT INTO air_quality (latitute, longitude, hour_id, aqi, category_id) VALUES (?, ?, ?, ?, ?)", (latitute, longitude, hour_id, aqi, category_id))

    # commit changes and close the connection
    conn.commit()
    conn.close()


def calculate_average_aqi():
    conn = sqlite3.connect("air_quality.db")
    cursor = conn.cursor()
    
    latandlong = ("42.28", "-83.74")  # replace with your lat and long values

    # query the database to get the AQI values
    cursor.execute("SELECT aqi FROM air_quality WHERE latitute = ? AND longitude = ?", latandlong)
    results = cursor.fetchall()

    # extract the AQI values into a list using list comprehension
    aqi_values = [result[0] for result in results]

    # calculate the average AQI
    average_aqi = sum(aqi_values) / len(aqi_values)
    
    print("The average AQI is:", average_aqi)
    
    conn.close()

#dictionary: new longitude, latitude
# key is number, lat& long is value
conn = sqlite3.connect('locations.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE locations (location_id INTEGER PRIMARY KEY, latitude REAL, longitude REAL)''')

# Insert the data into the locations table
locations = {
    0: (42.28, -83.74),  # Ann Arbor, Michigan
    1: (33.75, -117.83),  # Tustin, California
    2: (47.61, -122.33),  # Seattle, Washington
    3: (35.69, 139.69),  # Tokyo, Japan
    4: (-33.87, 151.21),  # Sydney, Australia
    5: (40.71, -74.01),  # New York
    6: (51.51, -0.13)  # London, UK
}

for location_id, (latitude, longitude) in locations.items():
    cursor.execute('''INSERT INTO locations (location_id, latitude, longitude) VALUES (?, ?, ?)''', (location_id, latitude, longitude))

conn.commit()
conn.close()
# url1 = 'https://api.breezometer.com/air-quality/v2/historical/hourly?lat=48.857456&lon=2.354611&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-20T02:00:00'
# response = requests.get(url1)
# data = response.json()['data']

# conn = sqlite3.connect('air_quality.db')
# c = conn.cursor()

# c.execute('''CREATE TABLE air_quality (datetime text, aqi integer, category text)''')

# for entry in data:
#     datetime = entry['datetime']
#     aqi = entry['indexes']['baqi']['aqi']
#     category = entry['indexes']['baqi']['category']
#     c.execute("INSERT INTO air_quality VALUES (?, ?, ?)", (datetime, aqi, category))

# conn.commit()
# conn.close()

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
    
    ann_arbor_aqi = get_aqi_info("?lat=42.28&lon=-83.74&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    aa_latandlong = getlatandlong("?lat=42.28&lon=-83.74&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    #print(aa_latandlong)
    tustin_aqi = get_aqi_info("?lat=33.75&lon=-117.83&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    tustin_latandlong = getlatandlong("?lat=33.75&lon=-117.83&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")

    seattle_aqi = get_aqi_info("?lat=47.61&lon=-122.33&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    seattle_latandlong = getlatandlong("?lat=33.75&lon=-117.83&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    
    tokyo_aqi = get_aqi_info("?lat=35.69&lon=139.69&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    tokyo_latandlong = getlatandlong("?lat=35.69&lon=139.69&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")

    sydney_aqi = get_aqi_info("?lat=-33.87&lon=151.21&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    sydney_latandlong = getlatandlong("?lat=-33.87&lon=151.21&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")

    new_york_aqi = get_aqi_info("?lat=40.71&lon=-74.01&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    newyork_latandlong = getlatandlong("?lat=-40.71&lon=-74.01&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")

    london_aqi = get_aqi_info("?lat=51.51&lon=-0.13&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    london_latandlong = getlatandlong("?lat=51.51&lon=-0.13&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")

    create_db_table("air_quality.db")

    database_processing(ann_arbor_aqi, aa_latandlong)
    database_processing(tustin_aqi, tustin_latandlong)
    database_processing(seattle_aqi, seattle_latandlong)
    database_processing(tokyo_aqi, tokyo_latandlong)
    database_processing(sydney_aqi, sydney_latandlong)
    database_processing(new_york_aqi, newyork_latandlong)
    database_processing(london_aqi, london_latandlong)

    calculate_average_aqi()

if __name__ == "__main__":
    main()