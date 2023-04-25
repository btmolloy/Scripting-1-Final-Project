#!/usr/bin/python
import argparse as ap
from ftplib import FTP

def fileCheck(IP_ADDRESS:str, ??? ):
    #function should return list of files that have been modified in last 3 weeks - also it should loop through them and print them out to console
    #Im not sure what args are needed for this function so just fill them in as you go
    ftpserver = FTP(IP_ADDRESS)
    
    ftpServer.login() #Need to get username and password of the user to login
    
    ftpServer.cwd('~')
    ftpFiles = ftpServer.nlst()
    #Get list of files to check through
    for f in ftpfiles:
        #if f's modify date is within past three weeks:
            #Create a list of the file names to add to the email
            #Print the name and modify date of each file
        pass
    return() #Returns list of compromised files

def emailRecipient(senderEmail:str, recipientEmail:str, ctoBoolean):
    #function should email a "cute" email to the user and request the sender email password to send email
    #ctoBoolean will be true if -c was specified on start

def downloadFiles(fileList, fileLocation):
    #function should download files to a folder if this option was called if fileLocation is null or "" then should be downloaded to "Quarentine File" in home directory.

def ipValidation(input):
    #if input.matches(IP Address Regex)
        #return true
    pass
    #returns boolean value

def emailValidation(input):
    pass
    #return boolean value 

def get_parser():
    #initial argument parser to define basic info about command
    parser = ap.ArgumentParser(prog="NETWORK_MONITOR",usage="./Group3_Final.py SENDER_EMAIL RECIPIENT_EMAIL IP_ADDRESS [-d DIRECTORY_NAME] [-c]", add_help=True)

    #Below is mandatory arguments
    parser.add_argument("senderEmail", help="The email address of the sender.")
    parser.add_argument("recipientEmail", help="The email address of the recipient.")
    parser.add_argument("ipAddress", help="The IP address of the compromised machine to be examined.")

    # Below adds the arguments for the commands defining their basic info such as description and actions
    parser.add_argument("-d", "--download", action="store", dest="DirName",
                        help="If selected, the directory inputed will be used as the destination for downloading the smallest files. If not selected, downloads will be put in the current users home directory.")
    parser.add_argument("-c", "--cto", action="store_true", dest="booleanAttachCTO",
                        help="If this option is specified, the chief technology officer (CTO) will be added as a recipient of the email.")

    return parser

#below is main method to process the input
def main():
    mpsr = get_parser()

    #try except is created for error handling
    try:
        parserResult = mpsr.parse_args()

        if parserResult.senderEmail is not None:
            pass
        if parserResult.senderEmail is not None:
            pass
        if parserResult.booleanAttachCTO:
            pass

    #except method used to catch errors
    except Exception as ex:
        print(ex)

#below is configured so that script can be imported elsewhere and main wont run
if __name__ == "__main__":
    main()
