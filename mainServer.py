import os, requests, nodesConfig
from flask import Flask, render_template, url_for, request, session, flash, redirect, send_from_directory, jsonify
from flask.ext.pymongo import PyMongo
from werkzeug.utils import secure_filename

#dict - key = filename, contains list of all node addresses that have the file
#listOffiles['index.jpeg'] = ["http://127.0.0.1:5002/", "http://127.0.0.1:5002/"]
listOfFiles = {}
fileAccessCount = {}

#dict - key = nodeID, contains list of all node addresses
#listOffiles[1] = "http://127.0.0.1:5001/"
connectedNodes = {}

UPLOAD_FOLDER ='/home/donal-tuohy/Documents/SS_year/DFS/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def parseNodeID(address):
    split = address.split(':')
    port = int((split[2])[:4])
    return port - 5000


def addFilesFromNode(dictOfFiles, nodeAddress):
    for fileName in dictOfFiles:
        if fileName in listOfFiles.keys():
            if nodeAddress not in listOfFiles[fileName]:
                (listOfFiles[fileName]).append(nodeAddress)
                (fileAccessCount[fileName])[1] += 1     #Add to the total number of nodes that have the file 
                
        else:
            listOfFiles[fileName] = [nodeAddress]
            fileAccessCount[fileName] = [0,1]       #First index is amount of times it has been accesed, second is number of nodes that have it

def roundRobin(filename):
    myList = fileAccessCount[filename]
    indexOfNodeToUse = (myList[0])%(myList[1])
    (fileAccessCount[filename])[0] += 1
    return indexOfNodeToUse 
    
#If client wants to get a file, it sends a get request to this URL
#This server checks if it is stored in the node and if so, returns the address of the node to the client
@app.route('/download/<filename>')
def download_file(filename):

    if filename in listOfFiles.keys():
        nodeAddress = ((listOfFiles[filename])[roundRobin(filename)])
        return jsonify({'message': 'File exists.', 'address': ( nodeAddress + filename), 'nodeID': parseNodeID(nodeAddress)})
    else:
        return jsonify({'message': 'File does not exist.'})
    
    # #Step through each active node
    # for node in connectedNodes:
        
    #     #Send get request to current node to check if it has the file
    #     response = requests.get(connectedNodes[node] + "servercheck/" + filename)
    #     #Make sure response was okay
    #     if response.ok:
    #         #Take the json part out of the response
    #         response2 = response.json()
    #         message = response2['message']

    #         #Parse message and if file is found, return address of node the file is stored on. Function will also stop searching
    #         if message == "File on node.":
    #             print("File found on: ", connectedNodes[node])
    #             return jsonify({'message': 'File exists.', 'address': (connectedNodes[node] + filename), 'nodeID': node})
    #         #
    #         elif message == "File does not exist.":
    #             print("File not on: ", connectedNodes[node])
    #             pass
    #         else:
    #             return "ERROR MATE"
    #     del response
    # return "RESPONSE NOT OKAY"



@app.route('/newnode', methods=['POST'])
def newNode():
    response = request.get_json()
    newNodeID = response['nodeID']
    newNodeAddr = response['address']
    dictOfFiles = response['currentFiles']
    addFilesFromNode(dictOfFiles, newNodeAddr)
    print("Global list of files: ",listOfFiles)
    connectedNodes[newNodeID] = newNodeAddr

    #fileDB  = mongo.db.fileList

    
    print("Node " + str(newNodeID) +" connected on " + newNodeAddr + ".")
    print(connectedNodes)
    return "Hello" #request.get_json()



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == "__main__":
    app.run(debug=True)