#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import json
#https://developer.cisco.com/learning/tracks/collab-cloud/business-messaging/collab-spark-message/step/1
# Bearer: OGYwNzUyNDYtODkwMi00ZWFiLThhOWYtY2E3Mjc1YTc5OTQ1YWM2MzI1NTEtZjZk_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f
#https://developer.webex.com/docs/api/v1/people/get-my-own-detailshttps://developer.webex.com/docs/api/v1/people/get-my-own-details
#ODJhY2RiNDAtMWJlMy00NDI2LWE1NWEtMzQ0MTI0ZTFhZjZlMjI4MGI5MzEtM2Mz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f
#ZWYzYmUyMWYtZDM3OS00N2Y3LWJkMzctZDUzZmVhNDkwYzNmNTA5ODcyYzgtYTdi_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f
#This module facilitates Cisco webex Teams communications.
#This is implemented via a class through instantiating a webex_msg object.
#Webex_msg has the following methohods & properties.

'''
"id": "Y2lzY29zcGFyazovL3VzL1JPT00vYzBiZDMzODAtODk2NC0xMWU4LWJiZjgtZmIxOWQ1ZmY1NzAy",
      "title": "CxC AIS Team",
      "type": "group",
      "isLocked": false,
      "lastActivity": "2019-11-02T04:01:19.164Z",
      "creatorId": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jNTM1NzM4Ni1iOTJlLTRlNjMtYjlhZi1mNGIwYmRiYzk5MTg",
      "created": "2018-07-17T01:57:25.816Z",
      "ownerId": "1eb65fdf-9643-417f-9974-ad72cae0e10f"

#Methods

send_msg
status_code

#Properties
emailid

'''

#Global Variables
content_type='application/json'
path='messages'
email_id='tleach@cisco.com'
cxc_ais_teams_roomid='Y2lzY29zcGFyazovL3VzL1JPT00vYzBiZDMzODAtODk2NC0xMWU4LWJiZjgtZmIxOWQ1ZmY1NzAy'

class webex_msg(object):
    webex_URL = 'https://api.ciscospark.com/v1/'
    auth_header= "Bearer ZWYzYmUyMWYtZDM3OS00N2Y3LWJkMzctZDUzZmVhNDkwYzNmNTA5ODcyYzgtYTdi_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
    headers= {'Authorization': auth_header, 'content-type' : content_type}

    def __init__(self,email_id):
        print("Webex Teams Object Instantiated\n URL={0}\n".format(webex_msg.webex_URL+path))
        self.email_id=email_id
        self.cxc_ais_teams_roomid=cxc_ais_teams_roomid

    def send_webex_message(self, message_text ):
        #payload={"toPersonEmail":self.email_id, "text":"This is a trest message"}
        payload = {"roomId": self.cxc_ais_teams_roomid , "text": message_text}
        try:
            self.webex_request=requests.post(webex_msg.webex_URL+path,data=json.dumps(payload),headers=webex_msg.headers)
            return self.webex_request.status_code
        #Requests Expeption processing
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("Error {0}".format(e))
        #General exception processing
        except:
            print("An Exception Occured {0}".format(sys.exc_info()[0]))


if __name__ == "__main__":
    x=webex_msg("daalberg@cisco.com")
    z=x.send_webex_message('This is a test message 3')
    print("Status_code {0}".format(z))




