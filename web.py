import os
from flask.ext.googlemaps import GoogleMaps
from alerts import *
import time
from flask import Flask,flash,redirect,render_template,request,send_from_directory, url_for
import logging
from database import *
from werkzeug import secure_filename

logging.basicConfig(filename='web.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
app = Flask(__name__)
db = Database('mydb')
GoogleMaps(app)

app.secret_key = 'xervtr'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/var/www/web/uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    try:
        return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    except Exception as e:
        logging.error('allowed_file(), {}:{}'.format(type(e).__name__, e))

@app.route('/')
def index():
    try:
        people = db.getPeople()
        return render_template('index.html', people = people)
    except Exception as e:
        logging.error('index(), {}:{}'.format(type(e).__name__, e))

@app.route('/add_person/')
def addPerson():
    try:
        return render_template('add_person.html') 
    except Exception as e:
        logging.error('addPerson(), {}:{}'.format(type(e).__name__, e))

@app.route('/add_volunteer/')
def addVolunteer():
    try:
        return render_template('add_volunteer.html')
    except Exception as e:
        logging.error('addVolunteer(), {}:{}'.format(type(e).__name__, e))

@app.route('/process_volunteer',methods=['POST'])
def processVolunteer():
    try:
        properties = ['firstName', 'lastName', 'tel', 'lng','lat']
        
        vol = {}
        
        for p in properties:
            if not request.form[p]:
                flash('Property {} is missing!'.format(p))
                return redirect(url_for('addVolunteer'))
            if request.form[p] == '' or request.form[p] == 0:
                flash('Property {} cannot be empty'.format(p))
                return redirect(url_for('addVolunteer'))
            vol[p] = request.form[p]
       
        db.addVolunteer(vol)
        checkPeopleForVol(vol,db)

        flash('Volunteer {} was added.'.format(vol['firstName']))
        return redirect(url_for('index'))
    except Exception as e:
        logging.error('processVolunteer(), {}:{}, {}'.format(type(e).__name__, e, str(e.args)))

@app.route('/process_person/',methods =['POST'])
def processPerson():
    try:
        personProperties = ['firstName', 'lastName', 'email', 'lat','lng','missSince','age','gender', 'race', 'hairColor','eyeColor','weight','heightF', 'heightI']
        
        # Get the name of the uploaded file
        # the filename on the server will be the same as original one
        # need to change that if enter production stage to avoid
        # problems with user files that have the same name
        file = request.files['image']
        
        if not file:
            flash('Please upload an image. Image is the most important piece of information')
            return redirect(url_for('addPerson'))
        
        person = {}

        for p in personProperties:
            if not request.form[p]:
                flash('Property {} is missing!'.format(p))
                return redirect(url_for('addPerson'))
            if request.form[p] == '' or (request.form[p] == 0 and p != 'heightI'):
                flash('Property {} cannot be empty'.format(p))
                return redirect(url_for('addPerson'))
            person[p] = request.form[p]

        # Check if the file is one of the allowed types/extensions
        if allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            person['imageURL'] = url_for('uploadedFile',filename=filename)
        else:
            flash('Please upload a valid image file. Valid formats include {}'.format(str(app.config['ALLOWED_EXTENSIONS'])))
            return redirect(url_for('addPerson'))
       
        person['reported'] = time.time()
        person['_id'] = db.addPerson(person)
        checkVolForPerson(person,db)
        flash('Added {} to the list of missing people'.format(person['firstName']))
        return redirect(url_for('index'))

    except Exception as e:
        logging.error('processPerson(), {}:{}, {}'.format(type(e).__name__, e, str(e.args)))

@app.route('/people/<id>/')
def people(id):
    try:
        person = db.getPerson(id)
        if person:
            return render_template('person.html', person = person)
        else:
            return 'User with id = {} does not exist'.format(id)
    except Exception as e:
        logging.error('people(), {}:{}, {}'.format(type(e).__name__,e,str(e.args)))

@app.route('/add_location/<id>/')
def addLocation(id):
    try:
        person = db.getPerson(id)
        if person:
            firstName = person['firstName']
            lastName = person['lastName']
            return render_template('add_location.html', lastName = lastName, firstName = firstName,id=id)
        else:
            return 'User with id = {} does not exist'.format(id)
    except Exception as e:
        logging.error('addLocation(), {}:{}, {}'.format(type(e).__name__,e,str(e.args)))

@app.route('/process_location/<id>/', methods=['POST'])
def processLocation(id):
    try:
        person = db.getPerson(id)
        if person:
            if request.form['lng'] and request.form['lat']:
                person['lng1'] = request.form['lng']
                person['lat1'] = request.form['lat']
                db.updatePerson(person)
            else:
                flash("You haven't picked the location")
                return redirect(url_for('addLocation', id = id))
            flash('Updated coordiates')
            return redirect(url_for('people', id = id))
        else:
            return 'User with id = {} does not exist'.format(id)
    except Exception as e:
        logging.error('addLocation(), {}:{}, {}'.format(type(e).__name__,e,str(e.args)))


@app.route('/uploads/<filename>/')
def uploadedFile(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logging.error('uploadedFile(), {}:{}'.format(type(e).__name__, e))
    
if __name__ == '__main__':
    app.run()
