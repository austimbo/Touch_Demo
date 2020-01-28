#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import json
import sys
from os import environ
import webbrowser


#Global Variables
#Client ID And CLient Secret recuired in Teams Authorization. (Used to be in touch_serv)
Access_code =""
Client_ID="" #"Cff5893294edf86ee74882ad11344574c12488084ee6bfb0092547d07424afc44"
Secret_ID="" #"59fc1559331c330430ec41b9b026198ebe5513764535bb0214f09e7aa88debd6"
#Webex Teams variables
access_token=""
refresh_token=""
auth_parms_file="./auth_parms.txt"
#global Client_ID, Secret_ID, redirect_uri
content_type='application/json'
path='messages'
email_id='tleach@cisco.com'
cxc_ais_teams_roomid='Y2lzY29zcGFyazovL3VzL1JPT00vYzBiZDMzODAtODk2NC0xMWU4LWJiZjgtZmIxOWQ1ZmY1NzAy'
redirect_uri = "http://0.0.0.0:5000/oauth"
refreshed = False

#This module facilitates Cisco webex Teams communications.
#This is implemented via a class through instantiating a webex_msg object.
#Webex_msg has the following methohods & properties.
'''
#This is presented along wth the Information about integration.
#To edit details of the integration 
https://developer.webex.com/my-apps/touch_10_buddy


Integration ID: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL0NmZjU4OTMyOTRlZGY4NmVlNzQ4ODJhZDExMzQ0NTc0YzEyNDg4MDg0ZWU2YmZiMDA5MjU0N2QwNzQyNGFmYzQ0
https://api.ciscospark.com/v1/authorize?client_id=Cff5893294edf86ee74882ad11344574c12488084ee6bfb0092547d07424afc44&response_type=code&redirect_uri=http%3A%2F%2F0.0.0.0%3A5000%2Foauth&scope=spark%3Aall%20spark%3Akms&state=set_state_here

'''
auth_code_url="https://api.ciscospark.com/v1/authorize?client_id=Cff5893294edf86ee74882ad11344574c12488084ee6bfb0092547d07424afc44&response_type=code&redirect_uri=http%3A%2F%2F0.0.0.0%3A5000%2Foauth&scope=spark%3Aall%20spark%3Akms&state=set_state_here"

class webex_msg(object):
    webex_URL = 'https://api.ciscospark.com/v1/'
    #auth_header= "Bearer ZWYzYmUyMWYtZDM3OS00N2Y3LWJkMzctZDUzZmVhNDkwYzNmNTA5ODcyYzgtYTdi_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
    #auth_header= "Bearer YzZjMDFkOTAtNTcwYS00YzRiLTg2NzItOTcxYTZjMjk3MWZjMzk4MWU4NjQtZmMz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
    #auth_header = ("Bearer " + access_token) #Now that we have the bearer created dynamically.
    #headers= {'Authorization': auth_header, 'content-type' : content_type}

    def __init__(self,email_id):
        print("Webex Teams Object Instantiated\n URL={0}".format(webex_msg.webex_URL+path))
        self.email_id=email_id
        self.cxc_ais_teams_roomid=cxc_ais_teams_roomid

    def send_webex_message(self, message_text ):

        auth_header = ("Bearer " + access_token)  # Now that we have the bearer created dynamically.
        # This is  "Test Code" -Deliberately fuck up the access token to force a refresh by inserting an expireed one. 
        if not refreshed:
            print ("Setting false access token to test")
            auth_header = "Bearer ZWYzYmUyMWYtZDM3OS00N2Y3LWJkMzctZDUzZmVhNDkwYzNmNTA5ODcyYzgtYTdi_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"  # Test Access_Token

        headers = {'Authorization': auth_header, 'content-type': content_type}
        payload = {"roomId": self.cxc_ais_teams_roomid , "text": message_text}
        try:
            self.webex_request = requests.post(webex_msg.webex_URL + path, data=json.dumps(payload), headers=headers)
            self.webex_request.raise_for_status()
            return self.webex_request.status_code

        #Requests Expeption processing
        #This exception looks for a HTTPP status code 401. $01 means that the access token used was invalid or expireds. We use refresh_token to obtain another one.
        except requests.exceptions.HTTPError as e:
            print("Error {0}".format(e))
            if e.response.status_code==401:
                print("This is where we will refresh the token")
                self.refresh_token(message_text) #Did this so that I call retry the send message after refreshing the token.

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("Error {0}".format(e))

    def refresh_token(self,message_text):
        refresh_WT__access_token()
        self.send_webex_message(message_text)
        return self.webex_request.status_code



#This function authenticates the webex teams all using a Client_ID & Client Secret & Returns an Access token
#This is a two phase process:
#1. An orthorization code is first obtained (ask permission). This wil trigger a response to the redirect URL.
#2. An access token is obtained.
#As there is a HTTP handshake with Webex teams, any teams integration using authentication is required to have a web server.


#Step two of obtaining an access token. After auth_code (code) haqs been probided.
def get_WT_access_tokens(code,Client_ID,Secret_ID):
    global Access_code
    """Gets access token and refresh token"""
    print ("Access code {0} @ get_tokens".format(code))
    url = "https://api.ciscospark.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
                    "code={2}&redirect_uri={3}").format(Client_ID, Secret_ID, Access_code, redirect_uri)
    try:
        req = requests.post(url=url, data=payload, headers=headers)
        results = json.loads(req.text)
        print("Results from request for access token, Status Code {0}\n".format(req.status_code))
        global access_token
        access_token = results["access_token"]
        refresh_token = results["refresh_token"]
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Error {0}".format(e))

        #Write the access token and refresh token to the file that will be used later if app is restarted.
    try:
        with open(auth_parms_file,'w+') as auth_parms:
             auth_parms.write( "%s,%s,%s" %(access_token,refresh_token,Access_code))
    except:
        print("An Exception Occured writing to the Auth_parms_file{0}".format(sys.exc_info()[0]))

    return access_token, refresh_token

# This function is used to refresh the access token if it has expired. When that happens, an attempt is made to acquire another access token using the refresh token.
# We may combine get access_token and refresh_access token at some point, but wil keep it separate for now.
# Refer to https://developer.webex.com/docs/integrations

#Input Parameters: (Should all be in global variables)
#grant cobe set to refresh_token
#Client_id, Client_Secret
#Refresh_Token

def refresh_WT__access_token():
    global Client_ID, Secret_ID, Access_code, refresh_token, access_token, refreshed
    #print(" At Refresh access token - Code: {0} \t Client_ID {1} \t Client_Secret {2} \t Refresh Token {3} ".format(Access_code,Client_ID,Secret_ID,refresh_token))
    spark_url="https://api.ciscospark.com/v1/access_token"
    headers = {'accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded'}
    payload = ("grant_type=refresh_token&client_id={0}&client_secret={1}&"
               "refresh_token={2}").format(Client_ID, Secret_ID, refresh_token)

    try:
        req = requests.post(url=spark_url, data=payload, headers=headers)
        req.raise_for_status()
        results = json.loads(req.text)
        print("Results from Refresh access token, Status Code {0}\n".format(req.status_code))
        access_token = results["access_token"]
        refresh_token = results["refresh_token"]

    except requests.exceptions.HTTPError as e:
        print("Error {0}".format(e))
        if e.response.status_code == 400:
            print("This is where we need to open a web page to have the operator sign on to Webex teams and manualy obtain an access token")
            "Initiate a new browser window, pointing to the URL where operator needs to enter credentials to obtain an auth code"
            webbrowser.open(auth_code_url, new=1)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Error {0}".format(e))
        #Write the access token and refresh token to the file that will be used later if app is restarted.
    try:
        with open(auth_parms_file,'w+') as auth_parms:
             auth_parms.write( "%s,%s,%s" %(access_token,refresh_token,Access_code))
    except:
        print("An Exception Occured writing to the Auth_parms_file{0}".format(sys.exc_info()[0]))

    refreshed=True #Test code used in conjunstion wit send_webex_message to force a token refresh
    return access_token, refresh_token

#This function retrives parameters required for Webex team security and autherization; ClientID, Secret ID, acces-token, refresh token
def init_WT_security_parms():
    #Webex teams Cliend ID and SecretID have been stored as environment variables.
    global access_token, refresh_token,Client_ID, Secret_ID,Access_code
    try:
        Client_ID=environ.get('WT_CLIENT_ID')
        Secret_ID=environ.get('WT_SECRET_ID')
    except:
        print("Error retreiving environent variables")

    #if the above was succssful retreive the currently stored values for Access token and refresh token
    try:
        with open(auth_parms_file,'r') as auth_parms:
            auth_parms_data=auth_parms.read()
            access_token,refresh_token,Access_code=auth_parms_data.split(',')
            print("Access Token:{0} \t Refresh Token {1} \t Access_Code (From file)".format(access_token,refresh_token,Access_code))
    except:
        print("An Exception Occured {0}".format(sys.exc_info()[0]))
        print("Error Retreiving Access Token and Refresh token from a file")

    return  Client_ID,Secret_ID




'''
if __name__ == "__main__":
    x=webex_msg("daalberg@cisco.com")
    z=x.send_webex_message('This is a test message 3 building touch 10 integration')
    print("Status_code {0}".format(z))
'''



