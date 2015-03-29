from database import *
from geopy.distance import vincenty
from twilio.rest import TwilioRestClient 
import logging
import time 
logging.basicConfig(filename='web.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

ACCOUNT_SID = "AC227abb8b70bfd0237a9917f5740db5bd" 
AUTH_TOKEN = "8721bb6a4f070bb5a6ac6b4759e0d056" 
sender = "+18147534070"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
distance = 20
url = 'http://hackpsu.cloudapp.net/people/'

def sendMessage(to,text):
    try:
        client.messages.create(
                    to=to, 
                    from_=sender, 
                    body=text,  
        )
    except Exception as e:
        logging.error('sendMessage(), {}:{}, {}'.format(type(e).__name__, e, str(e.args)))

def checkPeopleForVol(vol,db):
    people = db.getPeople()

    for person in people:
        if time.time() - float(person['reported']) <= 48*60*60:
            if vincenty([float(person['lat']),float(person['lng'])],[float(vol['lat']),float(vol['lng'])]).miles < distance or ('lat1' in person and 'lng1' in person and vincenty([float(person['lat1']),float(person['lng1'])],[float(vol['lat']),float(vol['lng'])]).miles < distance):
                text = 'Dear {}, {} went missing less than 48 hours ago in your area! Go to {}{} for details'.format(vol['firstName'],person['firstName'],url,person['_id'])
                sendMessage(vol['tel'],text)


def checkVolForPerson(person,db):
    vols = db.getVolunteers()

    for vol in vols:
        if time.time() - float(person['reported']) <= 48*60*60:
            if vincenty([float(person['lat']),float(person['lng'])],[float(vol['lat']),float(vol['lng'])]).miles < distance:
                text = 'Dear {}, {} went missing less than 48 hours ago in your area! Go to {}{} for details'.format(vol['firstName'],person['firstName'],url,person['_id'])
                sendMessage(vol['tel'],text)

def checkVolForPersonAfter(person,db):
    vols = db.getVolunteers()

    for vol in vols:
        if time.time() - float(person['reported']) <= 48*60*60:
            if vincenty([float(person['lat1']),float(person['lng1'])],[float(vol['lat']),float(vol['lng'])]).miles < distance:
                text = 'Dear {}, {} went missing less than 48 hours ago in your area! Go to {}{} for details'.format(vol['firstName'],person['firstName'],url,person['_id'])
                sendMessage(vol['tel'],text)

