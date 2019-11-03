from cloudant.client import Cloudant

from check_login import check_login

import json

import sys

def add_family_members(username, password, fullName, phoneNumber):
    client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    for document in my_database:
        username_db = document["username"]
        password_db = document["password"]
        if  username == username_db and password == password_db:
            document['preferences']['family_numbers'].append({fullName, phoneNumber})
            document.save()
            print("Family member's phone number info pushed to document in database")
            break
        else:
            print("User not found", file=sys.stderr)

    client.disconnect()

if __name__ == '__main__':
    add_family_members(username, password, name, number)