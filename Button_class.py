#!/usr/bin/env python3
#Thi file contains the classes fr each button in the pannel.
from codec_routines import get_from_codec
from lxml import etree, objectify
global userid, password #In the receiving module
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
            self.widget_action(self.widget_id, self.widget_value, self.widget_type)
            #Here we can decide on the different actions for different types, clicked (pressed released)


#this routine is called when the temperature button is called
def temperature_cntrl_routine(widget_id, widget_value, widget_type):
    print("This is from the button routine\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))

#this routine is called when the temperature button is called
def beverage_help_routine(widget_id, widget_value, widget_type):
    print("Beer required\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))

#this routine is called when the temperature button is called
def tech_help_routine(widget_id, widget_value, widget_type):
    print("Technical Help required\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))

def catering_help_routine(widget_id, widget_value, widget_type):
    print("Catering Help required\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))

def log_help_routine(widget_id, widget_value, widget_type):
    print("Logistics Help required\n ID: {0}\t Value: {1}\t Type: {2}\n".format(widget_id,widget_value,widget_type))

button_actions = {'temp_cntrl': temperature_cntrl_routine,
                  'bev_help': beverage_help_routine,
                  'tech_help' : tech_help_routine,
                  'catering_help': catering_help_routine,
                  'log_help': log_help_routine
                  }


#Here we instantiate an object for every widget/button defined in /userinterface/extensions
#The first step is to 'get' all defined widgets from 192.168.0.42/getxml?location=/status/userinterface/extensions.
#Next we retreive data regarding each widget and instantiate a "Roomctl_button object for each.

#Retreiving the XML
def get_widget_xml(userid, password):
    URL_suffix="/status/userinterface/extensions"
    response = get_from_codec(userid,password,URL_suffix)
    #print(response.text)
    return response

def extract_value_from_xml(xml_text_string,xml_path):
    # Change the response textr into an XML document/object
    response_xml_obj = etree.fromstring(xml_text_string.text)
    xml_text_value = response_xml_obj.find('./'+xml_path)
    return xml_text_value

def build_button_objects(xml_string_string):
    #button_actions = {'temp_cntrl': temperature_cntrl_routine, 'bev_help': beverage_help_routine}
    #First we take the text string returned to us from the codec.
    #Use etree fromstring to turn it into an etree object.
    response_xml_object = objectify.fromstring(xml_string_string)
    #Now we retreive all of the buttone from the object.
    #print(etree.tostring(response_xml_object,pretty_print=True))
    for elem in response_xml_object.getchildren(): #Just to step in over the first tag whuch is  <UserInterface>
        for widget in elem.Extensions.getchildren():
            #Here we pul back all interesting information about each button/widget
            if widget.WidgetId.text:
                widget_id=widget.WidgetId.text.lower()
            # Get the Item number of the widget:
                item_number = widget.attrib["item"]
                print("Widget_id is: {0}\tWidget Item_number is: {1}\n".format(widget_id, item_number))
            #Instantiate an Object for the widget/Button
                #Build the object name by appending _widget
                widget_object_name = widget_id + "_widget"
                print("Creating {0}".format( widget_object_name))
                #Note that the button onjects are stored in a dictionary called button_objects.
                #This was a recomendation in many foruns as it prevents the requirement to use 'eval' in building the objects,
                #Which was troubleome.
                button_objects[widget_object_name]= Roomctl_Button()
            #Set up actions for eqch of the buttons
            #So this is a bit complicated here we take the object that we just built & assign the nae of an action function/routine to it.
            #Both are looking up dictionaries to do so. SO a troubleshooting nughtmare.
                try:
                    button_objects[widget_object_name].widget_action = button_actions[widget_id]
                except KeyError:
                    print("Key Error, no routine defined for:  {0}\n".format(widget_id))

            else:
                print("XML Parse Error, No text in widgit id")

    return "ok"