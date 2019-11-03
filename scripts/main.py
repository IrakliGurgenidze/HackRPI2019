import urllib.request
import json
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from twilio.rest import Client

def db_connect():
    client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
    client.connect()
    database_name = "test"
    return client

def db_get():
    client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    for doc in my_database:
        print(doc['lastLat'], doc['lastLng'])


    client.disconnect()

def db_push():
    client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    data = {
        'username':'skrt@gmail.com',
        'password': 'julia1738',
        'preferences': {
            'data_permission': 'true',
            'family_numbers':[{'8455210416':'Bob'},{'8455210415':'Sally'}]
        },
        'coordinates': [
            [
                {"lat": 69},
                {"lng": 69},
                {"timestamp":"11/3/2019"}
            ]
        ]
    }
    data['coordinates'].append([
                {"lat": 69},
                {"lng": 69},
                {"timestamp":"11/4/2019"}
        ])

    my_database.create_document(data)
    print('Date pushed to database')
    client.disconnect()

def check_login(username, password):
    client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    for d in my_database:
        username_db = d["username"]
        password_db = d["password"]
        if username == username_db and password == password_db:
            return True

    client.disconnect()
    return False

def send_text():
    # Your Account SID from twilio.com/console
    account_sid = "AC08edac3cdeeed8e8341e114d675949f6"
    # Your Auth Token from twilio.com/console
    auth_token  = "78fa5f050df281597e411df17c6f0896"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+18455210416", 
        from_="+19387770709",
        body="www.google.com/maps/place/42.72128+-73.6886784")
    print(message.sid)


def printResults(data):
    # json module loads the string data into a dictionary
    quakes = json.loads(data)

    # access the contents of the JSON like any other Python object
    if "title" in quakes["metadata"]:
        print(quakes["metadata"]["title"])

    for q in quakes["features"]:
        if q["properties"]["mag"] >= 4.5:
            print(q['geometry']['coordinates'], "and mag is:", q["properties"]["mag"])

def main():
    # variable to hold the source URL
    # free data feed from the USGS lists all earthquakes for the last day larger than Mag 2.5
    urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"
    
    # Opens the URL and read the data
    webUrl = urllib.request.urlopen(urlData)
    print (webUrl.getcode())
    if (webUrl.getcode() == 200):
        data = webUrl.read()
        # print out results
        printResults(data)
    else:
        print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))

if __name__ == "__main__":
    #main()
    #db_get()
    #send_text()
    db_push()
    check_login("skrt@gmail.com","julia1738")