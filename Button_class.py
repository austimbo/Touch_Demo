#!/usr/bin/env python3
#Thi file contains the classes fr each button in the pannel.
from codec_routines import get_from_codec
from lxml import etree, objectify
global userid, password #In the receiving module
from teams_integration import webex_msg
import Incident_manager
from Incident_manager import generate_incident


button_objects={} #This glbal Dictionary holds all opjefts pertaining to buttons.
#Build a button for each object.
#We will build the same object for each button in the system


class Roomctl_Button(object):

    def __init__(self): #widget_id,widget_value,widget_type):

        #Set up the required properties
        self.widget_id = None
        self.widget_value=None
        self.widget_type=None
        self.widget_action=None
        self.system_name=None
        self.system_mac=None
        self.system_ip=None
        self.incident_number=None
        self.button_busy=False
        self.widget_object_name=None
        self.sysem_site=None
        self.system_room=None

        #Maybe have a dictionary here that is a control block for each action
        #Identify what thpe of event it triggers on.
        #self.widget_action=temperature_cntrl_routine

    #learn the values from the button push
    #Dump out the Informtion from the pressed button.

    #Have methon actions associated with eachof the button events.
    #For Example Clicked

    def button_action(self):
    # Code executed when trigger events happen.
    #Remember not to put brackets
        if self.widget_action:
            self.widget_action(self.widget_id, self.widget_value, self.widget_type,self.system_name,self.system_ip,self.system_mac,self.widget_object_name)
            #Here we can decide on the different actions for different types, clicked (pressed released)


#this routine is called when the temperature button is called
def temperature_cntrl_routine(widget_id, widget_value, widget_type, system_name, system_ip, system_mac, widget_object_name):
    print("This is from the button routine\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))

#this routine is called when the temperature button is called
def beverage_help_routine(widget_id, widget_value, widget_type, system_name, system_ip, system_mac,widget_object_name):
    print("Beer required\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))
    if widget_type == "clicked":
        # Build a webex message object.
        x = webex_msg()
        # Generabe an incident object.
        incident_object_name = generate_incident(widget_object_name)
        # Generate an adaptive card. This uses a method in the incident object
        zz = Incident_manager.touch_buddy_incidents[incident_object_name].generate_incident_adaptive_card()
        # Send the message via Webex Teams
        z = x.send_webex_message(zz)
        # Print the status code to the console
        print("Status_code {0} Incident object name: {1}".format(z, incident_object_name))


#this routine is called when the temperature button is called
def tech_help_routine(widget_id, widget_value, widget_type, system_name, system_ip, system_mac, widget_object_name):
    print("Technical Help required\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))
    if widget_type == "clicked":
        #Build a webex message object.
        x=webex_msg()
        #Generabe an incident object.
        incident_object_name=generate_incident(widget_object_name)
        #Generate an adaptive card. This uses a method in the incident object
        zz=Incident_manager.touch_buddy_incidents[incident_object_name].generate_incident_adaptive_card()
        #Send the message via Webex Teams
        z=x.send_webex_message(zz)
        #Print the status code to the console
        print("Status_code {0} Incident object name: {1}".format(z, incident_object_name))


def catering_help_routine(widget_id, widget_value, widget_type, system_name, system_ip, system_mac, widget_object_name):
    print("Catering Help required\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type,))
    if widget_type == "clicked":
        # Build a webex message object.
        x = webex_msg()
        # Generabe an incident object.
        incident_object_name = generate_incident(widget_object_name)
        # Generate an adaptive card. This uses a method in the incident object
        zz = Incident_manager.touch_buddy_incidents[incident_object_name].generate_incident_adaptive_card()
        # Send the message via Webex Teams
        z = x.send_webex_message(zz)
        # Print the status code to the console
        print("Status_code {0} Incident object name: {1}".format(z, incident_object_name))

def log_help_routine(widget_id, widget_value, widget_type, system_name, system_ip, system_mac, widget_object_name):
    print("Logistics Help required\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))
    if widget_type == "clicked":
        # Build a webex message object.
        x = webex_msg()
        # Generabe an incident object.
        incident_object_name = generate_incident(widget_object_name)
        # Generate an adaptive card. This uses a method in the incident object
        zz = Incident_manager.touch_buddy_incidents[incident_object_name].generate_incident_adaptive_card()
        # Send the message via Webex Teams
        z = x.send_webex_message(zz)
        # Print the status code to the console
        print("Status_code {0} Incident object name: {1}".format(z, incident_object_name))

button_actions = {'temp_cntrl': temperature_cntrl_routine,
                  'bev_help': beverage_help_routine,
                  'tech_help' : tech_help_routine,
                  'catering_help': catering_help_routine,
                  'log_help': log_help_routine
                  }


#Here we instantiate an object for every widget/button defined in /userinterface/extensions
#The first step is to 'get' all defined widgets from 192.168.0.42/getxml?location=/status/userinterface/extensions.
#Next we retreive data regarding each widget and instantiate a "Roomctl_button object for each.

#Retreiving the userinterface/entension XML (Button/widget information)
def get_widget_xml(userid, password,Codec_IP):
    URL_suffix="/status/userinterface/extensions"
    response = get_from_codec(userid,password,URL_suffix,Codec_IP)
    #print(response.text)
    return response

#Retreive a bunch of ident paraeters that will uniquely identify this codec.
def get_some_xml(userid,password,url_suffix,Codec_IP):
    response=get_from_codec(userid,password,url_suffix,Codec_IP)
    return response

def extract_value_from_xml_t(xml_text_string,xml_path):
    # Change the response textr into an XML document/object
    response_xml_obj = etree.fromstring(xml_text_string.text)
    xml_text_value = response_xml_obj.find('./'+xml_path)
    return xml_text_value.text

def build_button_objects(xml_string_string,system_name,system_mac,system_ip,system_room,system_site):
    #First we take the text string returned to us from the codec.
    #Use etree fromstring to turn it into an etree object.
    response_xml_object = objectify.fromstring(xml_string_string)
    #Now we retreive all of the buttons from the object.
    #print(etree.tostring(response_xml_object,pretty_print=True))
    for elem in response_xml_object.getchildren(): #Just to step in over the first tag which is  <UserInterface>
        for widget in elem.Extensions.getchildren():
            #Here we pull back all interesting information about each button/widget
            if widget.WidgetId.text:
                widget_id=widget.WidgetId.text.lower()
            # Get the Item number of the widget:
                item_number = widget.attrib["item"]
                print("Widget_id is: {0}\tWidget Item_number is: {1}\n".format(widget_id, item_number))
            #Instantiate an Object for the widget/Button
                #Build the object name by appending _widget
                #In order to make this multi-codec appending system name and mac-address(might reduce this to just-mac is performance is an issue).
                #Note that we are replacing : with _ in mac address due to : causing a key error.
                widget_object_name =( "{0}_{1}_{2}_widget".format(system_name,system_mac.replace(":","_",5),widget_id)).lower()
                print("Creating {0}".format( widget_object_name))
                #Note that the button objects are stored in a dictionary called button_objects.
                #This was a recomendation in many foruns as it prevents the requirement to use 'eval' in building the objects,
                #Which was troubleome.
                button_objects[widget_object_name]= Roomctl_Button()
            #Set up actions for eqch of the buttons as well as identification parameters system_name & system_mac
            #So this is a bit complicated here we take the object that we just built & assign the nae of an action function/routine to it.
            #Both are looking up dictionaries to do so. SO a troubleshooting nughtmare.
                try:
                    button_objects[widget_object_name].widget_action = button_actions[widget_id]
                    button_objects[widget_object_name].system_name=system_name
                    button_objects[widget_object_name].system_ip = system_ip
                    button_objects[widget_object_name].system_mac = system_mac
                    button_objects[widget_object_name].widget_object_name = widget_object_name
                    button_objects[widget_object_name].system_room = system_room
                    button_objects[widget_object_name].system_site = system_site
                except KeyError:
                    print("Key Error, no routine defined for:  {0}\n".format(widget_id))

            else:
                print("XML Parse Error, No text in widgit id")

    return "ok"