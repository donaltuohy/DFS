import sys
from client import *

#returns the Id of this current node
def getClientID():
    if(len(sys.argv) > 0):
        return int(sys.argv[1])
    return 1

clientID = getClientID()
cachedFiles = {}
createFolders(clientID)


while True:

    choice = input("\nTo upload a file, press 1.\nTo download a file press 2.\nTo show all files on the server press 3.\nTo show all local files press 4.\nYour choice: ")
    
    if (choice == '1'):
        print(chr(27) + "[2J")
        printListOfFiles(clientId)
        filename = input("Enter file name to upload:")
        print(chr(27) + "[2J")
        uploadFile(filename)

    elif (choice == '2'):
        print(chr(27) + "[2J")
        printServerFiles()
        filename = input("Enter file name to download:")
        print(chr(27) + "[2J")
        downloadFile(filename, clientID, cachedFiles)

    elif (choice == '3'):
        print(chr(27) + "[2J")
        printServerFiles()

    elif (choice == '4'):
        print(chr(27) + "[2J")
        printListOfFiles()

    else:
        print("Invalid value entered.")


