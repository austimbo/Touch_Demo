#!/usr/bin/env python3


#This is the main module for the touch server application
#Include Modules

from flask import Flask, request, render_template
from lxml import etree
from codec_routines import login_to_codec #Did this to shorten the name
from codec_routines import init_codec
from codec_routines import set_room_control_screens
from codec_routines import touch_serv_codecs as touch_serv_codecs
from codec_routines import touch_serv_codec
import codec_routines #Did this to access the local variables, like cookie Jar defined in codec_routines
from Button_class import Roomctl_Button
from Button_class import get_widget_xml
from Button_class import build_button_objects
from Button_class import get_some_xml
from Button_class import button_objects
from Button_class import extract_value_from_xml_t
import teams_integration
from teams_integration import get_WT_access_tokens
from teams_integration import init_WT_security_parms
from teams_integration import process_card_ack
import time
import inspect # Reason to be able to check if a class exists.
import os
app = Flask(__name__)
app.config['DEBUG'] = False
userid="admin"
password="cisco"
#codec_routines.CodecIP="192.168.0.42"
codec_file="codecs.txt"





#redirect_uri = "http://0.0.0.0:5000/oauth"



@app.route('/')
def index_url():
     return render_template("index.html")
     #'<h1>Hello World</h1> \n <p>This is the Index page {0}</p>'

@app.route('/webhooks', methods=['POST', 'GET' ] ) #URL that webhooks hit
def webhooks():
    print("yo got a webhook!!!")
    print (request.json)  #Dumps out the entire data field.
    card_ack_json=request.json #Get ready to process in the teams_integrtation module.
    process_card_ack(card_ack_json)
    return "ok"

@app.route('/oauth', methods=['POST', 'GET' ] ) #Endpoint acting as Redirect URI. Redirected tohere after requesing permission.
def oauth():
    """Retrieves oauth code in readiness to generate tokens for users"""
    global code #Turn code to a global, as its also required when refreshing a token.
    if "code" in request.args:  # and state == "YOUR_STATE_STRING":
        state = request.args.get("state")  # Captures value of the state.
        teams_integration.Access_code = request.args.get("code")  # Captures value of the code.
        print("OAuth code: {0}".format(teams_integration.Access_code))
        print("OAuth state: {0}".format(state))
    #Lets retreive the token from Webext teams ath.
        teams_integration.access_token, teams_integration.refresh_token = get_WT_access_tokens(teams_integration.Access_code,teams_integration.Client_ID,teams_integration.Secret_ID)
    #Still need some sort of error handling here. Might also set token values within in the functiom & error out on a bad status code.
    else:
        print("Didn't Receve a respomse when requesting an access token")
        return "Error"
    return render_template("granted.html")

#This is the URL set to sent feedback to in the codec
@app.route('/codec', methods=['POST', 'GET' ])
def codec_url():
    #Decode the data
    data_req=request.data.decode('utf-8')
    app.logger.info('headers:{}'.format(request.headers))
    app.logger.info('values:{}'.format(data_req))

    #Build an XML Object
    xml_tree=etree.fromstring(data_req)
    #Look for a tag called action
    #print(data_req)
    #Here we retreive the system nam, IP and mac addresse from the Ident tag
    ident=xml_tree.xpath('/Event/Identification')
    if ident:
        for z in ident[0].iter():
            tag_z=z.tag.lower()
            if tag_z=='systemname' and z.text:
                system_name=z.text
            if tag_z == 'ipaddress' and z.text:
                system_ip=z.text
            if tag_z=='macaddress' and z.text:
                system_mac=z.text
    action = xml_tree.xpath('/Event/UserInterface/Extensions/Widget/Action')
    if action:
        #First reset the widget value as this will change frequesntly
        widget_value= None
        for x in action[0].iter():
            #We are pointing to 'action' tag
            # Look at the tag lower than action
            tag_1=x.tag.lower()
            #Check if it is populated with text
            #Check if the tag is called widgetid & has test
            if tag_1=='widgetid' and x.text:
                #If it is the tag below it should be 'widgetname', save that <WidgetId item="1">widget_10</WidgetId>
                widget_id=x.text.lower()
                #print(tag_1, format(widget_id))
            if tag_1== 'value' and x.text:
                widget_value=x.text.lower()
                #print(tag_1,format(widget_value))
            if tag_1=='type' and x.text:
                widget_type=x.text.lower()
                #print(tag_1,format(widget_type))
        #This is the button Handler.
        #Rather than requiring to cycle through all of the button names we have previously built an object for each active button.
        #We check if there is a widget ID field within an objet & if so if an object has been defined for it.
        # If so we take the values from the RX'd XML and store them in the object and then action it.
        # Note that object naems are constructed  as follows widget_id+"_widget"
        #Firt build a widget name:
        try:
            button_widget_name = ("{0}_{1}_{2}_widget".format(system_name, system_mac.replace(":","_",5), widget_id)).lower()
            #So now we address the correcponding already instantiated object build from the configuration. These are stored in an array called
            widget_id and button_widget_name #Not sure if I need this and more.
            button_objects[button_widget_name].widget_id = widget_id
            button_objects[button_widget_name].widget_value=widget_value
            button_objects[button_widget_name].widget_type = widget_type
            button_objects[button_widget_name].button_action()  # Do whatever action is associated with the widget
            return "ok"
        #except NameError:
        except KeyError:
            #Return anyway at this point although there was a name error
            print("There was a key error. Not able to find a match to the system name in button_objects[{0}].widget_id = {1}".format(button_widget_name),widget_id)
            return "ok"
    return "ok"

if __name__ == "__main__":

    # open the file contining information for all of the codes.
    with open( codec_file, 'r') as codec_info_f:
        print ("Absolute path is: {0}".format(os.path.abspath(codec_file)))
        for codec_csv in codec_info_f:    #Do all of this stuff for each codec in the list.
            # Now we need to split of the fields in the file
            print("Codec CSV read is: {0} ".format(codec_csv))
            CodecIP, userid, password, system_room, system_site = codec_csv.split(",")
            print("Current Codec is  (from file) ip: {0} \t Userid: {1} \t Password {2} \t Room: {3} \t System Site: {4}\n".format(CodecIP, userid, password, system_room, system_site))
            #Login into the codec and save the authentication cookie
            cookies=login_to_codec(userid, password, CodecIP)
            #Initialize the feedback mechanism
            init_codec(userid, password, CodecIP)
    #Not going to do this right now, as the upload process is complicated and not easily automated
    #set_room_control_screens(userid,password)

            #Retreive the portion of the status containing the identity of each of the configured buttons.
            #Firstly the System Name
            contact_parameters = get_some_xml(userid, password, "/status/userinterface/contactinfo",CodecIP)
            system_name = extract_value_from_xml_t(contact_parameters, "/ContactInfo/Name")
            #Then The mac address
            network_parameters=get_some_xml(userid,password,"/status/network",CodecIP)
            #Extract identification parameters from the currently addressed codec.
            system_mac=extract_value_from_xml_t(network_parameters,"/Network/Ethernet/MacAddress")
            system_ip=extract_value_from_xml_t(network_parameters,"/Network/IPv4/Address")
            #http://<Codec IP>/getxml?location=status/userinterface/extensions
            system_widgets=get_widget_xml(userid, password,CodecIP)
            #Need to eventually insert code to check that we got the correct xml code back.
            #Now we process the received xml.
            print("From Main Loop\n System Name: {0}\t System Mac: {1} System IP: {2}\n\n".format(system_name, system_mac, system_ip))
            #The below function builds a dynamic object for each button (Button_class.py)
            #If it has a name of Temp_cntrl its object will be call "temp_cntrl_widget"
            #Maybe later Build Button Objects can be called from a method on each codec object.
            build_button_objects(system_widgets.text, system_name, system_mac, system_ip, system_room, system_site)
            #Build the codec object for this codec. Will eventually move more functionality over to here.
            #instantiate a codec object
            touch_serv_codecs[system_name] = touch_serv_codec(system_name)
            #System name
            touch_serv_codecs[system_name].system_name=system_name
            #Credentials
            touch_serv_codecs[system_name].userid=userid
            touch_serv_codecs[system_name].password=password
            #Cookie Jar containing authentication hash.
            touch_serv_codecs[system_name].cookies = cookies
            #Networking information.
            touch_serv_codecs[system_name].system_mac=system_mac
            touch_serv_codecs[system_name].system_ip = system_ip
            #Print out important information about the Codeec just processes.
            touch_serv_codecs[system_name].print_values()



            #Initialise Webex teams security/Autherization parameters - Secret ID Client ID etc.
    Client_ID, Secret_ID=init_WT_security_parms()
    #Maybe set up the web hooks here.
    print("Client_ID: {0}\t Secret_ID: {1} (From Environment variables)".format(Client_ID,Secret_ID))
    # Start the flask server to use the configured IP address of the interface.
    app.run(host="0.0.0.0", port=5000)


