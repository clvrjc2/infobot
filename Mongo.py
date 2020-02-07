from datetime import datetime
import os
from messnger_syntax.bot import Bot
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
bot = Bot (ACCESS_TOKEN)

timestamp = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
def survey(survey, image, intruder, notified,new):
    survey_insert = { 
                    'key':'Q3RN',
                    'created_at': timestamp,
                    'image':image,
                     'intruder': intruder,
                     'notified':notified,
                     'new':new
                   }
    users.insert(user_insert)

def update_survey(survey,image,intruder,notified,new)
    survey.update({"key": "Q3RN"},{"$set":{'new':new ,'created_at': timestamp, 'image':image, 'intruder':intruder, 'notified': notified}})                      
    

#register user to be notified
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
                    'action': ''
                    'ask':''
                   }
    users.insert(user_insert)
    
def update_user(survey, sender_id, action,ask)
    survey.update({"user_id": sender_id},{"$set":{'action':action ,'ask': ask}})                      
 
