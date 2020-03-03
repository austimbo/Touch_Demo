#!/usr/bin/env python3
import json
import Button_class
import time
from codec_routines import write_to_widget
from codec_routines import touch_serv_codecs

incident_number=0
touch_buddy_incidents = {}

#This module is used to manage incident requests.
#Incidents happen when a meeting room ocupent presses a service request buttion requesting a particular type of assistance.
#When this iccurs, an incident object is created to track the incident througj to completion.
#All parameters relating to an incidet are stored in this object.


class touch_buddy_Incident(object):

    # Create Incident Function . This function is called directly by a button event. It
    # 1. Creates an event, capturing as much information as possible regarding the issue
    # 2. Generates a Microsoft adaptive card.
    # 3. Initiates the transmission of the card via Webex teams.

        def __init__(self,widget_object_name): #Set up an incident:
            #Set up the required properties
            self.indcident_number = 0
            self.incident_object_name=None
            self.status="Initial"
            self.created_time=None
            self.actioned_time=None
            self.resolved_time=None
            self.actioned_by_name=None
            self.actioned_by_phone = None
            self.actioned_by_email = None
            self.service_request_ada_card_json=None

            self.widget_object_name = widget_object_name
           #The widget ID that triggered the event.
            print("Widget Object (init) Name in {0} Incident nunmber: {1}".format(widget_object_name,self.widget_object_name))
           #Post button busy status in the button object
            Button_class.button_objects[self.widget_object_name].button_busy = True
           # Generate an incident number. (Base this in the widgit ID number
           # Get the widget_id of the button that iniated the incident(Influences the adaptive card)
            self.widget_id=Button_class.button_objects[self.widget_object_name].widget_id
            self.widget_status_field=self.widget_id+"_status"
           # 1. Codec Name (Should tell us the room)
            self.system_name = Button_class.button_objects[self.widget_object_name].system_name
           #The room that the requesting is originating from
            self.system_site = Button_class.button_objects[self.widget_object_name].system_site
            self.system_room = Button_class.button_objects[self.widget_object_name].system_room
           #Post the incident number into the button object.
            Button_class.button_objects[self.widget_object_name].incident_number=self.indcident_number
            self.CodecIP=touch_serv_codecs[self.system_name].system_ip

        def generate_incident_adaptive_card(self):
           #Build an adaptive card and store as text -nased JSON
            self.service_request_ada_card_json=adaptive_card_builder(self.incident_number, self.incident_object_name, self.system_room,self.system_site, self.widget_id)
            self.status = "Open"
            write_to_widget('admin', 'cisco', self.widget_status_field, "Incident {0} - Status {1}".format(self.incident_object_name, self.status), self.CodecIP)
            return self.service_request_ada_card_json

        #This method is accessed when an touch_buddy incident event event is acknowledged
        def Incident_acknowledget(self):
            #Set the status on the touch 10 that the event is acknowledged and provide details of the responder.
            self.status="Acknowledged"
            print("Acknowledging Incident Number: {0} Status: {1}".format(self.indcident_number, self.status))
            write_to_widget('admin', 'cisco', self.widget_status_field, "{0}  {1} {2} {3}".format(self.incident_object_name, self.status,self.actioned_by_name, self.actioned_by_phone),self.CodecIP)
            return "ok"








def generate_incident(widget_object_name): #Opens a touch buddy incident
    #Generate an incident object, to keep track of each incident.
    incident_number=generate_incident_number()
    incident_object_name="TBI"+ str(incident_number)
    print("Creating Incident object {0} for Widget {1}".format(incident_object_name, widget_object_name))
    #Create the incident object and store in an array.
    touch_buddy_incidents[incident_object_name]=touch_buddy_Incident(widget_object_name)
    #Tell the newly created object, which incident number it is representing.
    touch_buddy_incidents[incident_object_name].incident_number=incident_number
    touch_buddy_incidents[incident_object_name].status = "Open"
    #THere is probably a new elegant way to do this __something__ but WTF
    touch_buddy_incidents[incident_object_name].incident_object_name=incident_object_name
    # Generate a Timestamp
    seconds = time.time()
    touch_buddy_incidents[incident_object_name].created_time = time.ctime(seconds)
    return incident_object_name



#Routine to generate an incident number this might become more fancy later
def generate_incident_number():
    global incident_number
    incident_number +=1
    return incident_number


#This generic function builds the standard adaptive card for an incident and passent the dictionaly/or maybe the string back to calling function.

def adaptive_card_builder(incident_number, incident_name, system_room, system_site, widget_id):
    #Look up the incendent type from the below dictionary
    incident_type_dict={""
                        "log_help": "Logistics",
                        "tech_help": "Technical",
                        "catering_help" : "Catering",
                        "bev_help" : "Beverage"
                        }

    service_request_ada_card_dict = json.loads('''
                {
    	    "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vNGI3MGQ4ZTAtNGNjMC0xMWVhLTkyYjQtZDNjYjc0Nzc5ODAz",
    	    "markdown": "[Global Customer Experience Centres](https://www.cisco.com).,Customer Alerts Tasks Service",
    	    "attachments": [{
    	    	"contentType": "application/vnd.microsoft.card.adaptive",
    	    	"content": {
    	    		"$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    	    		"type": "AdaptiveCard",
    		    	"version": "1.0",
    			    "body": [{
    				    "type": "ColumnSet",
    				    "columns": [{
    					    	"type": "Column",
    						    "width": 2,
    		    				"items": [{
    			    					"type": "TextBlock",
    				    				"text": "Cisco GlobalCustomer Experience Centres ",
    					    			"weight": "bolder",
    						    		"size": "medium"
    				    			},
    				    			{
    					    			"type": "TextBlock",
    						    		"text": "Customer Alerts Tasks Service",
    					    			"isSubtle": true,
    					    			"size": "medium"
    					    		},
    						    	{
    						    		"type": "TextBlock",
    						    		"text": "",
    						    		"weight": "bolder",
    						    		"size": "small"
    						    	},
    						    	{
    						    		"type": "Input.Text",
    						    		"id": "incident_num",
    						    		"value": "",
    						    		"maxLength": 5,
    						    		"isVisible": false
    						    	}
    						    ]
    				    	},
    				    	{
    				    		"type": "Column",
    				    		"width": 1,
    				    		"items": [{
    				    			"type": "Image",
    				    			"url": "https://media.gettyimages.com/photos/people-pass-by-the-cisco-logo-at-the-2017-web-summit-in-lisbon-on-7-picture-id871337838?s=1024x1024",
    				    			"size": "auto"
    				    		}]
    				    	}
    		    		]
    		    	}],
    		    	"actions": [{
    		    		"type": "Action.Submit",
    		    		"title": "Acknowledge"
    		    	}]
    		    }
    	    }]
            } ''')
    service_request_ada_card_dict["attachments"][0]["content"]["body"][0]["columns"][0]["items"][2]["text"] = " {0} Assistance required in the {1} {2} Room \n Incident {3}".format(incident_type_dict[widget_id] , system_site, system_room, incident_name )
    #print(json.dumps(service_request_ada_card_dict,indent=4))
    service_request_ada_card_dict["attachments"][0]["content"]["body"][0]["columns"][0]["items"][3]["value"] = "TBI{0}".format(incident_number)
    return json.dumps(service_request_ada_card_dict)


