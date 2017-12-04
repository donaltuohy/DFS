import requests, shutil, profile, io, os, pathlib
from shutil import copyfile
from datetime import datetime
CLIENT_FOLDER = '/home/donal-tuohy/Documents/SS_year/DFS/clientDirectory/clientFiles/CLIENT_'
CACHE_FOLDER = '/home/donal-tuohy/Documents/SS_year/DFS/clientDirectory/clientFiles/CACHE_'
CACHE_TIMEOUT = 1 #In minutes

def printListOfFiles(clientId):
    fileList = os.listdir(CLIENT_FOLDER + str(clientId))
    fileList = sorted(fileList)
    print("Files stored in client folder.")
    print("________________________________")
    for fileName in fileList:
         print(fileName)
    print("\n\n")

#When node starts up, all existing files are presumed to be out of date
def updateCacheList(clientID, cachedFilesList):
    fileList = os.listdir(CLIENT_FOLDER + str(clientID))
    for fileName in fileList:
        if fileName not in cachedFilesList.keys():
         cachedFilesList[fileName] = ["0", "0", "0", 0]

#Returns the dict of server files
def getServerDict():
    files = requests.get("http://127.0.0.1:5000/returnlist")
    return files.json()

#Prints all the files stored on the server
def printServerFiles():
    fileList = getServerDict()
    print("Files stored on the server")
    print("________________________________")
    for filename in fileList.keys():
        print(filename)
    print("\n\n")

def doesCacheExists(filename, clientID):
    if filename in os.listdir(CACHE_FOLDER + str(clientID)):
        return True
    return False

def doesFileExists(filename, clientID):
    if filename in os.listdir(CLIENT_FOLDER + str(clientID)):
        return True
    return False

def getFileVersion(filename):
    response = requests.get('http://127.0.0.1:5000/version/' + filename)
    serverJsonResponse = response.json()
    return serverJsonResponse['fileVersion']

def createFolders(clientID):
    pathlib.Path(CACHE_FOLDER + str(clientID)).mkdir(parents=True, exist_ok=True)
    pathlib.Path(CLIENT_FOLDER + str(clientID)).mkdir(parents=True, exist_ok=True)
    print("Client & cache folders created.")
    
def getFileFromCache(filename, clientID):
    if doesCacheExists(filename, clientID):
        files = {'file': open(CACHE_FOLDER + str(clientID) + '/' + filename, 'rb')}
        return files     
    return "File doesn't exist"

def getFile(filename, clientID):
    if doesFileExists(filename, clientID):
        files = {'file': open(CLIENT_FOLDER + str(clientID) + '/' + filename, 'rb')}
        return files     
    return "File doesn't exist"

def parseCurrentTime():
    currentTime = (str(datetime.now())).split()
    date = currentTime[0]
    time = ((currentTime[1]).split('.'))[0]
    time = time.split(":")
    hours = time[0]
    minutes = time[1]
    return date, hours, minutes

#Returns how old the cache is in minutes
def getCacheAge(cacheTime):
    currDate, currHours, currMinutes = parseCurrentTime()
    currTotalMinutes = (int(currHours)*60) + (int(currMinutes))
    cacheTotalMinutes = ((int(cacheTime[1]))*60) + (int(cacheTime[2]))
    return currTotalMinutes - cacheTotalMinutes

def createNewFileName(filename):
    splitName = filename.split('.')
    return splitName[0] + '(1).' + splitName[1]

#Will first check that the cache is from this day, then checks if the time is wihtin ten minutes
def checkIfCacheOkay(filename, cachedFilesList):
    if filename in cachedFilesList.keys():
        if(getFileVersion(filename) == (cachedFilesList[filename])[3]):
            date, hours, minutes = parseCurrentTime()
            if ((cachedFilesList[filename])[0] == date):
                age = getCacheAge(cachedFilesList[filename])
                if(age < CACHE_TIMEOUT):
                    return True
        print("Cached file version is not up to date. Fetching updated version.")
    return False


def downloadFile(filename, clientID, cachedFilesList):
    if checkIfCacheOkay(filename, cachedFilesList):
        cachedFile = getFileFromCache(filename,clientID)
        copyfile((CACHE_FOLDER + str(clientID) + "/" + filename),(CLIENT_FOLDER + str(clientID) + "/" + filename))
        prompt()
        print("Cached file downloaded from: Date:" + (cachedFilesList[filename])[0] + " Time: " + (cachedFilesList[filename])[1] + ":" +(cachedFilesList[filename])[2]  )
        return
    filecheck = requests.get("http://127.0.0.1:5000/download/" + filename)
    if (filecheck.ok):
        print("filecheck is okay")
        serverJsonResponse = filecheck.json()
        if (serverJsonResponse['message'] == "File exists."):
            print("About to send get request")
            fileRequest = requests.get(serverJsonResponse['address'])
            print("Get request sent")
            with open(CLIENT_FOLDER + str(clientID) + "/" + filename, 'wb') as handler:
                handler.write(fileRequest.content)
            with open(CACHE_FOLDER + str(clientID) + "/" + filename, 'wb') as handler:
                handler.write(fileRequest.content)
            del fileRequest
            date, hours, minutes = parseCurrentTime()
            cachedFilesList[filename] = [date, hours, minutes, getFileVersion(filename)]
            prompt()
            print(filename, "has been downloaded and added to the cache.")
        else:
            print(filename, "does not exist on server.")
    else:
        print("Request failed.")
    return



def uploadFile(filename, clientID, fileVersion, cachedFilesList):
    if not doesFileExists(filename, clientID):
        print(filename + " doesn't exist in the client folder.")
        return
    overwriteFlag = False
    filecheck = requests.get("http://127.0.0.1:5000/uploadcheck/" + filename)
    if filecheck.ok:
        serverJsonResponse = filecheck.json()
        if serverJsonResponse['message'] == 'File already exists.':
            serverVersion = getFileVersion(filename)
        
            if(serverVersion > fileVersion):
                print("This file is outdated. Please download the new version from the server.\nServer version: " + str(serverVersion) + "\nYour version: " + str(fileVersion))
                return fileVersion
        
            while not overwriteFlag:
                print("File with that name already exists on server.")
                choice = input("Would you like to overwrite it? (y/n):")
                
                if choice == 'y':
                    files = getFile(filename,clientID)
                    fileVersionDict = {'fileVersion' : fileVersion}
                    print("Uploading to: " ,serverJsonResponse['nodeAddresses'])
                    listOfNodes = serverJsonResponse['nodeAddresses']
                    for nodeAddress in listOfNodes:
                        upload = requests.post(nodeAddress + 'upload', files=files, json=fileVersionDict)
                        if upload.ok:
                            print("Uploaded to " + nodeAddress)
                            fileVersion += 1
                        else:
                            print("Could not upload to " + nodeAddress)
                        del upload
                    return fileVersion
                    overwriteFlag = True

                elif choice == 'n':
                    newFilename = createNewFileName(filename)
                    choice = input("Would you like to create " + newFilename + "? (y/n):")
                    if choice == 'y':
                        copyfile((CLIENT_FOLDER + str(clientID) + "/" + filename),(CLIENT_FOLDER + str(clientID) + "/" + newFilename))
                        files = getFile(newFilename, clientID)
                        uploadAddress = serverJsonResponse['addressToUploadTo']
                        print("Uploading to ", uploadAddress)
                        upload = requests.post(uploadAddress + 'upload', files=files)
                        if upload.ok:
                            print("Uploaded to " + uploadAddress)
                            downloadFile(newFilename,clientID,cachedFilesList)
                            return 1
                        else:
                            print("Could not upload to server")
                            return 1
                        del upload
                    elif choice == 'n':
                        print(chr(27) + "[2J")
                        prompt()
                        print("Upload cancelled.") 
                        overwriteFlag = True
                        return fileVersion
                    print("Invalid answer.")
                
                else:
                    print("Invalid answer.")
        
        elif serverJsonResponse['message'] == 'File does not exist.':
            files = getFile(filename, clientID)
            uploadAddress = serverJsonResponse['addressToUploadTo']
            upload = requests.post(uploadAddress + 'upload', files=files)
            if upload.ok:
                print("Uploaded to " + uploadAddress)
                return 1
            else:
                print("Could not upload to server")
                return 1
            del upload

def removeFile(filename):
    response = requests.post("http://127.0.0.1:5000/remove/" + filename)
    if response.ok:
        print("<" + filename + "> has been deleted form the server")
    else:
        print("<" + filename + "> could not be deleted.")

def backupFile(filename):
    filecheck = requests.get("http://127.0.0.1:5000/backupcheck/" + filename)
    if filecheck.ok:
        serverJsonResponse = filecheck.json()
        if serverJsonResponse['message'] == 'File already exists.':
            addr = serverJsonResponse['addressToUploadTo']
            print("Backing up to:", addr)
            backup = requests.get(addr[0] + "backup/" + filename)
            if backup.ok:
                print("File backed up succesfully")
        else:
            print("Cannot backup")

def prompt():
    print("Hello. Welcome to Donal's DFS.")
    print("________________________________\n")
