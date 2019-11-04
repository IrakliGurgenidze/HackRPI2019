from cloudant.client import Cloudant

import uuid

import sys

def create_new_user(username, password):
  client = Cloudant.iam("","")
  client.connect()
  db = client["test"]
  
  data = {
    "username": username,
    "password": password,
    'preferences': {
        'data_permission': 'false',
        'family_numbers':[]
    },
    'coordinates': []
  }
  
  doc = db.create_document(data)

  print("user created")
  client.disconnect()

if __name__=="__main__":
  create_new_user(sys.argv[1], sys.argv[2])
