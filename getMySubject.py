import requests
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configs

# If you are running this script , please enable third party app access in your(sender's) Gmail account 
# run it in background :  nohup python3 -u getMySubject.py > output.log &
# Kill it :  pkill -f getMySubject.py

def sendmail():

    print("--Initiate Email Session--")

    # sender emailId configured in configs.py
    sender_email = configs.username
    
    receiver_email=[]
    
    # GmailID of receiver who wnats to receive the notification
    receiver_email.append('GMAIID')
    
    # Sender EmailID password configured in configs.py
    password = configs.password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Web-Development Subject available"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    data = 'Check Availability : https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=202220&s_crn=&s_subj=CSCI&s_numb=&n=41&s_district=100 \n \n Register COurse : https://register.dal.ca/StudentRegistrationSsb_PROD/ssb/classRegistration/classRegistration'
    part1 = MIMEText(data, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    # sleep for 15 mins once email has been triggered to eliminate email bombarding
    time.sleep(900)
    receiver_email.clear()

def getdata():
    try:
        r = requests.get("https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=202220&s_crn=&s_subj=CSCI&s_numb=&n=41&s_district=100", stream=True)
        SubjectCode = ''
        SubjectSeats = ''
        seatList = []
        dictSubject = ''
        subjectDictionary = {}
        for line in r.iter_lines():
            s = line.decode("utf-8")
            if s.startswith('<b>CSCI') :
                SubjectCode = s[3:12]
            if  s.startswith('<font color='):
                seatList.append(s)

        print('Got the data ')

        # length of last font color in array , as last font tag is related to Webdevelopment subject
        # length of last element in array -> <font color=darkred>FULL</font> is 31
        # if the length of last element changes a mail will be triggered to mailIds present in receiver_email array
        if(len(seatList[len(seatList)-1]) < 31):
            sendmail()
    except:
        print(Exception)
        time.sleep(60)
        print("Sleeping for 60 secs")

if __name__ == '__main__':
    while True:
        print('starting')
        getdata()
        #run this script every 15 secs
        time.sleep(15)
