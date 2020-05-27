# @Author: Anthony Walker <walkanth>
# @Date:   2020-02-28T10:34:13-08:00
# @Email:  dev.sokato@gmail.com
# @Last modified by:   walkanth
# @Last modified time: 2020-02-28T11:21:55-08:00



#Programmer: Anthony Walker

from collections.abc import Iterable
import smtplib, ssl, argparse, os, sys, subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import signal

class functionTimer:
    """This class is the function timer."""
    def __init__(self, seconds=1, error_message='Your function has timed out.'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)

class ENotiPy(object):
    """Use this class to execute a function and notify via email when it has completed."""
    def __init__(self,rank=0,timeout=None):
        """Initializer."""
        self.timeout = timeout*60 if isinstance(timeout,type(1.0)) or isinstance(timeout,type(1)) else None
        try:
            self.smtp =os.environ['ENOTIPY_SMTP']
            self.port = int(os.environ['ENOTIPY_PORT'])
            self.email = self.receiver = os.environ['ENOTIPY_EMAIL']
        except Exception as e:
            print("""Error: Environment variables not properly set. Check the README for information on how to set this.""")
            sys.exit()
        self.server = smtplib.SMTP(self.smtp, self.port)
        self.rank = rank
        self.sm = "Congratulations, your code ran to completion.\n"
        self.subject = "Code Completion."

    def prepareMessage(self):
        """Use this function to prepare success or failure message, send, and receiver."""
        self.success = MIMEMultipart()
        self.success['From'] = self.email
        self.success['To'] = self.receiver
        self.success['Subject'] = self.subject

    def send(self):
        """This is the server login function."""
        self.server.connect(self.smtp,self.port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.email, os.environ['ENOTIPY_KEY'])
        self.server.sendmail(self.email,self.receiver,self.success.as_string())
        self.server.quit()

    def sendIt(self):
        """Use this function to attempt to send the mail"""
        try:
            self.prepareMessage()
            self.sm += "\n-ENotiPy\n"
            ts = MIMEText(self.sm)
            self.success.attach(ts)
            self.send()
        except Exception as e:
            print(e)
            print("""If you received a Username and Password error for gmail accounts,
            login to your account and visit https://support.google.com/accounts/answer/6010255 and setup an app password for ENotipy.
            Users of email services may have an option similar to this.""")

    def run(self,fcn,*args,**kwargs):
        """Call run to execute the given function and arguments."""
        self.fcn = fcn
        if self.rank == 0:
            try:
                #Executing main rank with or without timeout
                if self.timeout is None:
                    self.rets = self.fcn(*args,**kwargs)
                else:
                    with functionTimer(seconds=self.timeout):
                        self.rets = self.fcn(*args,**kwargs)
                #Adding returns to success message
                if isinstance(self.rets,Iterable):
                    self.sm+="\nReturns:\n"
                    for i,arg in enumerate(self.rets):
                        self.sm += str(arg)+"\n"
                elif self.rets is not None:
                    self.sm+="\nReturns:\n"
                    self.sm += str(self.rets)
            #Catching any erros
            except Exception as e:
                self.subject = "Oops, something went wrong."
                self.sm = "Code execution failure:\n"+str(e)
            self.sendIt()
        else:
            if self.timeout is None:
                self.rets = self.fcn(*args,**kwargs)
            else:
                with functionTimer(seconds=self.timeout):
                    self.rets = self.fcn(*args,**kwargs)

    def runCommand(self,command):
        """Use this function to execute the commandline argument."""
        if self.rank == 0:
            try:
                process = subprocess.run(command,timeout=self.timeout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if process.returncode != 0:
                    raise Exception("Command failed with: "+str(process.stderr))
            except Exception as e:
                self.subject = "Oops, something went wrong."
                self.sm = "Code execution failure:\n"+str(e)
            self.sendIt()

def str2bool(v):
    """This funciton converts strings to booleans."""
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected as string.')

def requestEnvSetup():
    """Use this function to set env variables before execution."""
    print("ENotipy environment setup requested.\n")
    print("If you are unsure of a requested setup argument check the README.\n")
    os.environ['ENOTIPY_EMAIL'] = input("Enter email address: ")
    os.environ['ENOTIPY_KEY'] = input("Enter password: ")
    os.environ["ENOTIPY_SMTP"] = input("Enter SMTP server: ")
    os.environ["ENOTIPY_PORT"] = input("Enter SMTP port: ")

def infoFileEnvSetup(infoFile):
    """Use this function to export the appropriate variables from INFO file."""
    with open(infoFile,'r') as f:
        lns = [line for line in f]
        lns = lns[1:5]
        lns = [line.split("\"")[1] for line in lns]
        os.environ['ENOTIPY_EMAIL'] = lns[0]
        os.environ['ENOTIPY_KEY'] = lns[1]
        os.environ["ENOTIPY_SMTP"] = lns[2]
        os.environ["ENOTIPY_PORT"] = lns[3]

def lineRun():
    """Use this function to run from the commandline."""
    parser = argparse.ArgumentParser(description="""This is the commandline interface for
    ENotipy. An open source notification software that wraps your code and sends an email notification
    when the code has either completed or terminated due to an error.
    """)
    parser.add_argument("command", nargs='?',default=None)
    parser.add_argument("-i","--info",default=None,type=str,help="""An info file can be completed similar to the SAMPLE_INFO file provided and passed with this argument.
    Alternatively, it can be sourced or the request option can be specified""")
    parser.add_argument("-r","--request",default=False,type=str2bool,help="""Set this argument to true to request environment setup at runtime.""")
    parser.add_argument('-t','--timeout',default=None,type=float,help="""If specified this will kill the operation after the specified amount of time in minutes.""")
    parser.add_argument('-g',"--generate",action='store_true',help="This option can be specified to generate a new SAMPLE_INFO if there is not one.")
    args = parser.parse_args()
    #Throw error if command isn't provided
    if args.command is None and not args.generate:
        parser.error("a command must be specified unless using a different ENotipy functionality.")

    if args.generate:
        print('Generating SAMPLE_INFO script')
        with open("SAMPLE_INFO","w") as f:
            f.write("#!/usr/bin/env bash\n")
            f.write("export ENOTIPY_EMAIL=\"dev.notipy@gmail.com\"\n")
            f.write("export ENOTIPY_KEY=\"SuperSecretPassword\"\n")
            f.write("export ENOTIPY_SMTP=\"smtp.gmail.com\"\n")
            f.write("export ENOTIPY_PORT=\"587\"")
        f.close()
    else:
        #Adjust timeout to seconds
        if args.request:
            requestEnvSetup()
        elif args.info is not None:
            infoFileEnvSetup(args.info)
        #Splitting command for process
        splitCommand = args.command.split(" ")
        #Execute command
        notifier = ENotiPy(timeout=args.timeout)
        notifier.runCommand(splitCommand)
