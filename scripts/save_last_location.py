from cloudant.client import Cloudant

from check_login import check_login

import json

import sys

def save_last_location(username, password, locationData):
    client = Cloudant.iam("","")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    found = False
    for d in my_database:
        username_db = d["username"]
        password_db = d["password"]
        if username == username_db and password == password_db:
            d['coordinates'].append(json.loads(locationData))
            d.save()
            found = True
            break

#    my_database.create_document(data)
    if found: print('Date pushed to database')
    else: print('User not found', file=sys.stderr)
    client.disconnect()

if __name__ == '__main__':
    save_last_location(sys.argv[1], sys.argv[2], sys.argv[3])
