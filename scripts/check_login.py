from cloudant.client import Cloudant

import json

import sys

def check_login(username, password):
    client = Cloudant.iam("","")
    client.connect()
    database_name = "test"
    my_database = client[database_name]

    for d in my_database:
        username_db = d["username"]
        password_db = d["password"]
        if username == username_db and password == password_db:
            print(json.dumps(d))
            client.disconnect()
            return
    print('Could not find account', file=sys.stderr)
    client.disconnect()

if __name__ == '__main__':
	check_login(sys.argv[1], sys.argv[2])
