from cloudant.client import Cloudant

from check_login import check_login

import json

import sys

def save_last_location(username, password, data):
    client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    data = check_login(username, password)

    data['coordinates'].append(data)

    my_database.create_document(data)
    print('Date pushed to database')
    client.disconnect()

if __name__ == '__main__':
    save_last_location(sys.argv[1], sys.argv[2], sys.argv[3])