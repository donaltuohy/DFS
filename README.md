# Distributed file system

## Overview
This reposistory contains the files I have created to implement a Distributed File System. There are several parts to the system which can be seen in figure 1.

![Distributed File System Diagram](https://user-images.githubusercontent.com/20796292/33880900-05061398-df2b-11e7-845e-a4eafbca43bf.png "Figure 1: Distributed File System Diagram")
*Figure 1: Distributed File System Diagram* 

The system is built using two python scripts and then accessed using a python library of functions which I have created. The system runs locally with each node on a different port.

### [mainServer.py](https://github.com/donaltuohy/DFS/blob/master/mainServer.py)
This file is the script for the directory server. It acts as a go between for clients and nodes. It is essential for maintaining the system as every request and action that is perfomed is dealt with by this server.

Using the flask module, I was able to create a series of endpoints on the server which would make it act as an API. The clients and nodes can send requests to these endpoints to find the node address, file name, file version, etc.. for the task they want to complete. 

I have built this server using several key global dictionaries. Using these allowed for very fast access to files rather than having to iterate through a list. This fast access was very useful as the server may have many requests in a short period of time.

The server runs on localhost 127.0.0.1. To run this script in terminal, set the path to the file's directory and call:

>*python3.6 mainServer.py*

### [nodeServer.py](https://github.com/donaltuohy/DFS/blob/master/nodeServer.py)
This file is the script used to create a node. Every active node uses this script and it takes in 1 argument which is the nodes ID. The node will then take this ID and add it to 5000 to get the port number it will run on (ie. Node ID = 8, port = 5008).

When a node is initialised, it will check if it has a unique directory to store files. If it doesn't, it will automatically create one (eg. "NODE_8"). It will then send an intialisation POST request to the main server. This request contains a json file with all of the files stored at that node. The server then takes in this information and will use it for when a client wants this nodes files.   

A node has many endpoints but the main two are the upload and download enpoints. A client will send requests to these endpoints to send or recieve files.

To run this script in terminal, set the path to the file's directory and call:

>*python3.6 nodeServer.py node`ID(int)*

### [client.py](https://github.com/donaltuohy/DFS/blob/master/clientDirectory/client.py)        
This is the library of functions I have built which allow a client to interact with the distributed file server API. It uses the requests library in python.

There are functions for uploading and downloading files, backing up files, retrieving the list of files stored on the server and also recieving a list of the files stored on in the clients folder.  

This script does not need to be run. It is imported into the controller script, described next. 

### [controller.py](https://github.com/donaltuohy/DFS/blob/master/clientDirectory/controller.py) 
I created this script just as a way to demonstrate the services I have implemented in my distributed file system. 

Many of these scripts can be run at the same time once they have unique IDS. 

To run this script in terminal, set the path to the file's directory and call:

>*python3.6 contoller.py clientID(int)*

## Distributed Transparent File Access
The first service I imlplemented was distributed transparent file access. I did this by creating the basics of the nodeServer script.

The node has a directory that is associated with it. This directory stores the files that should be accessible by the client.

To upload a file, a client would send a POST request to the *'/upload'* endpoint. This endpoint then checks for an attached file and if it's okay, it adds the file to it's directory. This process can be seen by the red request in figure 2. 

To download a file, a client would send a GET request. The endpoint for this however, would be the file name the client wishes to download (eg. *'/file1.txt'*). The node would then seach for this file in it's directory and if it has it, send it back as a response to the request. This can be seen by the green request in figure 2.

![Transparent File Access Diagram](https://user-images.githubusercontent.com/20796292/33941766-9a5015c6-e00b-11e7-9197-713792f032c0.png)
*Figure 2: Transparent File Access Diagram* 



## Directory Service

## Caching

## Lock Service

## Replication
