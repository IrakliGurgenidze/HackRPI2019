from cloudant.client import Cloudant

import json

import sys

def save_loc_to_db(user, location):
  client = Cloudant.iam("","")
  client.connect()
  db = client["test"]
  
  loc = json.loads(location)
  
  data = {
    "user": user,
    "lastLat": loc['lat'],
    "lastLng": loc['lng']
  }
  
  doc = db.create_document(data)

  client.disconnect()

if __name__=="__main__":
  save_loc_to_db(sys.argv[1], sys.argv[2])
