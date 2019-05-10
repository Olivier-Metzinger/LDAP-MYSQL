import logging
import variables
import os
import smtplib
from email.mime.text import MIMEText

def send_log_mail():
    fp = open('error_log.log', 'rb')
    msg = MIMEText(fp.read())
    fp.close()
    msg['Subject'] = variables.SUBJECT_mail
    msg['From'] = variables.FROM_mail
    msg['To'] = variables.TO_mail

    if (os.stat("error_log.log").st_size) > 0:
         mail = smtplib.SMTP('10.10.44.148')
         mail.sendmail(variables.FROM_mail, variables.TO_mail, msg.as_string())