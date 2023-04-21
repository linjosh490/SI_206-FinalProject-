import requests
import sqlite3
import csv
import numpy as np
import matplotlib.pyplot as plt

def get_aqi_info(api_data):
    #the base url for the air quality API 
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
    curr.execute('''CREATE TABLE IF NOT EXISTS air_quality (id INTEGER PRIMARY KEY, latitude REAL, longitude REAL, hour_id INTEGER, aqi INTEGER, category_id INTEGER)''')


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
        latitude = latandlong[0]
        longitude = latandlong[1]
        cursor.execute("INSERT INTO air_quality (latitude, longitude, hour_id, aqi, category_id) VALUES (?, ?, ?, ?, ?)", (latitude, longitude, hour_id, aqi, category_id))

    conn.commit()
    conn.close()


def calculate_average_aqi(latitude, longitude):
    conn = sqlite3.connect("air_quality.db")
    cursor = conn.cursor()

    # query the database to get the AQI values
    cursor.execute("SELECT aqi FROM air_quality WHERE latitude = ? AND longitude = ?", (latitude, longitude))
    results = cursor.fetchall()

    # extract the AQI values into a list using list comprehension
    aqi_values = [result[0] for result in results]

    # calculate the average AQI
    average_aqi = sum(aqi_values) / len(aqi_values)
    conn.close()

    return average_aqi
    

def data_visual():
    cities = ['Ann Arbor, MI', 'Tustin, CA', 'Shanghai, China', 'Tokyo, Japan', 'Sydney, Australia', 'New York, NY', 'London, UK']
    aqi = [calculate_average_aqi(42.292328, -83.736755), calculate_average_aqi(33.752544, -117.81802), calculate_average_aqi(31.2, 121.4375), calculate_average_aqi(35.7, 139.6875), calculate_average_aqi(-33.75, 151.125), calculate_average_aqi(40.710335, -73.99307), calculate_average_aqi(51.5, -0.120000124)]

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(cities, aqi, color='green')
    ax.grid(axis='y')

    # Set the title and axis labels
    ax.set_title('Average Air Quality Index by City')
    ax.set_xlabel('City')
    ax.set_ylabel('Air Quality Index')

    # Display the chart
    plt.show()



def join_tables():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()

    # Join the two tables using SQL query
    query = '''SELECT air_quality.latitude, air_quality.longitude, weather_data.visibility, weather_data.temperature_2m, weather_data.relativehumidity_2m, air_quality.aqi FROM weather_data INNER JOIN air_quality ON weather_data.lat = air_quality.latitude AND weather_data.long = air_quality.longitude AND weather_data.hourly_time = air_quality.hour_id '''
    result = cursor.execute(query).fetchall()

    cursor.execute('''CREATE TABLE IF NOT EXISTS joined_table (latitude REAL, longitude REAL, visibility REAL, temperature_2m REAL, relativehumidity_2m REAL, aqi INTEGER)''')

    # Insert the joined data into the new table
    cursor.executemany('''INSERT INTO joined_table VALUES (?, ?, ?, ?, ?, ?)''', result)

    # Commit changes and close database connection
    conn.commit()
    conn.close()

def create_scatterplot():
    # Connect to the database and create a cursor object
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()

    # Retrieve data from the joined table
    cursor.execute('SELECT visibility, aqi FROM joined_table')
    data = cursor.fetchall()

    x = np.array([row[0] for row in data])
    y = np.array([row[1] for row in data])

    # Calculate the slope and intercept of the line of best fit
    m, b = np.polyfit(x, y, 1)

    # Create a scatterplot
    plt.scatter(x, y, c='green')
    plt.xlabel('Visibility')
    plt.ylabel('Air Quality Index (AQI)')
    plt.title('Relationship between AQI and Visibility')

    # plt.xlim(0)
    # plt.ylim(0)

    # Plot the line of best fit
    plt.plot(x, m*x+b, c='red')

    # Show the correlation coefficient
    corr_coef = np.corrcoef(x, y)[0,1]
    plt.text(0.05, 0.9, f'Correlation coefficient: {corr_coef:.2f}', transform=plt.gca().transAxes)

    plt.show()

    conn.close()


def write_csv():
    # Create a list of tuples containing the city name, latitude, longitude, and AQI
    cities = [('Ann Arbor', 42.292328, -83.736755, calculate_average_aqi(42.292328, -83.736755)),
            ('Tustin', 33.752544, -117.81802, calculate_average_aqi(33.752544, -117.81802)),
            ('Shanghai', 31.2, 121.4375, calculate_average_aqi(31.2, 121.4375)),
            ('Tokyo', 35.7, 139.6875, calculate_average_aqi(35.7, 139.6875)),
            ('Sydney', -33.75, 151.125, calculate_average_aqi(-33.75, 151.125)),
            ('New York', 40.710335, -73.99307, calculate_average_aqi(40.710335, -73.99307)),
            ('London', 51.5, -0.120000124, calculate_average_aqi(51.5, -0.120000124))]

    # Open a file for writing and create a CSV writer object
    with open('city_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['City', 'Latitude', 'Longitude', 'AQI'])

        # Write the data for each city
        for city in cities:
            writer.writerow(city)

#dictionary: new longitude, latitude
# key is number, lat& long is value
# conn = sqlite3.connect('locations.db')
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE locations (location_id INTEGER PRIMARY KEY, latitude REAL, longitude REAL)''')

# # Insert the data into the locations table
# locations = {
#     0: (42.28, -83.74),  # Ann Arbor, Michigan
#     1: (33.75, -117.83),  # Tustin, California
#     2: (47.61, -122.33),  # Seattle, Washington
#     3: (35.69, 139.69),  # Tokyo, Japan
#     4: (-33.87, 151.21),  # Sydney, Australia
#     5: (40.71, -74.01),  # New York
#     6: (51.51, -0.13)  # London, UK
# }

# for location_id, (latitude, longitude) in locations.items():
#     cursor.execute('''INSERT INTO locations (location_id, latitude, longitude) VALUES (?, ?, ?)''', (location_id, latitude, longitude))

# conn.commit()
# conn.close()

#for loop
#auto increment

def main(): 
    # locations = {
    #     0: (42.28, -83.74),  # Ann Arbor
    #     1: (33.75, -117.83),  # Tustin, California
    #     2: (47.61, -122.33),  # Seattle
    #     3: (35.69, 139.69),  # Tokyo, Japan
    #     4: (-33.87, 151.21),  # Sydney, Australia
    #     5: (40.71, -74.01),  # New York
    #     6: (51.51, -0.13)  # London, UK
    # }
    
    ann_arbor_aqi = get_aqi_info("?lat=42.292328&lon=-83.736755&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    aa_latandlong = getlatandlong("?lat=42.292328&lon=-83.736755&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    
    tustin_aqi = get_aqi_info("?lat=33.752544&lon=-117.81802&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    tustin_latandlong = getlatandlong("?lat=33.752544&lon=-117.81802&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    
    shanghai_aqi = get_aqi_info("?lat=31.2&lon=121.4375&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    shanghai_latandlong = getlatandlong("?lat=31.2&lon=121.4375&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    
    tokyo_aqi = get_aqi_info("?lat=35.7&lon=139.6875&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    tokyo_latandlong = getlatandlong("?lat=35.7&lon=139.6875&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    
    sydney_aqi = get_aqi_info("?lat=-33.75&lon=151.125&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    sydney_latandlong = getlatandlong("?lat=-33.75&lon=151.125&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
   
    new_york_aqi = get_aqi_info("?lat=40.710335&lon=-73.99307&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    newyork_latandlong = getlatandlong("?lat=40.710335&lon=-73.99307&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    
    london_aqi = get_aqi_info("?lat=51.5&lon=-0.120000124&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    london_latandlong = getlatandlong("?lat=51.5&lon=-0.120000124&key=7ca2640fbc58462ea0698af01079813d&start_datetime=2023-04-19T00:00:00&end_datetime=2023-04-19T23:00:00")
    

    create_db_table("air_quality.db")

    database_processing(ann_arbor_aqi, aa_latandlong)
    database_processing(tustin_aqi, tustin_latandlong)
    database_processing(shanghai_aqi, shanghai_latandlong)
    database_processing(tokyo_aqi, tokyo_latandlong)
    database_processing(sydney_aqi, sydney_latandlong)
    database_processing(new_york_aqi, newyork_latandlong)
    database_processing(london_aqi, london_latandlong)

    annarbor_avg_aqi = calculate_average_aqi(42.292328, -83.736755)
    print(f"Ann Arbor's average aqi is {annarbor_avg_aqi}.")
    tustin_avg_aqi = calculate_average_aqi(33.752544, -117.81802)
    print(f"Tustin's average aqi is {tustin_avg_aqi}.")
    shanghai_avg_aqi = calculate_average_aqi(31.2, 121.4375) 
    print(f"Shanghai's average aqi is {shanghai_avg_aqi}.")
    tokyo_avg_aqi = calculate_average_aqi(35.7, 139.6875)
    print(f"Tokyo's average aqi is {tokyo_avg_aqi}.")
    syney_avg_aqi = calculate_average_aqi(-33.75, 151.125)
    print(f"Sydney's average aqi is {syney_avg_aqi}.")
    newyork_avg_aqi = calculate_average_aqi(40.710335, -73.99307)
    print(f"New York's average aqi is {newyork_avg_aqi}.")
    london_avg_aqi = calculate_average_aqi(51.5, -0.120000124)
    print(f"London's average aqi is {london_avg_aqi}.")

    data_visual()

    join_tables()

    create_scatterplot()

    #write data into a file
    write_csv()


if __name__ == "__main__":
    main()