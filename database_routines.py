#!/usr/bin/env python3
import os
import sqlite3

db_filename = 'cxc_incidents.db'
schema_filename = 'cxc_incidents_schema.sql'
db_is_new = not os.path.exists(db_filename)


#Function to insert data into a database table.

def create_incident_db_rec(record_dict):
    with sqlite3.connect(db_filename) as conn:
        c=conn.cursor()   #Create the curser
        sql="INSERT into cxc_incidents VALUES(:incident_object_name ,:status,:widget_id,:system_site,:system_room,:actioned_by_name," \
        ":created_time,:actioned_time,:resolved_time,:actioned_by_phone,:actioned_by_email)"
        c.execute(sql,record_dict)
        #Update the created time so we have a reference.
        c.execute("UPDATE cxc_incidents SET created_time = datetime('now', 'localtime' ) where rowid={0}".format(c.lastrowid))
        conn.commit()
    return c.lastrowid

def ch_incident_db_rec_status(record_dict):
    with sqlite3.connect(db_filename) as conn:
        #change_parms={'rec_no':record_no, 'new_status': record_dict.status}
        sql_open = "UPDATE cxc_incidents SET incident_object_name=(:incident_object_name), status=(:status)," \
                        "widget_id=(:widget_id), system_site=(:system_site), system_room=(:system_room)"\
                        "WHERE rowid=(:record_no)"
        sql_acknowledged = "UPDATE cxc_incidents SET status=(:status), actioned_time = datetime('now', 'localtime' ), actioned_by_name=(:actioned_by_name)," \
                           " actioned_by_email=(:actioned_by_email), actioned_by_phone=(:actioned_by_phone) " \
                           "WHERE rowid=(:record_no)"
        sql_resolved = "UPDATE cxc_incidents SET status=(:status), resolved_time = datetime('now', 'localtime' )" \
                           " WHERE rowid=(:record_no)"

        #sql_resolved = "UPDATE cxc_incidents SET status=(:new_status), actioned_time = datetime('now', 'localtime' ) WHERE rowid=(:rec_no)"
        status_sql={'Open' : sql_open, 'Acknowledged':sql_acknowledged, 'Resolved': sql_resolved }
        c=conn.cursor()
        #This is a bit tricky the SQL used for each status is selected from the status demoted in the record_dct[status] field
        c.execute(status_sql[record_dict['status']], record_dict)
        conn.commit()
    return c.lastrowid

#This is a gerneric querey function, that querey the database returning whatever is being requested.
def view_record_by_criteria(agent=None, system_site = None, record_no=0 ):
    with sqlite3.connect(db_filename) as conn:
        c = conn.cursor()
        querey_params={'system_site': system_site }
        querey_sql="select* from cxc_incidents where system_site=:system_site;"
        c.execute(querey_sql, querey_params)
        #Now we need to return many resords
        for display_record in c.fetchall():
            print("Status\t Type\tLocation\tRoom\tAgent\tCall Time\tActioned Time\tResolved Time\tAgent Phone\tAgent Email" )
            for field in display_record:
                print("{0}\t".format(field),end='')
    return "ok"

#This routing initializes the database.
#Its basically called in case the database file doesnt exist.
def incident_database_init():
    with sqlite3.connect(db_filename) as conn:
        print("InitializationRoutine {0}".format(db_filename))
        if db_is_new:
            print('Creating Database Schema {0}'.format(db_filename))
            with open(schema_filename, 'rt') as f:
                print("Inserting Values into DB")
                schema = f.read()
                conn.executescript(schema)
        else:
            c=conn.cursor()
            print ("Database filename {0} exists \n Last record ID={1}".format(db_filename, c.lastrowid))
    return


'''

if __name__ == "__main__":

    record_dict_0 ={ 'status' : 'Initial',
          'widget_id':'log_help',
          'system_site':'Roseville',
          'system_room':'Engineers Office',
          'actioned_by_name' :'',
          'created_time':'',
          'actioned_time' : "actioned_time" ,
          'resolved_time' :"resolved_time",
          'actioned_by_phone' : '',
          'actioned_by_email' : '',
          'record_no' : 0
          }

    record_dict_1 ={ 'status' : 'Acknowledged',
          'widget_id':'log_help',
          'system_site':'Artarmon',
          'system_room':'Engineers Office',
          'actioned_by_name' :'Daniele Alberghina',
          'created_time': 'created time',
          'actioned_time' : "actioned_time" ,
          'resolved_time' :"resolved_time",
          'actioned_by_phone' : "+61403590496",
          'actioned_by_email' : 'daalberg@cisco.com',
          'record_no' : 6
          }
    record_dict_2 = {'status': 'Resolved',
                     #'widget_id': 'log_help',
                     #'system_site': 'Artarmon',
                     #'system_room': 'Engineers Office',
                     #'actioned_by_name': 'farty farty',
                     #'created_time': 'created time',
                     #'actioned_time': "actioned_time",
                     'resolved_time': "resolved_time",
                     #'actioned_by_phone': "+61403590496",
                     #'actioned_by_email': 'fartyg@cisco.com',
                     'record_no': 6
                     }
#Try adding a record to the database.
    incident_database_init()
    #last_rec=create_incident_db_rec(record_dict_0)   #Create the initial record
    #print("Last Record after Inserting record {0}".format(last_rec))
    #last_rec=ch_incident_db_rec_status(record_dict_2)
    view_record_by_criteria(system_site="Roseville")

'''







        









'''
    conn.execute("""
        insert into cxc_incidents (:status , :widget_id, :system_site, :system_room, :actioned_by_name, :created_time, :actioned_time, :resolved_time, :actioned_by_phone, :actioned_by_email)
        values ('Open', 'log_help', 'Roseville', 'Engineers', 'jon law', "ctime", "actioned_time" "resolved_time", "+61403590496", )
        """)


def write_incident_to_db(incident_object_name):
    #insert into cxc_incidents
    return
    
    
#https://pymotw.com/2/sqlite3/

'''





