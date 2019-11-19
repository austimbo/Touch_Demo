#!/usr/bin/env python3


#This is the main module for the touch server application
#Include Modules

from flask import Flask, request
from lxml import etree
from codec_routines import login_to_codec #Did this to shorten the name
from codec_routines import init_codec
from codec_routines import set_room_control_screens
import codec_routines #Did this to access the local variables, like cookie Jar defined in codec_routines
from Button_class import Roomctl_Button
from Button_class import get_widget_xml
from Button_class import build_button_objects
from Button_class import button_objects
import inspect # Reason to be able to check if a class exists.
app = Flask(__name__)
app.config['DEBUG'] = False
userid="admin"
password="cisco"
codec_routines.CodecIP="192.168.0.42"


@app.route('/')
def index_url():

    return '<h1>Hello World</h1> \n <p>This is the Index page {0}</p>'

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
    action = xml_tree.xpath('/Event/UserInterface/Extensions/Widget/Action')
    #print(data_req)
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
                #I think that we are addressing the  <Value item="1">decrement</Value>
            if tag_1== 'value' and x.text:
                widget_value=x.text.lower()
                #print(tag_1,format(widget_value))
            if tag_1=='type' and x.text:
                widget_type=x.text.lower()
                #print(tag_1,format(widget_type))
        #This is the button Handler.
        #Rather than requiring to cycle through all of the button names we have previously built an object for each active button.
        #We check if there is a bidget ID field within an objet & if so if an object has been defined for it.
        # If so we take the values from the RX'd XML and store them in the object and then action it.
        # Note that object naems are constructed  as follows widget_id+"_widget"
        #Firt build a widget name:
        try:
            button_widget_name = widget_id + "_widget"
            #So now we address the correcponding already instantiated object build from the configuration. These are stored in an array called
            #button_objects[]
            widget_id and button_widget_name #Not sure if I need this and more.
            #print(type(button_objects[button_widget_name]))
            button_objects[button_widget_name].widget_id = widget_id
            button_objects[button_widget_name].widget_value=widget_value
            button_objects[button_widget_name].widget_type = widget_type
            button_objects[button_widget_name].button_action()  # Do whatever action is associated with the widget
            return "ok"
        except NameError:
            #Return anyway at this point although there was a name error
            return "ok"
    return "ok"

if __name__ == "__main__":

    #Login into the codec and save the authentication cookie
    login_to_codec(userid,password)
    #Initialize the feedback mechanism
    init_codec(userid,password)
    #Not going to do this right now, as the upload process is complicated
    #set_room_control_screens(userid,password)
    #**Instantiate the room controll buttons**.
    #Here we start to build the dynamic button objects.
    #Retreive the portion of the status containing the identity of each of the configured buttons.
    #http://<Codec IP>/getxml?location=status/userinterface/extensions
    codec_response= get_widget_xml(userid, password)
    #Need to eventually insert code to check that we got the correct xml code back.
    #No we process the received xml.
    #print(codec_response.text)
    #The below function builds a dynamic object for each button (Button_class.py)
    #If it has a name of Temp_cntrl its object will be call "temp_cntrl_widget"
    build_button_objects(codec_response.text)
    # Start the flask server to use the configured IP address of the interface.
    app.run(host="0.0.0.0", port=5000)


