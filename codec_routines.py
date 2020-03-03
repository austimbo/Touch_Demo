#!/usr/bin/env python3
#This file contains all outbound connunication eoth the cocec.
from system_level_stuff import ip_of_machine
import requests
from requests.auth import HTTPBasicAuth
import sys
headers= {'content-type' : 'text/xml'}
cookies={}  #To be deleted after testing taking cookins from the codec object.
touch_serv_codecs={} # This isdictionary is a list of "codec_objects" there is one per codec.
                     # Codec objects contain all importat information about each codec in the system, so that it can be easily utilized.
                     # Accessed via touch_serv_codecs['codec_name']


#Class for a codec object:
class touch_serv_codec(object):
    def __init__(self,system_name):
        self.system_name=system_name
        self.userid=None
        self.password=None
        self.cookies={}
        self.system_mac=None
        self.system_ip=None

    def print_values(self):
        print("System Name: {0} \t UserID: {1} \t Password: {2} \t System Mac: {3} \t System IP: {4} \nCookie Jar:\n {5}\n\n".format(self.system_name, self.userid, self.password, self.system_mac, self.system_ip, self.cookies ))
        return "ok"

    #Later include methods to things such as the codec logimlogin

    #We can even move routimes that get the IP address etc into here.

    #Can even migrate calls to build button objects to here.


#Initialise the codec to send feedback to this machine on port 5000
''' The command when sent from tehconsole is:
    xcommand HTTPFeedback Register Feedback Slot :1 ServerURL: http://<this machine's IP address>/codec Expression
    "Event/UserInterface/Extensions/Widget
    '''

def init_codec(userid,password, CodecIP):
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
    response=post_to_codec(userid,password,"/putxml/",set_feedback, CodecIP)
    return response

def write_to_widget( userid, password, widget_id, widget_value, CodecIP):
    set_widget_value_xml='''
    <Command>
    <UserInterface>
        <Extensions>
          <Widget>
            <SetValue>
              <WidgetId>{0}</WidgetId>
              <Value>{1}</Value>
            </SetValue>
            </Widget>
        </Extensions>
    </UserInterface>
    </Command>'''.format(widget_id, widget_value)
    #print(set_widget_value_xml)  ##Test Code
    response = post_to_codec(userid, password, "/putxml/", set_widget_value_xml, CodecIP )
    return response


def set_room_control_screens(userid,password, CodecIP):
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
    response = post_to_codec(userid, password, "/putxml/", clear_room_cntl, CodecIP)
    # response = post_to_codec(userid, password, "/putxml/", room_ctl_xml)
    return response

def login_to_codec(userid,password, Codec_IP):
    #This function logs the app onto the codec and retreives the authentication cookie.
    #URL for beginning a session
    Auth_URL="/xmlapi/session/begin"
    #define a globally available variable called cookies
    response=post_to_codec(userid, password, Auth_URL,"",Codec_IP)
    global cookies
    cookies = response.cookies
    return cookies  #Return the cookie jar, so that it can be saved and later used again for this codec.


def post_to_codec(userid,password,URL_sfx,xml_data,CodecIP):
    #global CodecIP
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


#Function to retreive at information via a via HTTP GET
#make a basic get to retreive the codec information
#Note that get from codec has been modified. It builds the URL within get from codec.
#The only the specific location (parameter) information is imported via the URL_sfx
def get_from_codec(userid, password,URL_sfx, Codec_IP):
    auth = HTTPBasicAuth(userid, password)
    #global CodecIP
    auth = HTTPBasicAuth(userid, password)
    http_prefix = "http://{0}".format(Codec_IP)
    xml_get = "/getxml?location="
    URL = http_prefix + xml_get+ URL_sfx
    try:
        response = requests.get(URL, cookies=cookies, timeout=(2, 5), verify=False, headers=headers, auth=auth)
        print('Status Code: {0} for {1}'.format(response.status_code,URL))
        return response

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Error {0}".format(e))

    except:
        print("An Exception Occured {0}".format(sys.exc_info()[0]))

#Commandline to Write to a Touch10 pannel button in a codec is:
#xCommand UserInterface Extensions Widget SetValue WidgetId:"log_status" Value:"A big Smelly Fart"