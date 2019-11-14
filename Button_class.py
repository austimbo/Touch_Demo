#!/usr/bin/env python3
#Thi file contains the classes fr each button in the pannel.

#Build a button for each object.
#We will build the same object for each button in the system
class Roomctl_Button(object):

    def __init__(self): #widget_id,widget_value,widget_type):
        self.widget_value=None
        self.widget_type=None
        #Maybe have a dictionary here that is a control block for each action
        #Identify what thpe of event it triggers on.
        self.widget_action=temperature_cntrl_routine

    #learn the values from the button push
    #Dump out the Informtion from the pressed button.

    #Have methon actions associated with eachof the button events.
    #For Example Clicked

    def button_action(self):
    # Code executed when trigger events happen.
    #Remember not to put brackets
        self.widget_action(self.widget_value,self.widget_type)

#this routine is called when the temperature button is called
def temperature_cntrl_routine(widget_value,widget_type):
    print("This is from the button routine\n Value {0}\t Type {1}\n".format(widget_value,widget_type))