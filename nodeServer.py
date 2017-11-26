import os, nodesConfig, requests, json
from flask import Flask, render_template, jsonify, url_for, request, session, flash, redirect, send_from_directory
from flask.ext.pymongo import PyMongo
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'
app.config['UPLOAD_FOLDER'] = '/home/donal-tuohy/Documents/SS_year/DFS/NODE_A'
#app.config['SERVER_NAME'] = '5001'

#Returns boolean of whether the file is there or not
def checkForFile(filename):
    return os.path.isfile("./NODE_A/" + filename) 

#Server checks if the file exists
@app.route('/servercheck/<filename>', methods=['GET'])
def serverCheck(filename):
    fileExists = checkForFile(filename)
    #Server looking for file
    print('Checking for file')
    if fileExists:
        return jsonify({'message': 'File on node.'}) 
    return jsonify({'message': 'File does not exist.'})


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        print("In post request part")
        #Check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return "No file part" #redirect(request.url)
        file = request.files['file']
        #if user does not select file
        if file.filename =='':
            print('No selected file')
            return "NO selected file" #redirect(request.url)""
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "file uploaded"
    


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    print(app.config['SERVER_NAME'])






