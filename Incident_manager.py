#!/usr/bin/env python3
import json
import Button_class
import time
from codec_routines import write_to_widget
from codec_routines import touch_serv_codecs
from database_routines import create_incident_db_rec
from database_routines import ch_incident_db_rec_status
import teams_integration

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

        def __init__(self,widget_object_name,incident_number, incident_object_name): #Set up an incident:
            #Set up the required properties
            self.incident_number = incident_number
            self.incident_object_name=incident_object_name
            self.status="Initial"
            self.created_time=None
            self.actioned_time=None
            self.resolved_time=None
            self.actioned_by_name=None
            self.actioned_by_phone = None
            self.actioned_by_email = None
            self.service_request_ada_card_json=None
            self.call_counter=0  #The number of times that the button has been pushed.

            self.widget_object_name = widget_object_name
           #The widget ID that triggered the event.
            print("Widget Object (init) Name in {0} Incident nunmber: {1}".format(self.incident_number, widget_object_name))
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
            Button_class.button_objects[self.widget_object_name].incident_number=self.incident_number
            self.CodecIP=touch_serv_codecs[self.system_name].system_ip
            #Generate Created a Timestamp
            seconds = time.time()
            self.created_time = time.ctime(seconds)

        def generate_incident_adaptive_card(self):
            #We only will build an adaptive card once for an incident object. That is when it is in an 'Initial" state.
            if self.status=='Initial':
            #Build an adaptive card and store as text -nased JSON
                self.service_request_ada_card_json=adaptive_card_builder(self.incident_number, self.incident_object_name, self.system_room,self.system_site, self.widget_id)
                x = teams_integration.webex_msg()
                zz = self.service_request_ada_card_json
                # Send the message via Webex Teams
                z = x.send_webex_message(zz)
                # Print the status code to the console
                print("Status_code {0} Incident object name: {1}".format(z, self.incident_object_name))
                #estroy the webex teams object.
                del z
                return self.service_request_ada_card_json

        #This method is accessed when an touch_buddy incident event event is acknowledged
        #This will eventually become depricated as we inplement incident_Change_status(status)
        def Incident_acknowledget(self): #Depricated
            #Set the status on the touch 10 that the event is acknowledged and provide details of the responder.
            self.status="Acknowledged"
            print("Acknowledging Incident Number: {0} Status: {1}".format(self.incident_number, self.status))
            write_to_widget('admin', 'cisco', self.widget_status_field, "{0}  {1} {2} {3}".format(self.incident_object_name, self.status,self.actioned_by_name, self.actioned_by_phone),self.CodecIP)
            return "ok"

        def incident_change_status(self,status):
            #Possible status's are currently Initia;, Open, Acknowledged, Closed
            #Initial is a very transient state and shouldnt be seen here.
            status_s={'Open':'Open', 'Acknowledged':'Acknowledged', 'Closed':'Closed'}
            # Is this a re-status - incident is already Open or already Acknowledged.
            #remember the previous status

            #First filter for known types
            # Set the self.status property within the incident.
            try:
                    self.status=status_s[status]
            except KeyError:
                    print("received an invalid status in change_status {}".format(status))
                    return

            #Count the number of times the button has been pushed.
            self.call_counter += 1

            #Take the appropraite action for that status change type.
            if self.status=='Open':
                widget_message='Incident: {0} - Status: {1} calls: {2}'.format(self.incident_object_name, self.status, self.call_counter)
                #Now lets do the needful to the database and change the status of the rerod to open
                # & insert other information that we know about.
                #This is a standard template.
                record_dict_open = {'status': 'Open',
                                 'incident_object_name' : self.incident_object_name,
                                 'widget_id': self.widget_id,
                                 'system_site': self.system_site,
                                 'system_room': self.system_room,
                                 'actioned_by_name': '',
                                 'created_time': '',  #Placeholder taken care of in the function.
                                 'actioned_time': 'actioned time', #These times are just placeholders.
                                 'resolved_time': "resolved_time", #These times are just placeholders.
                                 'actioned_by_phone': '',
                                 'actioned_by_email': '',
                                 'record_no': self.incident_number #Important primary key
                                 }
                lastrowid=ch_incident_db_rec_status(record_dict_open)

            if self.status == 'Acknowledged':
                widget_message="{0} {1} {2} {3} {4}  ".format(self.status, self.incident_object_name,  self.actioned_by_name, self.actioned_by_phone, self.call_counter)
                record_dict_acknowldged  = {'status': 'Acknowledged',
                                 'incident_object_name': self.incident_object_name,
                                 'widget_id': '',
                                 'system_site': '',
                                 'system_room': '',
                                 'actioned_by_name': self.actioned_by_name,
                                 'created_time': '', #Placeholder taken care of in the function.
                                 'actioned_time': '', # Actioned Time will be updated within the function
                                 'resolved_time': '',
                                 'actioned_by_phone': self.actioned_by_phone,
                                 'actioned_by_email': self.actioned_by_email,
                                 'record_no': self.incident_number
                                 }
                lastrowid = ch_incident_db_rec_status(record_dict_acknowldged )

            if self.status == 'Resolved':
                widget_message="{0} {1} {2} {3} {4} ".format(self.status, self.incident_object_name,  self.actioned_by_name, self.actioned_by_phone, self.call_counter)

            # Write status chenge to the database (Future) haha it is here now!
                record_dict_resolved = {'status': 'Resolved',
                             'widget_id': '',
                             'system_site': '',
                             'system_room': '',
                             'actioned_by_name': '',
                             'created_time': '',
                             'actioned_time': '',
                             'resolved_time': "resolved_time", #Placeholder taken care of in the function.
                             'actioned_by_phone': '',
                             'actioned_by_email': '',
                             'record_no': self.incident_number
                             }
                lastrowid = ch_incident_db_rec_status(record_dict_resolved)
                #Here we need to fee up button busy etc sy that the same button can used for its next call.
                Button_class.button_objects[self.widget_object_name].button_busy = False
        #Write the message built above to appropraite touch 10 widget
            print("{0} {1}".format(widget_message,self.created_time))
            write_to_widget( touch_serv_codecs[self.system_name].userid, touch_serv_codecs[self.system_name].password, self.widget_status_field, widget_message, self.CodecIP)
            return "ok"

def generate_incident(widget_object_name): #Opens a touch buddy incident
    #Generate an incident object, to keep track of each incident.
    #Check ig there is already an incident already outstanding for this object.
    #if there is an incident outstanding for this button/widget, there will be an incident id in the button object.
    if Button_class.button_objects[widget_object_name].button_busy:
        #Means that there is an outstanding incident already. No Need to generate another incident.
        #We will just update Just call the press count.
        #Here we are experiencing a re-status situation . We will in future re-write the status with an updates counter
        print("Re-status condition being experienced on {0}".format(widget_object_name))
        #We will do an incident status re-write with the same status
        incident_object_name="TBI" + str(Button_class.button_objects[widget_object_name].incident_number)
        print("Re-Status Condition {0}".format(incident_object_name))
        #Not the best way to do it but rewriting the current status bact to the incident object to increment the calls counter.
        touch_buddy_incidents[incident_object_name].incident_change_status(touch_buddy_incidents[incident_object_name].status)
    else:
        #Insert record into the database here
        #Use lastrow ID from the DB instead of generating the incident number
        #Fill in the following fields with what we know about the incident so far.

        record_dict_create = {'status': 'Initial',
                         'incident_object_name': '',
                         'widget_id': 'log_help',
                         'system_site': '',
                         'system_room': '',
                         'actioned_by_name': '',
                         'created_time': '', #Taken care of in the database routine
                         'actioned_time': "actioned_time",
                         'resolved_time': "resolved_time",
                         'actioned_by_phone': '',
                         'actioned_by_email': '',
                         'record_no': 0
                         }
        incident_number=create_incident_db_rec(record_dict_create) #Except we are best to create a cresh DB conn each time.
        #incident_number=generate_incident_number()
        incident_object_name="TBI"+ str(incident_number)
        print("Creating Incident object {0} for Widget {1}".format(incident_object_name, widget_object_name))
        #Create the incident object and store in an array.
        # Tell the newly created object, which incident number it is representing & all that shit
        touch_buddy_incidents[incident_object_name]=touch_buddy_Incident(widget_object_name,incident_number,incident_object_name)

        ##Need to swap these two calls in order to provide the user with a faster response on the touch 10.
        #Generate and send a microsoft adaptive card via Webex Teams
        touch_buddy_incidents[incident_object_name].generate_incident_adaptive_card()
        #Set the incident status to open, this will trigger all events that happen an incident is opened.
        #Including database events
        touch_buddy_incidents[incident_object_name].incident_change_status('Open')
    return incident_object_name  #Returns to button_class



##To be Depricated this function is now replaced by the last row in the DB.
#Routine to generate an incident number this might become more fancy later
#THis function to be depricated as the database now provides the invident number from the last rocord id inserted.
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


