import urllib.request
import requests
import json
import uncurl
import time
import datetime
import math
from math import sin, cos, sqrt, atan2, radians
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from twilio.rest import Client

def create_document(username,password, first_name, last_name):
    client = Cloudant.iam("","")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    document = {
        'username': username,
        'password': password,
        'first_name':first_name,
        'last_name': last_name,
        'preferences': {
            'data_permission': 'false',
            'family_numbers':[], #[{'8455210416':'Bob'},{'8455210415':'Sally'}]
            'radius':20
        },
        'coordinates': []
    }

    my_database.create_document(document)
    print('Document created!')
    client.disconnect()

def add_coordinates(username,password,lat,lng):
    client = Cloudant.iam("","")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    for document in my_database:
        username_db = document["username"]
        password_db = document["password"]
        if  username == username_db and password == password_db:
            document['coordinates'].append([{"lat": lat},{"lng": lng},{"timestamp":str(datetime.datetime.now())}])
            document.save()
            print('Coordinates pushed to document in database')
            break
        else:
            print("User not found")

    client.disconnect()

def add_family_members(username,password,name,number):
    client = Cloudant.iam("","")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    for document in my_database:
        username_db = document["username"]
        password_db = document["password"]
        if  username == username_db and password == password_db:
            document['preferences']['family_numbers'].append({number:name})
            document.save()
            print("Family member's phone number info pushed to document in database")
            break
        else:
            print("User not found")

    client.disconnect()

def send_text(lat,lng,target_number):
    # Your Account SID from twilio.com/console
    account_sid = ""
    # Your Auth Token from twilio.com/console
    auth_token  = ""

    client = Client(account_sid, auth_token)


    message = client.messages.create(
        to="+1"+target_number, 
        from_="+19387770709",
        body="ATTENTION: You have been designated as a loved one or family member by\n" + 
        "INSERT NAME HERE. An earthquake has occured and power services may be sparse.\n"+ 
        "Here is INSERT NAME HERE's last location: " + ' www.google.com/maps/place/'+str(lat)+'+'+str(lng))
    print(message.sid)

def in_radius(d_lat,d_lng,lat,lng,radius):
    R = 6373 #km
    dlat = radians(lat) - radians(d_lat) 
    dlon = radians(lng) - radians(d_lng)

    a = sin(dlat / 2)**2 + cos(d_lat) * cos(lat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    if distance <= radius:
        return True
    return False

def print_results(data):
    # json module loads the string data into a dictionary
    quakes = json.loads(data)
    quake_list = []
    # access the contents of the JSON like any other Python object
    if "title" in quakes["metadata"]:
        print(quakes["metadata"]["title"])

    for q in quakes["features"]:
        if q["properties"]["mag"] >= 6.0:
            print('Earthquake located at', q['geometry']['coordinates'], q["properties"]["place"] ,"--- Magnitude:", q["properties"]["mag"])

def get_earthquake_data():
    # variable to hold the source URL
    # free data feed from the USGS lists all earthquakes for the last day larger than Mag 2.5
    urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"
    
    # Opens the URL and read the data
    webUrl = urllib.request.urlopen(urlData)
    print (webUrl.getcode())
    if (webUrl.getcode() == 200):
        data = webUrl.read()
        # print out results
        print_results(data)
    else:
        print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))

if __name__ == "__main__":
    send_text(10,20,'9173594555')
    send_text(10,20,'8455210416')
    send_text(41,10,'2396890887')
    #send_text(41,10,'6507395096')
    #get_earthquake_data()