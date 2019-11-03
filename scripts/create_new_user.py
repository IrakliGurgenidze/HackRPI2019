from cloudant.client import Cloudant

import uuid

import sys

def create_new_user(username, password):
  client = Cloudant.iam("4936a8b9-e57c-4de5-b14b-847be444e187-bluemix", "dVyyF4i1Cs2NvTwmzlJiGHnyGlVcHm_c16LzIcOrZIH0")
  client.connect()
  db = client["test"]
  
  data = {
    "username": username,
    "password": password,
    "uuid": uuid.uuid4().hex
  }
  
  doc = db.create_document(data)

  client.disconnect()

if __name__=="__main__":
  create_new_user(sys.argv[1], sys.argv[2])
