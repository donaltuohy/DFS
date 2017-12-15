# Distributed file system

Student Name: Donal Tuohy

Student Number: 14313774

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
The next service I implemented was the directory service which acts a go-between for clients and nodes.

Whenever a client wants to perform an action it must check in with the server prior to completing that action.

When uploading a file, the client sends a request to the server asking to upload. The server then figures out which node has the least amount of files and returns the address of that node to the client. Once the client has uploaded the file to that node, the node posts a request to the server notifying it about the new file. 
The server then stores the name of the file and the address of the node it is stored on.

One problem that I found with this solution was that if many upload request are sent in a short period, they will all be sent to the same node as the notification is sent to the server after the file has been uploaded. For example, a client could be told to upload to a node while another file is still uploading. This would create an imbalance in the number of files per node. However it would balance itself out over time.

![Uploading a file through the directory server.](https://user-images.githubusercontent.com/20796292/34057126-a966c1ae-e1cd-11e7-85a1-c55c1dde4810.png)
*Figure 3: Uploading a file through the directory server.* 

When downloading a file, the client again sends a request to the directory server asking to download a certain filename. If the file exsists the server replies with the address of the node that file is stored at. The client then downloads that file from the node address that was sent to it. 
![Downloading a file through the directory server.](https://user-images.githubusercontent.com/20796292/34057565-6802751c-e1cf-11e7-8778-e6b0221ee535.png)
*Figure 4: Downloading a file through the directory server.*   

## Caching
Once the directory server was working correctly, I decided to implement caching so that each client could store versions of files locally.

I started by having the client automatically create a directory for its cached files. The client also keeps a dictionary of the files that are cached. Using the cache dictionary and directory, the client is able to maintain a cache with timestamp values.

I have created a check cache function in the client library which checks if the cache is older than a set timeout value in minutes. 

So when a client wants to download a file, it will first check if there is a cached version of the file and if it is up to date. If so, the client will then copy this file from it's cache directory into its local directory.

When a client is uploading, it will also update the cache dictionary and directory with the file been uploaded as that file with be the one stored on the server and will therefore be up to date at that time.

## Replication
To get replication working on this distributed file system, I started creating a backup function. When this function is called, it takes a file and backs it up on one node that doesn't store the file. This means that there can be one file on multiple nodes. This is an advantage for security but what if a client uploads another version?

To deal with this, I edited the upload function so that when a client asks to upload an existing file, it will recieve the address of every node that file is currently stored on. Every node will get the updated version and overwrite their older version.

There was also a problem if say client 1 and client 2 downloaded the same file. When one of these clients uploads their updated file, it would be overwritten when the other client uploads their updated file. 

To combat this, I implemented, file versions. The directory server would store an integer for each file which would be updated everytime a new version was uploaded. The client cache list also stored the local file version so that it could be compared with the server version.

If a client tries to upload a file which is behind the server version, the client will be denied. I also implemented service which allows the user to upload the file but with a number at the end of the name eg. "test(1).txt".

![Uploading replicas](https://user-images.githubusercontent.com/20796292/34057938-13075544-e1d1-11e7-97a0-dc7e54e55667.png)
*Figure 5: Uploading replicas.*

When downloading a file that is replicated several times across different nodes, I have created a round robin function. This function allows the client to download the file from the node that has been accessed least. So if a file is stored on two nodes, each time the file is downloaded it will get it from the other node. This helps balance the load on the nodes if lots of download requests are been sent.

## Lock Service
For locking files I have created another dictionary on the directory server which stores a list of all the file, whether they are locked and if so, the client that locked them.

This way when a client wants to upload or download a file, they must acquire the lock on it. So if client 1 downloads a file, no other client can access that file until client 1 uploads the file and the lock is removed.



