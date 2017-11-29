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
    if doesFileExists(filename):
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

#Will first check that the cache is from this day, then checks if the time is wihtin ten minutes
def checkIfCacheOkay(filename, cachedFilesList):
    if filename in cachedFilesList.keys():
        date, hours, minutes = parseCurrentTime()
        if ((cachedFilesList[filename])[0] == date):
            age = getCacheAge(cachedFilesList[filename])
            if(age < CACHE_TIMEOUT):
                return True
        print("Cached file is out of date. Fetching updated version.")
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
        serverJsonResponse = filecheck.json()
        if (serverJsonResponse['message'] == "File exists."):
            fileRequest = requests.get(serverJsonResponse['address'])
            with open(CLIENT_FOLDER + str(clientID) + "/" + filename, 'wb') as handler:
                handler.write(fileRequest.content)
            with open(CACHE_FOLDER + str(clientID) + "/" + filename, 'wb') as handler:
                handler.write(fileRequest.content)
            del fileRequest
            date, hours, minutes = parseCurrentTime()
            cachedFilesList[filename] = [date, hours, minutes]
            prompt()
            print(filename, "has been downloaded and added to the cache.")
        else:
            print(filename, "does not exist on server.")
    else:
        print("Request failed.")
    return

def uploadFile(filename):
    if not doesFileExists(filename):
        print(filename + " doesn't exist in the client folder.")
        return
    overwriteFlag = False
    filecheck = requests.get("http://127.0.0.1:5000/uploadcheck/" + filename)
    if filecheck.ok:
        serverJsonResponse = filecheck.json()
        print(serverJsonResponse)
        if serverJsonResponse['message'] == 'File already exists.':
            while not overwriteFlag:
                print("File with that name already exists on server.")
                choice = input("Would you like to overwrite it? (y/n):")
                if choice == 'y':
                    files = getFile(filename)
                    for nodeAddress in serverJsonResponse['nodeAddresses']:
                        upload = requests.post(nodeAddress + 'upload', files=files)
                        if upload.ok:
                            print("Uploaded to " + nodeAddress)
                        else:
                            print("Could not upload to " + nodeAddress)
                        del upload
                    overwriteFlag = True
                elif choice == 'n':
                    print(chr(27) + "[2J")
                    prompt()
                    print("Upload cancelled.") 
                    overwriteFlag = True
                    return
                else:
                    print("Invalid answer.")
        elif serverJsonResponse['message'] == 'File does not exist.':
            ###For now jujst send it to node 1!!!!
            files = getFile(filename)
            uploadAddress = serverJsonResponse['addressToUploadTo']
            upload = requests.post(uploadAddress + 'upload', files=files)
            if upload.ok:
                print("Uploaded to " + uploadAddress)
            else:
                print("Could not upload to server")
            del upload

def prompt():
    print("Hello. Welcome to Donal's DFS.")
    print("________________________________\n")

