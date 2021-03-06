from optparse import OptionParser
import grp
import os
import pwd
import shutil
import sys


class GenerateError:

    def __init__(self):
        self.errors={}
        return
        
    def addError(self, call, description):
        self.call=call
        self.description=description
        self.errors[self.call]=self.description
    
    def displayError(self):
        for key in self.errors:
            print '--Please use "%s" %s--' % (key, self.errors[key])
        exit()


def main():
    errorMessage=GenerateError()
    usersDir='/Users' #Set the start of the directory to have the user inserted
    delList=[] #Create empty list to add excluded users and invisible files
    delList.append('Shared') #Automaticly remove the Shared user so the program doesn't error

    parser=OptionParser()
    parser.add_option('-f', '--file', dest='fileName', help = 'Enter path to your new dock file.')
    parser.add_option('-e', '--excluded', dest='excludedUsers', help='Enter the names of users to exclude from the new dock.')
    parser.add_option('-g', '--group', dest='groupParse', help='Enter the name of the master group')
    parser.add_option('-i', '--include', dest='includeParse', help='If you only wish to update one user, enter their name in this option')
    (options, args)=parser.parse_args()

    if options.fileName is None:                                      #Checks to see if file argument was given
        errorMessage.addError("-f", "to select a file")        #Adds error message
    else:
        newFile=options.fileName                                     #converts newFile to local variable

    if options.groupParse is None:                                  #Checks to see if group argument was given
        errorMessage.addError("-g", "to enter the master group")     #adds error message
    else:
        groupName=options.groupParse                            #conver groupName to local variable
        groupList = grp.getgrnam(groupName) #Uses grep to get a list for the group containing the id number
        groupNum=groupList[2] #Retrive the group number from the list

    if errorMessage.errors != {}:                                       # Checks for any errors
        errorMessage.displayError()                                   # prints any errors then exits

    if options.excludedUsers is None:                               # Checks for excluded users argument
        exUser=[]                                                              # creates empty excluded users list
    else:
        exUserPre=options.excludedUsers                       #Converts string to local variable
        exUser=exUserPre.split(',')                                  #Creates list of string split at ","

    if options.includeParse is None:             #if there are no specified users
        userList=os.listdir(usersDir)            #retrive list of all users on the computer
        for user in userList:
            if user.startswith('.'):            #looks for hidden folders
                delList.append(user)            #adds them to the delete list
            for ex in exUser:
                if ex==user:
                    delList.append(ex)          #adds exculded users to delete list
        for line in delList:
            userList.remove(line)               #removes all unwated users from user list
    else:
        userList=[options.includeParse]    #if specified makes user list just the spicific users
    
    for user in userList:
        userNum=pwd.getpwnam(user)[2]     #gets user id number
        userPath=os.path.join(usersDir, user)
        prefPath=os.path.join(userPath, 'Library/Preferences/')   #joins paths for prefrences
        dockPath=os.path.join(prefPath, 'com.apple.dock.plist')   #joins path for dock plist
        try:
            os.remove(dockPath)        #trys to remove dock plist if it exists
        except:
            None
        shutil.copyfile(newFile, dockPath)      #copies new dock file
        os.chown(dockPath, userNum, groupNum)   #changes ownership of dock plist to specified user
        os.chmod(dockPath, 0o600)               #changes permissions for current user
    print 'Compleated'                          #lets you know the process is complete

    print userList                      #prints list of all modified users

if __name__ == "__main__":
    main()
