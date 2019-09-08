import os
from flask import Flask, request
from fbmq import Page

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

page = Page(ACCESS_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
  page.handle_webhook(request.get_data(as_text=True))
  return "ok"

@page.handle_message
def message_handler(event):
  """:type event: fbmq.Event"""
  sender_id = event.sender_id
  message = event.message_text
  
  page.send(sender_id, "thank you! your message is '%s'" % message)

@page.after_send
def after_send(payload, response):
  """:type payload: fbmq.Payload"""
  print("complete")
  
if __name__ == "__main__":
    app.run()
