import requests, shutil, profile, io

def downloadFile(filename):
    filecheck = requests.get("http://127.0.0.1:5000/download/" + filename)
    if filecheck.ok:
        serverJsonResponse = filecheck.json()
        if serverJsonResponse['message'] == "File exists.":
            fileRequest = requests.get(serverJsonResponse['address'])
            with open("./clientFiles/" + filename, 'wb') as handler:
                handler.write(fileRequest.content)
            del fileRequest
            print(filename, "has been downloaded.")
        else:
            print(filename, "does not exist on server.")
    else:
        print("Request failed.")

    return


print("Hello. Welcome to Donal's DFS.")
print("________________________________\n")

while True:
    filename = input("Enter file name to download:")
    downloadFile(filename)


