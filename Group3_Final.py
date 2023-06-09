#!/usr/bin/python
import argparse as ap
import os
import smtplib
import ssl
import sys
import paramiko
import re
import getpass
from smtplib import SMTP_SSL
from ssl import create_default_context
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
#import modules

# function should return list of files that have been modified in last 3 weeks - also it should loop through them and print them out to console
def fileCheck(IP_ADDRESS: str) -> list[str]:
    #Variables for list of files, port number, and command for finding modified files.
    masterList = []
    port = 22
    command = 'find ~ -type f -not -path \'*/\.*\' -mtime -21 -printf "%TY-%Tm-%Td\\t%k\\t%p\\n" | sort -n -k 2 | cut -f 1,3-'
    #Obtains the username and password and adds them to the masterlist
    username = input("Enter the username of a user on the compromised machine: ")
    masterList.append(username)
    password = getpass.getpass("Enter the password of the compromised user: ")
    masterList.append(password)

    try:
        # Setup SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Try ssh connection, if it fails close it and print the error.
        try:
            ssh_client.connect(IP_ADDRESS, port, username=username, password=password)
        except:
            print("ERROR: Invalid Credentials")
            exit(999)
            ssh_client.close()
        #Setup ssh command
        stdin, stdout, stderr = ssh_client.exec_command(command)
        #Parse through command output and add the filenames to the masterlist
        for line in stdout.readlines():
            line = line.strip()
            masterList.append(line)
        #If no files were found, present error
        if len(masterList) < 3:
            print(
                "EXIT CODE: No compromised files found. There are no files that have been modified within the past 3 weeks.")
            sys.exit(0)
            ssh_client.close()

        ssh_client.close()
    except Exception as ex:
        print(ex)
    #Iterates through the command output and prints the mod date and file name
    counter = 0
    print("%-25s %10s" % ("Last Modified Date", "File Name"))
    print("-------------------------------------------")
    for line in masterList:
        counter += 1
        if counter > 2:
            print(line)
    print(" ")
    #Separates the modified date and filename in the masterlist
    counter = 0
    for item in masterList:
        if counter > 1:
            path = item.split("/", 1)
            masterList[counter] = "/" + path[1]
        else:
            masterList[counter] = item
        counter += 1
    return (masterList)


def emailSendOff(fileList, fileSource, senderEmail: str, recipientEmail: str, ctoBoolean, IP_ADDRESS):
    sendPass = getpass.getpass("Enter email sender password: ")
    #sendPass = "fgknwqfsbpzdpuyg"
    #sets up email variables
    if ctoBoolean:
        names = "Chief Technology Officer and Others"
    else:
        names = "All"
    if ctoBoolean:
        recipientEmail = recipientEmail + ", cit383.testmail@gmail.com"
    location = "/home/" + fileList[0]
    #Finds smallest file to attach it to the email
    skipCounter = 1
    allFiles = ""
    for x in fileList:
        if skipCounter > 2:
            allFiles = allFiles + "\t" + x + "\n"
        skipCounter += 1
    if fileSource == "":
        attachPath = os.path.expanduser("~") + "/COMPROMISED_FILE_" + (fileList[2].split("/"))[-1]
    else:
        attachPath = fileSource + "/COMPROMISED_FILE_" + (fileList[2].split("/"))[-1]
    #Begins email and sets it up with recipient, subject, and sender
    emailContent = MIMEMultipart("mixed")
    emailContent['Subject'] = "IMPORTANT - COMPROMISED USER"
    emailContent['From'] = senderEmail
    emailContent['To'] = recipientEmail
    #Writes email including CTO, files, etc.
    body = f"""
Hello {names},
    
It has been found that the user '{fileList[0]}' on host '{IP_ADDRESS}' was compromised! This was discovered as files within the directory '{location}' were found to have been modified within the past 3 weeks.

Relevant information to this breach:
    IP ADDRESS: {IP_ADDRESS}\n
    USER: {fileList[0]}\n
    PASSWORD: {fileList[1]}\n
    AMOUNT OF FILES: {len(fileList) - 2}
    
The following is a list of all compromised files: 
{allFiles}
    
Attached to this email is the smallest file found that was compromised.
    
Sincerely,
    
Script
"""
    #Completes email setup by attaching the body as text. Sends through port and server.
    emailBody = MIMEText(body, "plain")
    emailContent.attach(emailBody)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    filename = "COMPROMISED_FILE_" + (fileList[2].split("/"))[-1]
    #Attaches smallest affected file to the email
    try:
        with open(attachPath, "rb") as attachment:
            p = MIMEApplication(attachment.read(), _subtype=(fileList[2].split("."))[-1])
            p.add_header('Content-Disposition', f"attachment; filename={filename}")
            emailContent.attach(p)
    except Exception as ex:
        print(str(ex))

    msg_full = emailContent.as_string()
    context = ssl.create_default_context()
    #Sends the email and closes the server connection
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        try:
            server.login(senderEmail, sendPass)
        except:
            print("ERROR: Incorrect login credentials.")
            server.quit()
            exit(0)
        try:
            server.sendmail(senderEmail, recipientEmail, msg_full)
        except:
            print("ERROR: Unable to send email after signing in.")
            server.quit()
            exit(0)
        server.quit()
        print("Successfully sent email!")
#Downloads the smallest affected file to the quarantine folder.
def downloadFiles(fileList, fileLocation, host, port):
    try:
        # Below creates the sftp connection to the client
        sshPipe = paramiko.Transport(host, port)
        sshPipe.connect(username=fileList[0], password=fileList[1])

        sftp = paramiko.SFTPClient.from_transport(sshPipe)

        # if the remote path exists continue
        if sftp.stat(fileList[2]):
            newFileName = "/COMPROMISED_FILE_" + (fileList[2].split("/"))[-1]
            #If file location is "", create the variable for the path to the file with the users home file
            if fileLocation == "":
                localFile = os.path.expanduser("~") + newFileName
            else:
                localFile = fileLocation + newFileName

            try:
                sftp.get(fileList[2], localFile)
            except:
                print("ERROR: The file '" + fileList[2] + "' could not be downloaded.")
                sftp.close()
                exit(0)

            # once done copying sftp connection is closed and a message is printed regarding the action.
            sftp.close()
            print("File successfully downloaded")
        # if the remote path doesnt exist, print error and end gracefully
        else:
            print("Error: Issue finding file on client")
            sftp.close()
            exit(0)

    # if any uncaught errors occur, this will catch them and print the error code
    except Exception as ex:
        print(ex)

#Ensure that IP address is valid and return a boolean value
def ipValidation(input):
    regex = r"^(?!0\.0\.0\.0)(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

    if re.match(regex, input):
        return True
    else:
        return False

#Ensure the email address is valid and return a boolean value
def emailValidation(input):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.fullmatch(regex, input):
        return True
    else:
        return False


def get_parser():
    # initial argument parser to define basic info about command
    parser = ap.ArgumentParser(prog="NETWORK_MONITOR",
                               usage="./Group3_Final.py SENDER_EMAIL RECIPIENT_EMAIL IP_ADDRESS COMP_USER [-d DIRECTORY_NAME] [-c]",
                               add_help=True)

    # Below is mandatory arguments
    parser.add_argument("senderEmail", help="The email address of the sender.")
    parser.add_argument("recipientEmail", help="The email address of the recipient.")
    parser.add_argument("ipAddress", help="The IP address of the compromised machine to be examined.")

    # Below adds the arguments for the commands defining their basic info such as description and actions
    parser.add_argument("-d", "--download", action="store", dest="DirName",
                        help="If selected, the directory inputed will be used as the destination for downloading the smallest files. If not selected, downloads will be put in the current users home directory.")
    parser.add_argument("-c", "--cto", action="store_true", dest="booleanAttachCTO",
                        help="If this option is specified, the chief technology officer (CTO) will be added as a recipient of the email.")

    return parser


# below is main method to process the input
def main():
    downloadLocation = ""
    mpsr = get_parser()
    # try except is created for error handling
    try:
        parserResult = mpsr.parse_args()
        if emailValidation(parserResult.senderEmail):
            if emailValidation(parserResult.recipientEmail):
                if ipValidation(parserResult.ipAddress):
                    try:
                        if parserResult.DirName is not None:
                            if os.path.exists(parserResult.DirName):
                                if os.path.isdir(parserResult.DirName):
                                    downloadLocation = parserResult.DirName
                                else:
                                    print("ERROR: -d value is not a directory")
                                    exit(0)
                            else:
                                print("ERROR: Inputted -d path does not exist")
                                exit(0)
                        compFiles = fileCheck(parserResult.ipAddress)
                        downloadFiles(compFiles, downloadLocation, parserResult.ipAddress, 22)
                        emailSendOff(compFiles, downloadLocation, parserResult.senderEmail, parserResult.recipientEmail,
                                     parserResult.booleanAttachCTO, parserResult.ipAddress)

                    except Exception as ex:
                        print(ex)
                else:
                    print("ERROR: Invalid IP Address, must be between 0.0.0.0 and 255.255.255.255")
            else:
                print("ERROR: Invalid recipient email")
        else:
            print("ERROR: Invalid sender email")

    # except method used to catch errors
    except Exception as ex:
        print(ex)


# below is configured so that script can be imported elsewhere and main wont run
if __name__ == "__main__":
    main()
