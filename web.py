import os
from flask import Flask,redirect,render_template,request,send_from_directory, url_for
import logging
from database import *
from werkzeug import secure_filename

logging.basicConfig(filename='web.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
app = Flask(__name__)
db = Database('mydb')

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

@app.route('/test/')
def test():
    try:
        return render_template('test.html')
    except Exception as e:
        logging.error('test(), {}:{}'.format(type(e).__name__, e))

@app.route('/upload/', methods =['POST'])
def upload():
    try:
        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            return redirect(url_for('uploadedFile',filename=filename))
    except Exception as e:
        logging.error('upload(), {}:{}'.format(type(e).__name__, e))

@app.route('/uploads/<filename>/')
def uploadedFile(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logging.error('uploadedFile(), {}:{}'.format(type(e).__name__, e))
    
if __name__ == '__main__':
    app.run()
