import urllib.request
import json
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from twilio.rest import Client

def db_check():
    client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    sample_data = [
        [1, "one", "boiling", 100],
        [2, "two", "hot", 40],
        [3, "three", "warm", 20],
        [4, "four", "cold", 10],
        [5, "five", "freezing", 0]
    ]

    for document in sample_data:
        # Retrieve the fields in each row.
        number = document[0]
        name = document[1]
        description = document[2]
        temperature = document[3]

        # Create a JSON document that represents
        # all the data in the row.
        json_document = {
            "numberField": number,
            "nameField": name,
            "descriptionField": description,
            "temperatureField": temperature
        }

        # Create a document using the Database API.
        new_document = my_database.create_document(json_document)

    print('Data uploaded to database')
    client.disconnect()

def send_text():
    # Your Account SID from twilio.com/console
    account_sid = "AC0da46e5fbcfc6bcce3a1a4eef28d9ef6"
    # Your Auth Token from twilio.com/console
    auth_token  = "67a090fe998a51715ab4cbf6e6685a9f"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+19173594555", 
        from_="+18455210416",
        body="Hello from Python!")

    print(message.sid)


def printResults(data):
    # json module loads the string data into a dictionary
    quakes = json.loads(data)

    # access the contents of the JSON like any other Python object
    if "title" in quakes["metadata"]:
        print(quakes["metadata"]["title"])

    for q in quakes["features"]:
        if q["properties"]["mag"] >= 5.0:
            print(q['geometry']['coordinates'])

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
    db_check()
    #send_text()