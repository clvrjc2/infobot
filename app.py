#Libraries to be import START
import random
from flask import Flask, request
from messnger_syntax.bot import Bot
import os
import json
import pymongo
from pymongo import MongoClient
import Mongo#import Mongo.py
from NLU import nlp
from collections import Counter #install collections
import datetime
#Libraries to be import END

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
MONGO_TOKEN = os.environ['MONGO_DB']

bot = Bot (ACCESS_TOKEN)
cluster = MongoClient(MONGO_TOKEN)
db = cluster["ACLC"]
users = db["users"]
student = db["student"]
account_slip = db["accountslip"]
enrollment = db["enrollment"]
employee = db["employee"]
exam = db["examschedule"]
schedule = db["myschedule"]
programs = db["programs"]
scholarship = db["scholarship"]

now = datetime.now()
d = datetime.datetime.strptime(now, "%d %b %Y  %H:%M:%S.%f")

image_url = 'https://raw.githubusercontent.com/clvrjc2/drpedia/master/images/'
GREETING_RESPONSES = ["Hi", "Hey", "Hello there", "Hello", "Hi there"]
#enrollment
frequirements = ''
ffee = ''
fflow = ''
trequirements = ''
tfee = ''
tflow = ''
orequirements = ''
ofee = ''
oflowcategory = ''
schedule = ''
#employee
eid = ''
ename = ''
department = ''
designation = ''
#users
std_id = ''
ask = ''
answer = ''
#student
name = '' 
guardian = '' 
contact = '' 
address = '' 
email = ''
#schedule
subject = '' 
day = '' 
time = '' 
room = '' 
unit = '' 
instructor = ''
sy = ''
sem = ''
#account
sy = ''
sem = '' 
prelim = '' 
midterm = ''
prefinal = ''
final = ''
amount_paid = ''
balance = ''
old_account = ''
#exam
subject = '' 
day = '' 
time = '' 
room = ''
proctor = ''
sy = ''
sem = ''
#scholarship
screq = ''
sname = ''
sdescription = ''
sstatus = ''
#programs SIS TESDA COLLEGE
pame = ''
pdescription = ''
pdepartment = ''
pstatus = ''

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		"""Before allowing people to message your bot, Facebook has implemented a verify token
		that confirms all requests that your bot receives came from Facebook.""" 
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	#if the request was not get, it must be POST and we can just proceed with sending a message back to user
	else:
		# get whatever message a user sent the bot
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					#Facebook Messenger ID for user so we know where to send response back to
					sender_id = message['sender']['id']
					user_data = Mongo.get_data_users(users, sender_id)
					patient_data = Mongo.get_data_patient(patient, sender_id)
		
					if message['message'].get('text'):
						if message['message'].get('quick_reply'):
							received_qr(message)  
						else: #else if message is just a text
							received_text(message)
					#if user sends us a GIF, photo,video, or any other non-text item
					elif message['message'].get('attachments'):
						#TO BE EDIT
						#bot.send_text_message(sender_id,get_message())
						pass
				elif message.get("postback"):  # user clicked/tapped "postback" button in earlier message
					received_postback(message)
					
	return "Message Processed"

#if user send a message in text
def received_text(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	text = event["message"]["text"]
	
	'''
	Mongo.update_user(student,std_id, ask, answer)
	Mongo.create_student(student,std_id, name, guardian, contact, address, email) 
	Mongo.create_schedule(schedule, std_id, subject, day, time, room, unit, instructor,sy,sem)
	Mongo.update_student(student,std_id, name, guardian, contact, address, email)
	Mongo.create_account(account, std_id, sy, sem, prelim, midterm, prefinal, final, amount_paid,balance, old_account)
	Mongo.create_exam(exam, std_id, subject, day, time, room, proctor,sy,sem)
	Mongo.create_scholarship(scholarship,name,description,status)      
	Mongo.create_program(programs,name,description,department,status)
	Mongo.create_enrollment(enrollment,schedules, requirements, fee, flow,category)
	Mongo.create_employee(employee,eid, name, department,designation)
	Mongo.get_data_users(users, sender_id)
	Mongo.get_data(table, std_id)
	Mongo.get_details(table)
	'''
	global schedules, frequirements, ffee, fflow,trequirements, tfee, tflow,orequirements, ofee, oflow,category#enrollment    
	global eid, ename, department,designation#employee
	global ask,answer,std_id #users
	global name, guardian, contact, address, email #student
	global subject, day, time, room, unit, instructor,sy,sem #schedule
	global sy, sem, prelim, midterm, prefinal, final, amount_paid,balance, old_account  #account
	global subject, day, time, room, unit, proctor,sy,sem    #exam
	global sname,description,status, sreq #scholarship
	global pame,description,department,status #programs SIS TESDA SENIOR HIGH
	#users
	user_data = Mongo.get_data_users(users, sender_id)
	#student_data = Mongo.get_data(student, std_id) for verification
	if user_data !=None:
		ask = user_data['last_message_ask']
		answer = user_data['last_message_answer']
	else: 
		pass
	
	if ask == 'student?' and answer == 'yes_student':
		if Mongo.student_exists(student, text):
			quick_replies = {"content_type":"text","title":"Enrollment","payload":"enrollment"},{"content_type":"text","title":"Schedule","payload":"schedule"},{"content_type":"text","title":"Account Slip","payload":"account_slip"},{"content_type":"text","title":"Exam Schedule","payload":"exam_schedule"},{"content_type":"text","title":"Scholarship","payload":"scholarship"},{"content_type":"text","title":"Others","payload":"others"}
			bot.send_quick_replies_message(sender_id, 'What can I do for you?', quick_replies)
		else:
			bot.send_text_message(sender_id,'Invalid ID number, please try again.')
	if answer == 'enrollment':
		bot.send_text_message(sender_id, 'Just click the Send Requirements Button')
		bot.send_quick_replies_message(sender_id, 'Get Requirements',  [{"content_type":"text","title":"Send Requirements","payload":"requirements"}])
	if answer == 'requirements':
		bot.send_text_message(sender_id, 'Simply click the buttons')
		quick_replies = {"content_type":"text","title":"Freshmen","payload":"freshmen"},{"content_type":"text","title":"Transferee","payload":"transferee"},{"content_type":"text","title":"Old Student","payload":"old"}
		bot.send_quick_replies_message(sender_id, 'Requirements for ?', quick_replies)
	if answer == 'freshmen':
		bot.send_text_message(sender_id, 'Just click the Send Enrollment Fee Button')
		bot.send_text_message(sender_id, 'For other matters simply click the start over button in the persistent menu')
		bot.send_quick_replies_message(sender_id, 'Enrollment Fee?',  [{"content_type":"text","title":"Send Enrollment Fee","payload":"fee"}])
	if answer == 'transferee':
		bot.send_text_message(sender_id, 'Just click the Send Enrollment Fee Button')
		bot.send_text_message(sender_id, 'For other matters simply click the start over button in the persistent menu')
		bot.send_quick_replies_message(sender_id, 'Enrollment Fee?',  [{"content_type":"text","title":"Send Enrollment Fee","payload":"fee"}])
	if answer == 'old':
		bot.send_text_message(sender_id, 'Just click the Send Enrollment Fee Button')
		bot.send_text_message(sender_id, 'For other matters simply click the start over button in the persistent menu')
		bot.send_quick_replies_message(sender_id, 'Enrollment Fee?',  [{"content_type":"text","title":"Send Enrollment Fee","payload":"fee"}])

	'''		
	if ask == "agree and proceed?" and answer == "see_details":
		oneqrbtn = [{"content_type":"text","title":"🤝Agree and proceed","payload":'ready_accept'}]
		bot.send_quick_replies_message(sender_id, 'Ready to go?', oneqrbtn)
		
	if ask == "check symptoms":
		oneqrbtn = [{"content_type":"text","title":"Check Symptoms 🔍","payload":'check_symptoms'}]
		bot.send_quick_replies_message(sender_id, 'How can I assist you today {}?\nI can check your/your childs symptoms🔍 and provide you pre-emptive medication afterwards.'.format(fname), oneqrbtn)
	
	inputs = nlp.nlp(text)
	if inputs != 'Invalid':
		pass
	else:
		x =["Im sorry, humans are complicated, I'm not trained to understand things well","Sorry, I did't quite follow that, perhaps use different words?","Sorry, I did't quite follow that, maybe use different words?"]
		bot.send_text_message(sender_id,random.choice(x))
	'''		

def send_remedies(sender_id,symptoms):
	patient_symptoms = list(symptoms.split(","))
	len_ps = len(patient_symptoms)
	elements = []
	if len_ps > 2:
		print(len_ps)
		for x in range(0,len_ps-1):
			rest = patient_symptoms[x].replace(" ","").replace("/","").replace("-","").replace(",","")
			elements.append({"title":patient_symptoms[x].capitalize(),"image_url":image_url +rest+'.png',"subtitle":"If symptom persist or worsen get a doctor's consultation.","buttons":[{"type":"postback","title":"More Details","payload":rest+"_about"},{"type":"postback","title":"Remedies","payload":rest+"_remedies"}]},)
			if x == len_ps-1:
				break
		else:
			bot.send_generic_message(sender_id, elements)
	elif len(patient_symptoms) == 2:
		ps = patient_symptoms[0]

		rest = ps.replace(" ","").replace("/","").replace("-","").replace(",","")
		print(ps,len(patient_symptoms),rest)
		elements = [
				 {
				  "title":ps.capitalize(),
				  "image_url":image_url +rest+'.png',
				  "subtitle":"If symptom persist or worsen get a doctor's consultation.",
				     "buttons":[
					{
					"type":"postback",
					"title":"More Details",
					"payload":rest+"_about"
					},
					 {
					"type":"postback",
					"title":"Remedies",
					"payload":rest+"_remedies"
					}
				     ]
				}
			      ]
		bot.send_generic_message(sender_id, elements)

#if user tap a button from a quick reply
def received_qr(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	text = event["message"]["quick_reply"]["payload"]
	'''
	Mongo.update_user(student,std_id, ask, answer)
	Mongo.create_student(student,std_id, name, guardian, contact, address, email) 
	Mongo.create_schedule(schedule, std_id, subject, day, time, room, unit, instructor,sy,sem)
	Mongo.update_student(student,std_id, name, guardian, contact, address, email)
	Mongo.create_account(account, std_id, sy, sem, prelim, midterm, prefinal, final, amount_paid,balance, old_account)
	Mongo.create_exam(exam, std_id, subject, day, time, room, proctor,sy,sem)
	Mongo.create_scholarship(scholarship,name,description,status)      
	Mongo.create_program(programs,name,description,department,status)
	Mongo.create_enrollment(enrollment,schedules, requirements, fee, flow,category)
	Mongo.create_employee(employee,eid, name, department,designation)
	Mongo.get_data_users(users, sender_id)
	Mongo.get_data(table, std_id)
	Mongo.get_details(table)
	Mongo.get_enrollment(table, category)
	'''
	global schedules, frequirements, ffee, fflow,trequirements, tfee, tflow,orequirements, ofee, oflow, category#enrollment    
	global eid, ename, department,designation#employee
	global ask,answer,std_id #users
	global name, guardian, contact, address, email #student
	global subject, day, time, room, unit, instructor,sy,sem #schedule
	global sy, sem, prelim, midterm, prefinal, final, amount_paid,balance, old_account  #account
	global subject, day, time, room, unit, proctor,sy,sem    #exam
	global sname,description,status,sreq #scholarship
	global pame,description,department,status #programs SIS TESDA SENIOR HIGH
	
	#users
	user_data = Mongo.get_data_users(users, sender_id)
	if user_data !=None:
		ask = user_data['last_message_ask']
		answer = user_data['last_message_answer']
	else: 
		pass
	eF_data = Mongo.get_enrollment(enrollment,'freshmen')
	eT_data = Mongo.get_enrollment(enrollment,'transferee')
	eO_data = Mongo.get_enrollment(enrollment,'old')
	if eF_data !=None:
		schedules = eF_data['schedules']
		frequirements = eF_data['requirements']
		ffee = eF_data['fee']
		fflow = eF_data['flow']
	else: 
		pass
	if eT_data !=None:
		trequirements = eT_data['requirements']
		tfee = eT_data['fee']
		tflow = eT_data['flow']
	else: 
		pass
	if eO_data !=None:
		orequirements = eO_data['requirements']
		ofee = eO_data['fee']
		oflow = eO_data['flow']
	else: 
		pass
	#If student
	if text == 'enrollment':
		Mongo.set_column(users, sender_id,'last_message_answer', 'enrollment')
		bot.send_text_message(sender_id, schedules)
		bot.send_quick_replies_message(sender_id, 'Get Requirements',  [{"content_type":"text","title":"Send Requirements","payload":"requirements"}])
	if text == 'requirements':
		Mongo.set_column(users, sender_id,'last_message_answer', 'requirements')
		quick_replies = {"content_type":"text","title":"Freshmen","payload":"freshmen"},{"content_type":"text","title":"Transferee","payload":"transferee"},{"content_type":"text","title":"Old Student","payload":"old"}
		bot.send_quick_replies_message(sender_id, 'Requirements for ?', quick_replies)
	if text == 'freshmen':
		Mongo.set_column(users, sender_id,'last_message_answer', 'freshmen')
		bot.send_text_message(sender_id,frequirements)
		bot.send_quick_replies_message(sender_id, 'Enrollment Fee?',  [{"content_type":"text","title":"Send Enrollment Fee","payload":"fee"}])
	if text == 'transferee':
		Mongo.set_column(users, sender_id,'last_message_answer', 'freshmen')
		bot.send_text_message(sender_id,trequirements)
		bot.send_quick_replies_message(sender_id, 'Enrollment Fee?',  [{"content_type":"text","title":"Send Enrollment Fee","payload":"fee"}])
	if text == 'old':
		Mongo.set_column(users, sender_id,'last_message_answer', 'freshmen')
		bot.send_text_message(sender_id,orequirements)
		bot.send_quick_replies_message(sender_id, 'Enrollment Fee?',  [{"content_type":"text","title":"Send Enrollment Fee","payload":"fee"}])
	if text == 'fee':
		bot.send_text_message(sender_id,ffee)
		bot.send_quick_replies_message(sender_id, 'Enrollment Flow?',  [{"content_type":"text","title":"Send Enrollment Flow","payload":"flow"}])
	if text == 'flow':
		bot.send_text_message(sender_id,flow)
		bot.send_text_message(sender_id,"For other matters simply click the 'start over' button in the persistent menu.")
		
	if text == 'schedule':
		Mongo.set_column(users, sender_id,'last_message_answer', 'schedule')
		quick_replies = {"content_type":"text","title":"Current","payload":"current"},{"content_type":"text","title":"Previous","payload":"previous"}
		bot.send_quick_replies_message(sender_id, 'What schedule?', quick_replies)
	
	if text == 'previous':
		bot.send_text_message(sender_id,'Under Development')
	if text == 'current':
		if d.month in range(1,7):
			prev = d.year - 1
			sy = "{}-{}".format(prev,d.year)
			sem = '2nd'
		else:
			nex = d.year + 1
			sy = "{}-{}".format(d.year,nex)
			sem = '2nd'
		sched = Mongo.get_schedule(schedule, sy, sem,std_id)
		if sched !=None:
			for data in sched:
				a = data["subject"]+" "+data["time"]+" "+data["day"] +" "+data["room"]+" "+data["instructor"]
				bot.send_text_message(sender_id,"* {}".format(a))
		else: 
			pass
		
	if text == 'account_slip':
		Mongo.set_column(users, sender_id,'last_message_answer', 'account_slip')
		quick_replies = {"content_type":"text","title":"Current","payload":"current_a"},{"content_type":"text","title":"Previous","payload":"previous_a"}
		bot.send_quick_replies_message(sender_id, 'What account slip?', quick_replies)
	if text == 'previous_a':
		bot.send_text_message(sender_id,'Under Development')
	if text == 'current_a':
		if d.month in range(1,7):
			prev = d.year - 1
			sy = "{}-{}".format(prev,d.year)
			sem = '2nd'
		else:
			nex = d.year + 1
			sy = "{}-{}".format(d.year,nex)
			sem = '2nd'
		slip = Mongo.get_slip(account_slip, sy, sem,std_id)
		if slip !=None:
			bot.send_text_message(sender_id,"ACCOUNT SLIP")
			for data in slip:
				bot.send_text_message(sender_id,"Prelim :{}\nMidterm :{}\nPrefinal :{}\nFinal :{}\nTotal :{}\nAmount Paid :{}\nBalance :{}\nOld Account :{}".format(data["prelim"], data["midterm"], data["prefinal"], data["final"], data["total"], data["amount_paid"], data["balance"], data["old_account"]))
		else: 
			pass
		
	if text == 'exam_schedule':
		if d.month in range(1,7):
			prev = d.year - 1
			sy = "{}-{}".format(prev,d.year)
			sem = '2nd'
		else:
			nex = d.year + 1
			sy = "{}-{}".format(d.year,nex)
			sem = '2nd'
		sched = Mongo.get_schedule(schedule, sy, sem,std_id)
		if sched !=None:
			for data in sched:
				a = data["subject"]+" "+data["time"]+" "+data["day"] +" "+data["room"]+" "+data["instructor"]
				bot.send_text_message(sender_id,"* {}".format(a))
		else: 
			pass
	if text == 'scholarship':
		pass
	if text == 'others':
		pass
	
	if text == 'yes_student':
		Mongo.set_column(users, sender_id,'last_message_answer', 'yes_student')
		bot.send_text_message(sender_id, "Please enter your student ID number.\nFor Example: 15000011000")
	if text == 'not_student':
		Mongo.set_column(users, sender_id,'last_message_answer', 'not_student')
		quick_replies = {"content_type":"text","title":"Enrollment","payload":"enrollment"},{"content_type":"text","title":"College Courses","payload":"college"},{"content_type":"text","title":"Senior High","payload":"sis"},{"content_type":"text","title":"Tesda Programs","payload":"tesda"},{"content_type":"text","title":"Scholarship","payload":"scholarship"},{"content_type":"text","title":"Others","payload":"others"}
		bot.send_quick_replies_message(sender_id, 'What do you want to know ?', quick_replies)
	

	  
#if user tap a button from a regular button
def received_postback(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	payload = event["postback"]["payload"]
	'''
	Mongo.update_user(student,std_id, ask, answer)
	Mongo.create_student(student,std_id, name, guardian, contact, address, email) 
	Mongo.create_schedule(schedule, std_id, subject, day, time, room, unit, instructor,sy,sem)
	Mongo.update_student(student,std_id, name, guardian, contact, address, email)
	Mongo.create_account(account, std_id, sy, sem, prelim, midterm, prefinal, final, amount_paid,balance, old_account)
	Mongo.create_exam(exam, std_id, subject, day, time, room, proctor,sy,sem)
	Mongo.create_scholarship(scholarship,name,description,status)      
	Mongo.create_program(programs,name,description,department,status)
	Mongo.create_enrollment(enrollment,schedules, requirements, fee, flow,category)
	Mongo.create_employee(employee,eid, name, department,designation)
	Mongo.get_data_users(users, sender_id)
	Mongo.get_data(table, std_id)
	Mongo.get_details(table)
	'''
	global schedules, frequirements, ffee, fflow,trequirements, tfee, tflow,orequirements, ofee, oflow,category#enrollment    
	global eid, ename, department,designation#employee
	global ask,answer,std_id #users
	global name, guardian, contact, address, email #student
	global subject, day, time, room, unit, instructor,sy,sem #schedule
	global sy, sem, prelim, midterm, prefinal, final, amount_paid,balance, old_account  #account
	global subject, day, time, room, unit, proctor,sy,sem    #exam
	global sname,description,status,sreq#scholarship
	global pame,description,department,status #programs SIS TESDA SENIOR HIGH
	#users
	user_data = Mongo.get_data_users(users, sender_id)
	#student_data = Mongo.get_data(student, std_id) for verification
	if user_data !=None:
		ask = user_data['last_message_ask']
		answer = user_data['last_message_answer']
	else: 
		pass
	#Get started button tapped{
	if payload=='start':
		greet = random.choice(GREETING_RESPONSES)
		if not Mongo.user_exists(users,sender_id): #if user_exists == false add user information
			bot.send_text_message(sender_id, "{} {}!,Welcome to ACLC Butuan's Information Chatbot".format(greet,first_name(sender_id))))
			bot.send_text_message(sender_id, "You can do inquiries, know your exam's schedule, get account slip and many other stuff.")
			Mongo.set_column(users, sender_id,'last_message_ask', 'student?')
			quick_replies = {"content_type":"text","title":"Yeah","payload":"yes_student"},{"content_type":"text","title":"Not yet","payload":"not_student"}
			bot.send_quick_replies_message(sender_id, 'Already a student?', quick_replies)
		else:
			if Mongo.student_enroll(student, sender_id):
				bot.send_text_message(sender_id, "{} {},Welcome back!".format(greet,first_name(sender_id))))
				quick_replies = {"content_type":"text","title":"Enrollment","payload":"enrollment"},{"content_type":"text","title":"Schedule","payload":"schedule"},{"content_type":"text","title":"Account Slip","payload":"account_slip"},{"content_type":"text","title":"Exam Schedule","payload":"exam_schedule"},{"content_type":"text","title":"Scholarship","payload":"scholarship"},{"content_type":"text","title":"Others","payload":"others"}
				bot.send_quick_replies_message(sender_id, 'What can I do for you?', quick_replies)
			else:
				bot.send_text_message(sender_id, "{} again {}!".format(greet,first_name(sender_id))))
				quick_replies = {"content_type":"text","title":"Enrollment","payload":"enrollment"},{"content_type":"text","title":"College Courses","payload":"college"},{"content_type":"text","title":"Senior High","payload":"sis"},{"content_type":"text","title":"Tesda Programs","payload":"tesda"},{"content_type":"text","title":"Scholarship","payload":"scholarship"},{"content_type":"text","title":"Others","payload":"others"}
				bot.send_quick_replies_message(sender_id, 'What do you want to know?', quick_replies)
			
	#Persistent Menu Buttons        
	if payload=='start_over':
		if terms == "Yes":
			Mongo.set_ask(users,sender_id, "")
			Mongo.set_answer(users,sender_id, "")
			quick_replies = {"content_type":"text","title":"Myself","payload":"myself"},{"content_type":"text","title":"My Child","payload":"mychild"},{"content_type":"text","title":"Someone else","payload":"someone"}
			bot.send_quick_replies_message(sender_id, 'Who do you want to 🔍check symptom, {}?'.format(first_name(sender_id)), quick_replies)
		elif terms == "No":
			greet_disclaimer(sender_id)
		
	if payload=='pm_dengue_prevention':
		bot.send_text_message(sender_id,'Dengue Prevention Under Construction')
	if payload=='pm_about':
		bot.send_text_message(sender_id,'About Under Construction')
	
	

def choose_howto(sender_id,payload1,payload2,payload3,name):
	choices = [
						{
						"type": "postback",
						"title": "💁‍♂️Natural Remedies",
						"payload": payload1
						},{
						"type": "postback",
						"title": "💊Medication",
						"payload": payload2
						},{
						"type": "postback",
						"title": "📃About",
						"payload": payload3
						}
						]
	bot.send_text_message(sender_id,"What do you want to know about {}.".format(name))
	bot.send_button_message(sender_id, "Choose:", choices)
	
def first_name(sender_id):
	user_info = bot.get_user_info(sender_id)
	if user_info is not None: 
		first_name = user_info['first_name']
		#lname = user_info['last_name']
		return first_name
	return ''

def init_bot():
	#Greetings 
	greetings =  {"greeting":[
		  {
			  "locale":"default",
			  "text":"Hi {{user_full_name}}!, You can ask for inquiries and more from ACLC INFO BOT"
			}
		]}
	bot.set_greetings(greetings)
	#Get started button
	gs ={ 
			  "get_started":{
				"payload":'start'
			  }
		}
	bot.set_get_started(gs)
	#Persistent Menu
	false=False
	pm_menu = {
				"persistent_menu": [
					{
						"locale": "default",
						"composer_input_disabled": false,
						"call_to_actions": [
							{
								"type": "postback",
								"title": "Start Over",
								"payload": "start_over"
							},
							{
								"type": "postback",
								"title": "Call ACLC",
								"payload": "pm_call"
							},
							{
								"type": "postback",
								"title": "Admin Login",
								"payload": "pm_admin"
							}
						]
					}
				]
			}
	bot.set_persistent_menu(pm_menu)
	
def greet_disclaimer(sender_id):
	Mongo.set_ask(users,sender_id, "agree and proceed?")
	bot.send_text_message(sender_id,"Before we proceed onward, it's time for a brief interruption from my good friends, the lawyers. ⚖️")
	bot.send_text_message(sender_id,"Remember that DrPedia is just a robot 🤖, not a doctor 👨‍⚕️.")
	bot.send_text_message(sender_id,"DrPedia is intended for informational purposes only and DrPedia don't attempt to represent a real pediatrician or a doctor in any way.")
	quick_replies = {"content_type":"text","title":"🤝Agree and proceed", "payload":"yes_agree"},{"content_type":"text","title":"📇See details","payload":"see_details"}
	bot.send_quick_replies_message(sender_id, "By tapping 'Agree and proceed' you accept DrPedia's Terms of Use and Privacy Policy", quick_replies)
				
def verify_fb_token(token_sent):
	#take token sent by facebook and verify it matches the verify token you sent
	#if they match, allow the request, else return an error 
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Invalid verification token'
#Greetings, persisten menu, get started button
init_bot()
if __name__ == "__main__":
	app.run()
