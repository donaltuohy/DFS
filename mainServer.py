import os, requests, nodesConfig
from flask import Flask, render_template, url_for, request, session, flash, redirect, send_from_directory, jsonify
from flask.ext.pymongo import PyMongo
from werkzeug.utils import secure_filename


connectedNodes = {}
UPLOAD_FOLDER ='/home/donal-tuohy/Documents/SS_year/DFS/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#If client wants to get a file, it sends a get request to this URL
#This server checks if it is stored in the node and if so, returns the address of the node to the client
@app.route('/download/<filename>')
def download_file(filename):
    # response = requests.get("http://127.0.0.1:5001/servercheck/" + filename)
    # if response.ok:
    #     responseJson = response.json()
    #     message = responseJson['message']
    #     if message == "File on node.":
    #         return jsonify({'message': 'File exists.', 'address': ("http://127.0.0.1:5001/" + filename)})
    #     elif message == "File does not exist.":
    #         return jsonify({'message': message })
    #     else:
    #         return "ERROR MATE"
    # return "RESPONSE NOT OKAY"

    #TOO COMPLICATED TOO SOON, DO TIS AFTER ONE NODE WORKS
    for node in connectedNodes:
        response = requests.get(connectedNodes[node] + "servercheck/" + filename)
        if response.ok:
            print(response.json())
            response2 = response.json()
            message = response2['message']
            if message == "File on node.":
                print("File found on: ", connectedNodes[node])
                return jsonify({'message': 'File exists.', 'address': (connectedNodes[node] + filename), 'nodeID': node})
            elif message == "File does not exist.":
                print("File not on: ", connectedNodes[node])
                pass # jsonify({'message': 'File doesnt exist',  'address': (connectedNodes[node] + filename), 'nodeID': node})
            else:
                return "ERROR MATE"
        del response
    return "RESPONSE NOT OKAY"



@app.route('/newnode', methods=['POST'])
def newNode():
    response = request.get_json()
    newNodeID = response['nodeID']
    newNodeAddr = response['address']
    connectedNodes[newNodeID] = newNodeAddr
    
    print("Node " + str(newNodeID) +" connected on " + newNodeAddr + ".")
    print(connectedNodes)
    return "Hello" #request.get_json()



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == "__main__":
    app.run(debug=True)