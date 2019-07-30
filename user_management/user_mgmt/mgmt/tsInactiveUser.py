# In pythin we need to import these to work with sessions and with JSON.
import json
import requests
import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import subprocess, shlex

thoughtspot_host = 'https://10.85.79.254'

session = requests.session()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session.verify = False
session.headers = {"X-Requested-By": "ThoughtSpot"}

credentials = {"username": "tsadmin", "password": "admin", "rememberme": True}

login = session.post(thoughtspot_host + '/callosum/v1/tspublic/v1/session/login', data=credentials)
if login.status_code != 204:
    print "Server connection failed. Status code: " + str(login.status_code)

checklogin = session.get(thoughtspot_host + '/callosum/v1/session/info')
response = json.loads(checklogin.text)
if "BTADMIN" == response['userName']:
    print "all OK"
else:
    print "Server connection failed. Status code: " + str(checklogin.status_code)


# allUsersJson = session.get(thoughtspot_host + '/callosum/v1/tspublic/v1/user/list' )
# allUsers = json.loads(allUsersJson.text)
#
# allUserList = []
#
# for usrs in allUsers:
#     if usrs['name'] not in ['tsadmin','system','su','System','Administrator']:
#         allUserList.append(usrs['name'])

objectTypeList = ["PINBOARD_ANSWER_BOOK", "QUESTION_ANSWER_BOOK", "LOGICAL_TABLE","USER"]
userList = []
objectAuthorList=[]
userListDict = {}
for objectType in objectTypeList:
    print objectType
    objectJson = session.get(thoughtspot_host + '/callosum/v1/tspublic/v1/metadata/listobjectheaders?type=' + objectType + '&category=ALL&sort=DEFAULT&offset=-1')
    getObject = json.loads(objectJson.text)


for objectType in objectTypeList:
    print(objectType)
    objectJson = session.get(thoughtspot_host + '/callosum/v1/tspublic/v1/metadata/listobjectheaders?type=' + objectType + '&category=ALL&sort=DEFAULT&offset=-1')
    getObject = json.loads(objectJson.text)

    if(objectType != "USER"):
        for jsonObject in getObject:
            objectAuthorList.append(jsonObject['author'])
    else:
        for jsonObject in getObject:
            userListDict[jsonObject['id']] = jsonObject['name']

for key, val in userListDict.iteritems():
    if key not in objectAuthorList:
        print key, val
        userList.append(key)

print(userList)

params = {"ids": json.dumps(userList)}

print params


#/*ADDED BY RAJESH*/
userString = ', '.join(userList)
userString = "\"" + userString + "\""

#print userString

response = session.post(thoughtspot_host + "/callosum/v1/session/user/deleteusers", data=params)

print response.status_code

#command_line = "python user_management/user_mgmt/ts_ug_util.py --ts_url " +thoughtspot_host +" --username "+  credentials["username"] + " --password " + credentials["password"] + " delete --users "
#args = shlex.split(command_line)
#args.append(userString)
#print args
#p = subprocess.Popen(args)
#p.poll()


