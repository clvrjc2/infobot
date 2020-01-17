from datetime import datetime
import os
from messnger_syntax.bot import Bot
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
bot = Bot (ACCESS_TOKEN)

def set_column(users, sender_id,column, value):
    users.update({"user_id": sender_id},{"$set":{column : value}})
    
def find_user_id(users, user_object_id):
    # Convert from string to ObjectId:
    return users.find_one({'_id': ObjectId(user_object_id)}) 

# Has to use user_id since user has not existed
def user_exists(users, sender_id):
    user = users.find_one({'user_id': sender_id})
    if user is None:
        user_fb = bot.get_user_info(sender_id)#all information
        create_user(users, sender_id, user_fb)
        return False
    return True

def create_user(users, sender_id, user_fb):
    timestamp = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
    user_insert = {'user_id': sender_id, 
                    'created_at': timestamp,
                    'first_name':user_fb['first_name'],
                    'last_name':user_fb['last_name'],
                    'std_id':'None',
                    'last_message_ask':'None',
                    'last_message_answer':'None'
                   }
    users.insert(user_insert)
    
def get_data_users(table, sender_id):
    a = table.find_one({'user_id': sender_id})
    if a != None:
        return a
    return None   

def get_enrollment(table, category):
    a = table.find_one({'category': category})
    if a != None:
        return a
    return None
'''
def get_schedule_count(table, std_id):
    #,'sy': sy,'sem':sem
    a = table.find_one({'std_id':std_id}).count()
    if a != None:
        return a
    return None   '''
def get_schedule(table, std_id):
    #,'sy': sy,'sem':sem
    a = table.find_one( {'std_id':std_id})
    if a != None:
        return a
    return None   

def get_slip(table, std_id):
    #, 'sy': sy, 'sem':sem
    a = table.find_one({ 'std_id':std_id} )
    if a != None:
        return a
    return None   

def get_data(table, std_id):
    a = table.find_one({'std_id': std_id})
    if a != None:
        return a
    return None    

def update_user(student,std_id, ask, answer):
    student.update({"std_id": std_id},{"$set":{'std_id':std,'last_message_ask':ask,'last_message_answer':answer}})   

def student_enroll(student, sender_id):
    std = student.find_one({'sender_id': sender_id})
    if std is None:
        return False
    return True

def student_exists(student, std_id):
    std = student.find_one({ 'std_id': std_id})
    if std is None:
        return False
    return True

def create_enrollment(enrollment,schedules, requirements, fee, flow,category):        
    insert = { 'schedules':schedules,
                        'requirements': requirements,
                        'fee': fee,
                        'flow': flow,
                        'category': category
                        }
    enrollment.insert(insert)

def create_employee(employee,eid, name, department,designation):                     
    insert = { 'eid': eid,
                        'name': name,
                        'department': department,
                        'designation': designation
                        }
    employee.insert(insert)
    
def create_student(student,sender_id,std_id, name, guardian, contact, address, email):                     
    timestamp = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
    insert = { 'created_at': timestamp,
                        'sender_id':sender_id,
                        'name': name,
                        'std_id':std_id,
                        'contact': contact,
                        'address': address,
                        'email': email,
                        'guardian': guardian
                        }
    student.insert(insert)

def update_student(student,std_id, name, guardian, contact, address, email):
    student.update({"std_id": std_id},{"$set":{'name': name,'std_id':std_id, 'contact': contact,'address': address,'email': email,'guardian': guardian}})                      

    
def create_schedule(schedule, std_id, subject, day, time, room, unit, instructor,sy,sem):                     
    insert = { 'std_id': std_id,
                        'subject':std_id,
                        'day': day,
                        'time': time,
                        'room': room,
                        'unit': unit,
                        'instructor': instructor,
                        'sy': sy,
                        'sem': sem
                        }
    schedule.insert(insert)

def create_account(account, std_id, sy, sem, prelim, midterm, prefinal, final,total, amount_paid,balance, old_account):                     
    insert = { 'std_id': std_id,
                        'prelim': prelim,
                        'midterm': midterm,
                        'prefinal': prefinal,
                        'final': final,
                        'overall_total':total,
                        'amount_paid': amount_paid,
                        'balance': balance,
                        'old_account': sy,
                        'sy': sy,
                        'sem': sem
                        }
    account.insert(insert)

def create_exam(exam, std_id, subject, day, time, room, proctor,sy,sem):                     
    insert = { 'std_id': std_id,
                        'subject':std_id,
                        'day': day,
                        'time': time,
                        'room': room,
                        'proctor': proctor,
                        'sy': sy,
                        'sem': sem
                        }
    exam.insert(insert)
    
def get_scholarship(table):
    a = table.find({'status':'active'})
    if a != None:
        return a
    return None  
    
def create_scholarship(scholarship,requirements,name,description,status):                     
    insert = {      'requirements': requirements,
                        'name': name,
                        'description': description,
                        'status': status
                        }
    scholarship.insert(insert)
    
def get_scholarship(table):
    a = table.find()
    if a != None:
        return a
    return None  

def create_program(programs,requirements,name,description,department,status):                     
    insert = {          'requirements':requirements,
                        'name': name,
                        'description': description,
                        'department':department,
                        'status': status
                        }
    programs.insert(insert)
    
def get_program(table,department):
    a = table.find({'status':'active'},{'department':department})
    if a != None:
        return a
    return None   
    
def get_details(table):
    a = table.find()
    if a != None:
        return a
    return None      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
