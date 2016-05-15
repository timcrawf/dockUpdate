from optparse import OptionParser
import grp
import os
import pwd
import shutil
import sys

parser=OptionParser()
parser.add_option('-f', '--file', dest='fileName', help = 'Enter path to your new dock file.')
parser.add_option('-e', '--excluded', dest='excludedUsers', help='Enter the names of users to exclude from the new dock.')
parser.add_option('-g', '--group', dest='groupParse', help='Enter the name of the master group')
parser.add_option('-i', '--include', dest='includeParse', help='If you only wish to update one user, enter their name in this option')
(options, args)=parser.parse_args()

if options.fileName is None:
    print'----ERROR----'
    print '--Please use "-f" to select a file--'
    sys.exit()
else:
    newFile=options.fileName

if options.excludedUsers is None:
    exUser=[]
else:
    exUserPre=options.excludedUsers
    exUser=exUserPre.split(',')
exUser.append('Shared')

if options.groupParse is None:
    print'----ERROR----'
    print '--Please use "-g" to select group assignment-'
    sys.exit()
else:
    groupName=options.groupParse
    
delList=[]
groupList = grp.getgrnam(groupName)
groupNum=groupList[2]

usersDir='/Users'

if options.includeParse is None:
    userList=os.listdir(usersDir)
    for user in userList:
        if user.startswith('.'):
            delList.append(user)
        for ex in exUser:
            if ex==user:
                delList.append(ex)
    for line in delList:
        userList.remove(line)
else:
    userList=[options.includeParse]
    

for user in userList:
    userNum=pwd.getpwnam(user)[2]
    userPath=os.path.join(usersDir, user)
    prefPath=os.path.join(userPath, 'Library/Preferences/')
    dockPath=os.path.join(prefPath, 'com.apple.dock.plist')
    try:
        os.remove(dockPath)
    except:
        None
    shutil.copyfile(newFile, dockPath)
    os.chown(dockPath, userNum, groupNum)
print 'Compleated'

print userList
