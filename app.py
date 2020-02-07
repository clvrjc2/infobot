#FOR ITMAJOR 4 QUADRUPE SURVELANCE BOT WITH FACIAL DETECTION AND MESSENGER NOTIFICATION

#Libraries to be import START
import random
from flask import Flask, request
from messnger_syntax.bot import Bot
import os
import json
import pymongo
from pymongo import MongoClient
import Mongo#import Mongo.py
#from nlu import nlp #NO NEED
#from collections import Counter #install collections
import datetime as dt
#Libraries to be import END

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

MONGO_TOKEN = os.environ['MONGO_DB']
cluster = MongoClient(MONGO_TOKEN)
db = cluster["Quadruped"]
survey = db["surveillance"]

image_url = 'https://raw.githubusercontent.com/clvrjc2/infobot/master/images/'
GREETING_RESPONSES = ["Hi", "Hey", "Hello there", "Hello", "Hi there"]

def notify():
	#Get the image from MongoDB save from local rpi which is the quadruped
	#bot.send_image ....
	#qr buttons to categorize as intruder or not
	#while true
	

def verify_fb_token(token_sent):
	#take token sent by facebook and verify it matches the verify token you sent
	#if they match, allow the request, else return an error 
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Invalid verification token

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
					if message['message'].get('text'):
						if message['message'].get('quick_reply'):
							received_qr(message)  
						else: #else if message is just a text
							received_text(message)
					#if user sends us a GIF, photo,video, or any other non-text item
					elif message['message'].get('attachments'):
						#TO BE EDIT
						#This will be the image file handling
						pass
				elif message.get("postback"):  # user clicked/tapped "postback" button in earlier message
					received_postback(message)
					
	return "Message Processed"

#if user send a message in text
def received_text(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	text = event["message"]["text"]
	#FOR MANIPULATION OF REGISTRATION USER INPUT
	
#if user tap a button from a quick reply
def received_qr(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	text = event["message"]["quick_reply"]["payload"]
	#ALL CONTROL WALK LEFT WALK RIGHT TURN ON TURN OF
	
#if user tap a button from a regular button
def received_postback(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	payload = event["postback"]["payload"]
	
	#Get started button tapped{
	if payload=='start':
		greet = random.choice(GREETING_RESPONSES)
		bot.send_text_message(sender_id, "{} {}!, I'm your Quadruped Sruvey Notifier".format(greet,first_name(sender_id)))
		quick_replies = [{"content_type":"text","title":"Yeah","payload":"sounds_good"}]
		bot.send_quick_replies_message(sender_id, "I will notify you if theres intruder in your house.\nYou can also control me 'Quadruped' through messenger.", quick_replies)
		
	#Persistent Menu Buttons        
	if payload=='pm_register':
		#Register this facebook to notify for intrustion detected.
		#with password
		bot.send_text_message(sender_id,'Under Development')
	if payload=='pm_surver':
		#turn the quadruped into survey mode or turn it on to walk rotaionaly
		#manipulated through mongodb value
		bot.send_text_message(sender_id,'Under Development')
	if payload=='pm_stay':
		#turn the quadruped into survey mode or turn it on to walk rotaionaly
		#manipulated through mongodb value

		bot.send_text_message(sender_id,'Under Development')
	
	
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
			  "text":"Hi {{user_full_name}}!, I'm your Quadruped Surveillance Notifier!"
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
								"title": "Register",
								"payload": "pm_register"
							},
							{
								"type": "postback",
								"title": "Survey",
								"payload": "pm_survey"
							},
							{
								"type": "postback",
								"title": "Stay",
								"payload": "pm_stay"
							}
						]
					}
				]
			}
	bot.set_persistent_menu(pm_menu)

#Greetings, persisten menu, get started button
init_bot()
if __name__ == "__main__":
	app.run()
