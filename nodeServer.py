import os, requests, json, sys, pathlib, nodesConfig
from flask import Flask, render_template, jsonify, url_for, request, session, flash, redirect, send_from_directory
from flask.ext.pymongo import PyMongo
from werkzeug.utils import secure_filename

#Node ID is passed in as the first argument, set node ID to 1 if no node specified
def getNodeID():
    if(len(sys.argv) > 0):
        return int(sys.argv[1])
    return 1

nodeID = getNodeID()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'
app.config['UPLOAD_FOLDER'] = '/home/donal-tuohy/Documents/SS_year/DFS/NODE_' + str(nodeID) 

#Returns boolean of whether the file is there or not
def checkForFile(filename):
    return os.path.isfile("./NODE_" + str(nodeID) +"/" + filename) 

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
            return filename + " uploaded to node " + str(getNodeID())
    


if __name__ == "__main__":

    from flask import jsonify

    ##First node will run on port 5001 and increment with each node
    nodeID = getNodeID()
    portNum = 5000 + nodeID
    address = ("http://127.0.0.1:" + str(portNum) + "/")

    pathlib.Path('./NODE_' + str(nodeID)).mkdir(parents=True, exist_ok=True)

    mainServerUrl = "http://127.0.0.1:5000/"
    joinJSON = {'message': 'I am a new node.', 'nodeID': nodeID, 'address': address }
    sendFlag = requests.post(mainServerUrl + "newnode", json=joinJSON) 

    app.run(debug=True, port=portNum)






