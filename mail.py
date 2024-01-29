#Libraries
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import RPi.GPIO as GPIO
import time
import os


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)


 
#set GPIO direction (IN / OUT)
GPIO.setup(15, GPIO.IN)


def email():
    fromaddr = "alina.jones.037@gmail.com"
    toaddr = "mdtobibulislamthoha@gmail.com"
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "He is in trouble"
     
    body = "I am in trouble. Please help me."
     
    msg.attach(MIMEText(body, 'plain'))
     
    #filename = "NAME OF THE FILE WITH ITS EXTENSION"
    #attachment = open("PATH OF THE FILE", "rb")
     
    #part = MIMEBase('application', 'octet-stream')
    #part.set_payload((attachment).read())
    #encoders.encode_base64(part)
    #part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    #msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "alina420")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()



if __name__ == '__main__':
    try:
        while True:

            if GPIO.input(15):
                print ("Sending mail")
                email()

                
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
