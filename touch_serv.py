#!/usr/bin/env python3


#This is the main module for the touch server application
#Include Modules

from flask import Flask, request
from lxml import etree
from codec_routines import login_to_codec #Did this to shorten the name
from codec_routines import init_codec
from codec_routines import set_room_control_screens
import codec_routines #Did this to access the local variables, like cookie Jar defined in codec_routines
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
                print(tag_1, format(widget_id))
                #I think that we are addressing the  <Value item="1">decrement</Value>
            if tag_1== 'value' and x.text:
                widget_value=x.text.lower()
                print(tag_1,format(widget_value))
            if tag_1=='type' and x.text:
                widget_type=x.text.lower()
                print(tag_1,format(widget_type))
        return "ok"

if __name__ == "__main__":

    #Login into the codec and save the authentication cookie
    login_to_codec(userid,password)
    #Initialize the feedback mechanism
    init_codec(userid,password)
    #Not going to do this right now, as the upload process is complicated
    #set_room_control_screens(userid,password)
    # Start the flask server to use the configured IP address of the interface.
    app.run(host="0.0.0.0", port=5000)


