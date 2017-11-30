import os, requests, nodesConfig
from flask import Flask, render_template, url_for, request, session, flash, redirect, send_from_directory, jsonify
from flask.ext.pymongo import PyMongo
from werkzeug.utils import secure_filename

### Server local database = dictionary with 3 nested dictionaries:

#dict - key = filename, contains list of all node addresses that have the file
#listOffiles['index.jpeg'] = ["http://127.0.0.1:5002/", "http://127.0.0.1:5002/"]

#dict - key = filename, contains list of all files and their current version
#fileVersion['index.jpeg'] = 1

#dict - key = filename, used to divide work between nodes
#fileAccessCount['index.jpeg'] = [10(Number of downloads), 3(Number of nodes the file is on)] #First index is amount of times it has been accessed, second is number of nodes that have it

listOfFiles = {'nodeAddresses': {},
                'fileAccessCount' : {},
                'fileVersion': {}
                }

#dict - key = nodeID, contains list of all node addresses
#connectedNodes[1] = ["http://127.0.0.1:5001/", 2(This is thenumberOfFiles)]
connectedNodes = {}

UPLOAD_FOLDER ='/home/donal-tuohy/Documents/SS_year/DFS/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

### LOCAL FUNCTIONS ###

#Pass in an address and it will return the node ID as an int
def parseNodeID(address):
    split = address.split(':')
    port = int((split[2])[:4])
    return port - 5000

#Pass in a dict of files {"index.jpeg": [address1, address2]}
def addFilesFromNode(dictOfFiles, nodeAddress):

    #for each file in the passed in dictionary
    for fileName in dictOfFiles:
        #Check if there is a file with this name already on the server
        if fileName in (listOfFiles['nodeAddresses']).keys():
            ((listOfFiles['fileVersion'])[fileName]) += 1
            #If the address of the current node isn't already stored, add it to the list of addresses associated with this file
            if nodeAddress not in ((listOfFiles['nodeAddresses'])[fileName]):
                ((listOfFiles['nodeAddresses'])[fileName]).append(nodeAddress)
                ((listOfFiles['fileAccessCount'])[fileName])[1] += 1     #Add to the total number of nodes that have the file 
        #If the file does not exist on the global list of files, create a new key with the filename        
        else:
            ((listOfFiles['nodeAddresses'])[fileName]) = [nodeAddress]
            ((listOfFiles['fileAccessCount'])[fileName]) = [0,1]     
            ((listOfFiles['fileVersion'])[fileName]) = 1  


#This works out where the file was downloaded most recently and preforms round robin to make sure the file is downloaded fairly from nodes
def roundRobin(filename):
    myList = ((listOfFiles['fileAccessCount'])[filename])
    indexOfNodeToUse = (myList[0])%(myList[1])
    ((listOfFiles['fileAccessCount'])[filename])[0] += 1
    return indexOfNodeToUse 


def nodeToUploadTo():
    minIndex = 1
    minValue = ((connectedNodes[1])[1])
    for node in connectedNodes.keys():
        if(connectedNodes[node])[1] < minValue:
            minIndex = node
    return (connectedNodes[minIndex])[0]    #Returning address to upload to

### ENDPOINTS ###


#When a new node is created it will send a POST request to this endpoint
#The request will contain a json file with all the node's details and files that it has
@app.route('/newnode', methods=['POST'])
def newNode():
    response = request.get_json()
    if (response):
        newNodeID = response['nodeID']
        newNodeAddr = response['address']
        dictOfFiles = response['currentFiles']
        addFilesFromNode(dictOfFiles, newNodeAddr)
        print("File Versions: ",listOfFiles['fileVersion'])
        connectedNodes[newNodeID] = [newNodeAddr, len(dictOfFiles)]
        return jsonify({'message': 'Node successfuly set up.'})
    else:
        return jsonify({'message': 'Node could not be set up.'})


#This endpoint is accessed by a node when it gets a new file. It updates the list of files
@app.route('/newfile', methods=['POST'])
def newFile():
    data = request.get_json()
    nodeAddress = data['nodeAddress']
    dictOfFile = data['fileName']
    addFilesFromNode(dictOfFile,nodeAddress)
    (connectedNodes[parseNodeID(nodeAddress)])[1] += 1
    print("File Versions: ",listOfFiles['fileVersion'])
    return "File added to global list"


#This endpoint returns a dict of all the files stored on the server
@app.route('/returnlist', methods=['GET'])
def returnFiles():
    return jsonify(listOfFiles['nodeAddresses'])


#This endpoint is used to check if a file exists on the server.
@app.route('/uploadcheck/<filename>', methods=['GET'])
def upload_file_check(filename):
    print("Filename: ", filename)
    if filename in (listOfFiles['nodeAddresses']):
        return jsonify({'message': 'File already exists.', 'nodeAddresses': ((listOfFiles['nodeAddresses'])[filename]), "addressToUploadTo": nodeToUploadTo()  })
    
    return jsonify({'message': 'File does not exist.', "addressToUploadTo": nodeToUploadTo() })

@app.route('/version/<filename>', methods=['GET'])
def getVersion(filename):
    return jsonify({'fileVersion': ((listOfFiles['fileVersion'])[filename]) })

#If client wants to get a file, it sends a get request to this URL
#This server checks it's list of files and returns the address of the node which should be accessed next
@app.route('/download/<filename>')
def download_file(filename):
    if filename in (listOfFiles['nodeAddresses']).keys():
        nodeAddress = (((listOfFiles['nodeAddresses'])[filename])[roundRobin(filename)])
        return jsonify({'message': 'File exists.', 'address': ( nodeAddress + filename), 'nodeID': parseNodeID(nodeAddress)})
    else:
        return jsonify({'message': 'File does not exist.'})


if __name__ == "__main__":
    app.run(debug=True)