import sys
from client import *

#returns the Id of this current node
def getClientID():
    if(len(sys.argv) > 0):
        return int(sys.argv[1])
    return 1

clientID = getClientID()
createFolders(clientID)

##                                                            |Date[0]     |   Hour[1]|   Minute[2]|   Version[3]|
##Keeps track of all cached files  cachedFiles['index.pdf'] = ['2017-11-30',      '13',        '03',            2]
cachedFiles = {}
updateCacheList(clientID, cachedFiles)


print(chr(27) + "[2J")

while True:

    

    choice = input("\nTo upload a file, press 1.\nTo download a file press 2.\nTo remove a file from the server press 3\nTo show all files on the server press 4.\nTo show all local files press 5.\nYour choice: ")
    

    ### USING UPLOAD FUNCTION   ### 
    if (choice == '1'):
        #Anytime you go to upload, refresh the cahe to see if files have been moved to the client folder
        updateCacheList(clientID, cachedFiles)

        print(chr(27) + "[2J")
        printListOfFiles(clientID)
        
        filename = input("Enter file name to upload:")
        print(chr(27) + "[2J")
        if filename in cachedFiles.keys():
            (cachedFiles[filename])[3] = uploadFile(filename, clientID, (cachedFiles[filename])[3], cachedFiles )
        else:
            print("That file does not exist")

    ### USING DOWNLOAD FUNCTION ###
    elif (choice == '2'):
        print(chr(27) + "[2J")
        printServerFiles()
        
        filename = input("Enter file name to download:")
        print(chr(27) + "[2J")
        downloadFile(filename, clientID, cachedFiles)

    elif (choice == '3'):
        print(chr(27) + "[2J")
        printServerFiles()
        filename = input("Enter file name to delete:")
        print(chr(27) + "[2J")

        listOfFiles = getServerDict()
        if filename in listOfFiles.keys():
            removeFile(filename)
        else:
            print("File doesn't exsist on server.")


    ### PRINT FILES ON SERVER   ###
    elif (choice == '4'):
        print(chr(27) + "[2J")
        printServerFiles()

    ### PRINT LOCAL FILES
    elif (choice == '5'):
        print(chr(27) + "[2J")
        printListOfFiles(clientID)



    else:
        print("Invalid value entered.")


