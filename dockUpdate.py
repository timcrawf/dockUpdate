from optparse import OptionParser
import grp
import os
import pwd
import shutil
import sys

def errorMessage(parser): # Error message to appear if you are missing information
    ending=lambda ending: if ending=='-f': return 'to select a file', if ending=='-g': return 'to define the group')
    print'----ERROR----'
    print '--Please use "%s" %s--' % (parser, ending(parser))
    sys.exit() #Quits the script

usersDir='/Users' #Set the start of the directory to have the user inserted
delList=[] #Create empty list to add excluded users and invisible files
delList.append('Shared') #Automaticly remove the Shared user so the program doesn't error

parser=OptionParser()
parser.add_option('-f', '--file', dest='fileName', help = 'Enter path to your new dock file.')
parser.add_option('-e', '--excluded', dest='excludedUsers', help='Enter the names of users to exclude from the new dock.')
parser.add_option('-g', '--group', dest='groupParse', help='Enter the name of the master group')
parser.add_option('-i', '--include', dest='includeParse', help='If you only wish to update one user, enter their name in this option')
(options, args)=parser.parse_args()

if options.fileName is None:
    errorMessage('-f')
else:
    newFile=options.fileName

if options.excludedUsers is None:
    exUser=[]
else:
    exUserPre=options.excludedUsers
    exUser=exUserPre.split(',')

if options.groupParse is None:
    errorMessage('-g')
else:
    groupName=options.groupParse
    groupList = grp.getgrnam(groupName) #Uses grep to get a list for the group containing the id number
    groupNum=groupList[2] #Retrive the group number from the list

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
