#!/usr/bin/python3

import configparser
import subprocess
import smtplib
from email.mime.text import MIMEText

c = configparser.ConfigParser()
c.read("config.conf")

threshold = 80
partition = "/","/data"

From = c.get("smtp", "sender")
To = c.get("smtp", "recipient")

def report_via_email(data):
    msg = MIMEText("Server running out of disk space\n %s" % (data) )
    msg["Subject"] = "Low disk space warning"
    msg["From"] = From
    msg["To"] = To
    with smtplib.SMTP(c.get("smtp", "server"), c.get("smtp", "port")) as server:
        server.ehlo()
        server.sendmail(From, To ,msg.as_string())

def check_once():
    df = subprocess.Popen(["df","-h"], stdout=subprocess.PIPE)
    data = ""
    for line in df.stdout:
        splitline = line.decode().split()
        
        for p in partition:
            if splitline[5] == p:
                if int(splitline[4][:-1]) > threshold:
                    data += "Mount: %s\t\tUsed: %s\tTotal: %s\tRemain: %s\tDevice: %s\n" % (splitline[5], splitline[4], splitline[1], splitline[3], splitline[0])
    report_via_email(data)


check_once()