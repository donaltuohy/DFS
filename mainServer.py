import os
from flask import Flask, render_template, url_for, request, session, flash, redirect, send_from_directory
from flask.ext.pymongo import PyMongo
from werkzeug.utils import secure_filename

UPLOAD_FOLDER ='/home/donal-tuohy/Documents/SS_year/DFS/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'
app.config['MONGO_DBNAME'] = 'dfs'
app.config['MONGO_URI'] = 'mongodb://donal:testing@ds117156.mlab.com:17156/dfs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("In post request part")
        #Check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        #if user does not select file
        if file.filename =='':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

mongo = PyMongo(app)

@app.route('/add')
def add():
    files = mongo.db.files
    files.insert({'name': 'testingFilename'})
    return "Added name!"


if __name__ == "__main__":
    app.run(debug=True)