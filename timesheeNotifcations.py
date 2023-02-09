import json
import frappe
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification
from frappe.utils import get_url_to_form, strip_html
from datetime import datetime, timedelta, date

# // --------------------------- Email Contant ------------------------------------

#def send email funcation
def send_an_email(user_email , doc_name):
    
    doc_link = get_url_to_form('Task', doc_name)
    subject = 'You did not create a timesheet for the task'
    recipients = user_email
    sender = 'nabaajafar2@gmail.com'
    message = f'Kindly create timesheet for the {doc_name} task '

    frappe.sendmail(
        recipients = user_email,
        subject = subject,
		template = "new_notification",
        sender = sender,
        message = message,
        reference_doctype = 'Task',
        reference_name = doc_name ,
        args = {
			'body_content':subject,
			'description': message,
			'document_type': 'Task',
			'document_name': doc_name,
			'doc_link': doc_link
		}
    )


# // ----------------- Notification for supervisor of the project after create task without timeshee --------------------------

def find_null_timesheet():
    timesheet_list = frappe.db.get_list("Task", filters={"act_start_date": ["<", "1900-01-01"]}, fields=["project", "creation","name"])
    all_timesheets = frappe.db.get_list("Timesheet", filters={"status":"Draft" } , pluck="name") # list of items
    for obj in all_timesheets : 
        counter = 0 
        take_doc = frappe.get_doc('Timesheet' , obj)
        take_task = take_doc.time_logs[0].task
        while counter < len(timesheet_list) : 
            if timesheet_list[counter]['name'] == take_task : 
                timesheet_list.pop(counter)
            counter +=1 

    # cleaned new timesheet_lsit 
    for t in timesheet_list:
        diff = datetime.utcnow() - t["creation"]
        if diff.days == -1:
            # get all supervisors
            project_doc = frappe.get_doc("Project", t["project"])
            supervisor_list = project_doc.spuervisors_box
            print(supervisor_list)
            for x in supervisor_list:
                supervisor_email = frappe.db.get_value("Employee", x.emp, ["company_email"])
                print(supervisor_email)
                send_an_email(supervisor_email , t["name"])
        



# // ----------------- Notification for operation manager (Reported to supervisord) after 2 days from creating task without timesheet --------------------------

def find_null_timesheet2():

    timesheet_list = frappe.db.get_list("Task", filters={"act_start_date": ["<", "1900-01-01"]}, fields=["project","name", "creation","act_start_date"])
    
    all_timesheets = frappe.db.get_list("Timesheet", filters={"status":"Draft" } , pluck="name") # list of items
    for obj in all_timesheets : 
        counter = 0 

        take_doc = frappe.get_doc('Timesheet' , obj)
        take_task = take_doc.time_logs[0].task
        while counter < len(timesheet_list) : 
            if timesheet_list[counter]['name'] == take_task : 
                timesheet_list.pop(counter) 
            counter +=1 

    # cleaned new timesheet_lsit 
 
   
    for t in timesheet_list:
        diff = datetime.utcnow() - t["creation"]
        if diff.days == 2:
            

            # get all supervisors
            supervisorss = []
            project_doc = frappe.get_doc("Project", t["project"])
            supervisor_list = project_doc.spuervisors_box
            for x in supervisor_list:
                supervisor = frappe.db.get_value("Employee", x.emp)
                supervisorss.append(supervisor)
            SM_email =[]
            for x in supervisorss:
                supervisor_manager = frappe.db.get_value("Employee", x, ["reports_to"])
                print(supervisor_manager)
                if supervisor_manager != None:
                    get_docm = frappe.get_doc('Employee' , supervisor_manager)
                    supervisor_manager_email = get_docm.company_email
                    print(supervisor_manager_email)
                    SM_email.append(supervisor_manager_email)
                else:
                    pass

                for email in SM_email:
                    if supervisor_manager != None:
                        send_an_email(email , t["name"])
                    else:
                        pass
            else:
                pass
        else:
            pass 


# // ----------------- Notification for operation manager role after 2 days from creating task without timesheet --------------------------


 def find_null_timesheet9():

     timesheet_list = frappe.db.get_list("Task", filters={"act_start_date": ["<", "1900-01-01"]}, fields=["project","name", "creation","act_start_date"])
    
     all_timesheets = frappe.db.get_list("Timesheet", filters={"status":"Draft" } , pluck="name") # list of items

     for obj in all_timesheets : 
         counter = 0 

         take_doc = frappe.get_doc('Timesheet' , obj)
         take_task = take_doc.time_logs[0].task
         while counter < len(timesheet_list) : 
             if timesheet_list[counter]['name'] == take_task : 
                 timesheet_list.pop(counter)
            
             counter +=1 

     # cleaned new timesheet_lsit 

     list_users = []
     users_roles = frappe.db.get_list('Has Role',filters={'role':('in',('Operation Manager')),'parenttype':'User'},fields={"parent"})
     for ins in users_roles :
         list_users.append(ins['parent']) 
     for t in timesheet_list:
         diff = datetime.utcnow() - t["creation"]
         if diff.days == 2:

             for email in list_users:
                 send_an_email(email , t["name"])
             else:
                pass
         else:
             pass 

 


# // ----------------- Notification for Senior operation manager SOM depending on the role --------------------------


def find_null_timesheet3():

    timesheet_list = frappe.db.get_list("Task", filters={"act_start_date": ["<", "1900-01-01"]}, fields=["project","name", "creation","act_start_date"])
    
    all_timesheets = frappe.db.get_list("Timesheet", filters={"status":"Draft" } , pluck="name") # list of items

    for obj in all_timesheets : 
        counter = 0 

        take_doc = frappe.get_doc('Timesheet' , obj)
        take_task = take_doc.time_logs[0].task
        while counter < len(timesheet_list) : 
            if timesheet_list[counter]['name'] == take_task : 
                timesheet_list.pop(counter)
            

            counter +=1 

    # cleaned new timesheet_lsit 

    list_users = []
    users_roles = frappe.db.get_list('Has Role',filters={'role':('in',('Senior Operation Manager')),'parenttype':'User'},fields={"parent"})
    for ins in users_roles :
        list_users.append(ins['parent']) 
    for t in timesheet_list:
        diff = datetime.utcnow() - t["creation"]
        if diff.days == 4:

            for email in list_users:
                send_an_email(email , t["name"])
            else:
                pass
        else:
            pass 





                       
