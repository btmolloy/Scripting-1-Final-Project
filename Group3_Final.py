#!/usr/bin/python
import argparse as ap


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
