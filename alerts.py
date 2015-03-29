from database import *
from twilio.rest import TwilioRestClient 
import logging

logging.basicConfig(filename='web.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

ACCOUNT_SID = "AC227abb8b70bfd0237a9917f5740db5bd" 
AUTH_TOKEN = "8721bb6a4f070bb5a6ac6b4759e0d056" 
sender = "+18147534070"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

def sendMessage(to,text):
    try:
        client.messages.create(
                    to=to, 
                    from_=sender, 
                    body=text,  
        )
    except Exception as e:
        logging.error('sendMessage(), {}:{}, {}'.format(type(e).__name__, e, str(e.args)))

def checkPeopleForVolunteer(vol,db):
    None

def checkVolForPerson(person,db):
    None

