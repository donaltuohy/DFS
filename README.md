# Distributed file system

## Overview
This reposistory contains the files I have created to implement a Distributed File System. There are several parts to the system which can be seen in figure 1.

![Distributed File System Diagram](https://user-images.githubusercontent.com/20796292/33880900-05061398-df2b-11e7-845e-a4eafbca43bf.png "Figure 1: Distributed File System Diagram")
*Figure 1: Distributed File System Diagram* 

The system is built using two python scripts and then accessed using a python library of functions which I have created. The system runs locally with each node on a different port.

### mainServer.py
This file is the script for the directory server. It acts as a go between for clients and nodes. It is essential for maintaining the system as every request and action that is perfomed is dealt with by this server.

Using the flask module, I was able to create a series of endpoints on the server which would make it act as an API. The clients and nodes can send requests to these endpoints to find the node address, file name, file version, etc.. for the task they want to complete. 

I have built this server using several key global dictionaries. Using these allowed for very fast access to files rather than having to iterate through a list. This fast access was very useful as the server may have many requests in a short period of time.

The server runs on localhost 127.0.0.1. To run this script in terminal. Set the path to the directory and call:

>*python3.6 mainServer.py*

### nodeServer.py
This file is the script used to create a node. Every active node uses this script and it take in 1 argument which is that nodes ID. The node will then take this ID and add it to 5000 to get the port number it will run on (ie. Node ID = 8, port = 5008).

When a node is initialised, it will check if it has a unique directory to store files. If it doesn't, it will automatically create one (eg. "NODE_8"). It will then send an intialisation POST request to the main server. This request contains a json file with all of the files stored at that node. The server then takes in this information and will use it for when a client wants this nodes files.          


## Distributed Transparent File Access

## Directory Service

## Caching

## Lock Service

## Replication
