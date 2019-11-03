from cloudant.client import Cloudant

import json

def save_loc_to_db(user, location):
  client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
  client.connect()
  db = client["test"]
  
  loc = json.loads(location)
  
  data = {
    "user": user,
    "lastLat": location['lat'],
    "lastLng": location['lng']
  }
  
  doc = db.create_document(data)

  client.disconnect()
