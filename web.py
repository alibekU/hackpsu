from flask import Flask
import logging
from database import *
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request

logging.basicConfig(filename='web.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
app = Flask(__name__)
db = Database('mydb')

@app.route('/')
def index():
    people = db.getPeople()
    return render_template('index.html', people = people)

if __name__ == '__main__':
    app.run()

@app.route('/add_child/')
def addChild():
    return render_template('add_child.html')

@app.route('/add_volunteer/')
def addVolunteer():
    return render_template('add_volunteer.html')
