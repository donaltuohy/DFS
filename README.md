# Distributed file system

## Overview
This reposistory contains the files I have created to implement a Distributed File System. There are several parts to the system which can be seen in figure 1.

![Distributed File System Diagram](https://user-images.githubusercontent.com/20796292/33880900-05061398-df2b-11e7-845e-a4eafbca43bf.png "Figure 1: Distributed File System Diagram")
*Figure 1: Distributed File System Diagram* 

The system is built using two python scripts and then accessed using a python library of functions which I have created.

### mainServer.py
This file is the script for the directory server. It acts as a go between for clients and nodes. It is essential for maintaining the system as every request and action that is perfomed is dealt with by this server.

Using the flask module, I was able to create a series of endpoints on the server which would make it act as an API. The clients and nodes can send requests to these endpoints to find the node address, file name, file version, etc.. for the task they want to complete. 

I have built this server using several key global dictionaries. Using these allowed for very fast access to files rather than having to iterate through a list.      


## Distributed Transparent File Access

## Directory Service

## Caching

## Lock Service

## Replication
