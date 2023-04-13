import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import requests
import json


def get_fruits(fruit_id): 
    base_url = "https://fruityvice.com/api/fruit/"
    complete_url = base_url + fruit_id 
    raw = requests.get(complete_url)
    response = raw.json()
    print(response)
    return response


def main(): 
    get_fruits("Banana")
    get_fruits("Strawberry")

if __name__ == '__main__':
    main()