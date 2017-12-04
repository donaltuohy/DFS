import os, requests, json, sys, pathlib, serverConfig
from flask import Flask, render_template, jsonify, url_for, request, session, flash, redirect, send_from_directory
from flask.ext.pymongo import PyMongo
from werkzeug.utils import secure_filename
from serverConfig import *
from time import sleep


#returns the Id of this current node
def getNodeID():
    if(len(sys.argv) > 0):
        return int(sys.argv[1])
    return 1

##CONFIGURATIONS##

nodeID = getNodeID()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'
app.config['UPLOAD_FOLDER'] = '/home/donal-tuohy/Documents/SS_year/DFS/NODE_' + str(nodeID)


#######################
### LOCAL FUNCTIONS ###
#######################

#returns the address of this node
def getAddress():
    nodeID = getNodeID()
    portNum = 5000 + nodeID
    return ("http://127.0.0.1:" + str(portNum) + "/")

#returns a dict of all the files on the node
def getDictOfFiles(nodeAddress):
    filesOnNode = {}
    fileList = os.listdir(app.config['UPLOAD_FOLDER'])
    for fileName in fileList:
         filesOnNode[fileName] = nodeAddress
    return filesOnNode

#Returns boolean of whether the file is there or not
def checkForFile(filename):
    return os.path.isfile("./NODE_" + str(nodeID) +"/" + filename) 


#################
### ENDPOINTS ###
#################

#Server checks if the file exists
@app.route('/servercheck/<filename>', methods=['GET'])
def serverCheck(filename):
    fileExists = checkForFile(filename)
    #Server looking for file
    print('Checking for file')
    if fileExists:
        return jsonify({'message': 'File on node.'}) 
    return jsonify({'message': 'File does not exist.'})

#Server uses this endpoint to tell the node to delete a file from the server
@app.route('/removefile', methods=['POST'])
def removeFile():
    message = request.get_json()
    filename = message['fileToDelete']
    os.remove(app.config['UPLOAD_FOLDER'] + '/' + filename)
    print("<" + filename + "> has been deleted from this node.")
    return jsonify({'message' : 'File deleted.'})

#Returns the file at this enpoint
@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#Recieves a file from the client to be uploaded to this node
#Once uploaded, sends a notification to the server that a file has been uploaded.
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            currentFiles[filename] = ""
            dataToNotify = {'nodeAddress': getAddress(), 'fileName': {filename: [getAddress()]}, 'fileType': "upload" }
            notifyServer = requests.post("http://127.0.0.1:5000/newfile", json=dataToNotify)
            print("<" + filename + "> has been uploaded to this node.")
            return filename + " uploaded to node " + str(getNodeID())
    
@app.route('/backup/<filename>', methods=['GET','POST'])
def backup(filename):
    filecheck = requests.get("http://127.0.0.1:5000/download/" + filename)
    if (filecheck.ok):
        serverJsonResponse = filecheck.json()
        print(serverJsonResponse)
        if (serverJsonResponse['message'] == "File exists."):
            print("Address to get file from = ", serverJsonResponse['address'])
            fileRequest = requests.get(serverJsonResponse['address'])
            print("Request sent to:", serverJsonResponse['address'])
            with open('/home/donal-tuohy/Documents/SS_year/DFS/NODE_' + str(nodeID) + "/" + filename, 'wb') as handler:
                handler.write(fileRequest.content)
            del fileRequest
            dataToNotify = {'nodeAddress': getAddress(), 'fileName': {filename: [getAddress()]} ,'fileType': "backup"}
            updateServer = requests.post("http://127.0.0.1:5000/newfile", json=dataToNotify)
            if updateServer.ok:
                print(filename + " backed up on this node.")
            else:
                print("Could not get file to backup")
    else:
        print("File backup unsuccessful")

    return "Hello"

if __name__ == "__main__":

    from flask import jsonify

    ##First node will run on port 5001 and increment with each node
    nodeID = getNodeID()
    portNum = 5000 + nodeID
    address = ("http://127.0.0.1:" + str(portNum) + "/")

    #Create folder if not already created for this node
    pathlib.Path('./NODE_' + str(nodeID)).mkdir(parents=True, exist_ok=True)
    
    currentFiles = getDictOfFiles(address)
    mainServerUrl = "http://127.0.0.1:5000/"
    
    joinJSON = {'message': 'I am a new node.', 'nodeID': nodeID, 'address': address, 'currentFiles': currentFiles}
    sendFlag = requests.post(mainServerUrl + "newnode", json=joinJSON) 

    app.run(debug=True,port=portNum)






