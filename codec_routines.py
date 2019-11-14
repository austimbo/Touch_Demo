#!/usr/bin/env python3
#This file contains all outbound connunication eoth the cocec.
from system_level_stuff import ip_of_machine
import requests
from requests.auth import HTTPBasicAuth
import sys
headers= {'content-type' : 'text/xml'}
cookies={}

#Initialise the codec to send feedback to this machine on port 5000
''' The command when sent from tehconsole is:
    xcommand HTTPFeedback Register Feedback Slot :1 ServerURL: http://<this machine's IP address>/codec Expression
    "Event/UserInterface/Extensions/Widget
    '''

def init_codec(userid,password):
    # Determine this machine's IP address
    IPAddr = ip_of_machine()
    set_feedback = '''
        <Command>  
            <HttpFeedback>
                <Register>
                    <FeedbackSlot>1</FeedbackSlot>
                    <ServerUrl>http://{0}:5000/codec</ServerUrl>
                    <Format>XML</Format>
                    <Expression item="1">/Event/UserInterface/Extensions/Widget</Expression>
                </Register>  
            </HttpFeedback>
        </Command>'''.format(IPAddr)
    response=post_to_codec(userid,password,"/putxml/",set_feedback)
    return response

def set_room_control_screens(userid,password):
    clear_room_cntl='''
        <Command>
            <UserInterface>
                <Extensions>
                    <Clear /> 
                </Extensions>
            </UserInterface>
        </Command> '''

    
    #open the file containing throom control definitions
    with open ("roomcontrolconfig.xml", "r") as room_ctl_file:
         room_ctl_xml=room_ctl_file.readlines()
         print(room_ctl_xml) # Just debug code.
         room_ctl_file.close()
    #now we will clear the the current room control pannel
    # this command lists all room control commands
    # xcommand UserInterface Extensions list
    # xCommand UserInterface Extensions Clear
    response = post_to_codec(userid, password, "/putxml/", clear_room_cntl)
    # response = post_to_codec(userid, password, "/putxml/", room_ctl_xml)
    return response

def login_to_codec(userid,password):
    #This function logs the app onto the codec and retreives the authentication cookie.
    #URL for beginning a session
    Auth_URL="/xmlapi/session/begin"
    #define a globally available variable called cookies
    response=post_to_codec(userid,password,Auth_URL,"")
    global cookies
    cookies = response.cookies


def post_to_codec(userid,password,URL_sfx,xml_data):
    global CodecIP
    auth = HTTPBasicAuth(userid, password)
    http_prefix="http://{0}".format(CodecIP)
    URL=http_prefix + URL_sfx
    try:
        response = requests.post(URL, cookies=cookies, timeout=(2, 5),data=xml_data,verify=False, headers=headers, auth=auth)
        print('Status Code: {0} for {1}'.format(response.status_code, URL))
        return response

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Error {0}".format(e))

    #except:
        print("An Exception Occured {0}".format(sys.exc_info()[0]))


