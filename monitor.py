#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys, os
import requests
import getpass
import shutil
import json
import time
import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header

if len(sys.argv)<2:
    print('Usage: auto script')
    exit(1)

home = 'http://sumo.pia.jp/vacant/va01.jsp'
timeReg = '.*月.*日.*時'
isuReg = 'イス.席'
statusReg = 'alt="(.)" border='

DATE_MAX = 15
DATE_START = 8
DATE_OK = set([8, 9, 14, 15, 21, 22])

def sendmail(msg):
    sender = 'sb@mars'
    receivers = ['yrjie0@gmail.com']
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("sb", 'utf-8')
    message['To'] =  Header("sc", 'utf-8')

    subject = 'this is sb'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('mail sent')
    except smtplib.SMTPException:
        print('Error: send mail error')

def main():
    with requests.session() as s:
        ret01 = s.get(home)
        text = ret01.text

        lines = text.strip().split('\n')
        # print(len(lines))
        cnt = -1

        msg = ''
        hasSeat = False
        time = ''
        for line in lines:
            # print(line)
            if cnt>=0 and cnt<DATE_MAX:
                now = cnt + DATE_START
                if now in DATE_OK:
                    m = re.search(statusReg, line, re.DOTALL)
                    status = m.group(1) if m else 'null'
                    if status!='×' and status!='null':
                        hasSeat = True
                    msg += '%s : %s  ' % (str(now), status)
                cnt += 1;
                continue
            if cnt>=DATE_MAX:
                msg += '\n'
                cnt = -1
                continue
            m = re.search(timeReg, line, re.DOTALL)
            if m:
                # print(line)
                time = line
                msg += line+'\n\n'
                continue
            m = re.search(isuReg, line, re.DOTALL)
            if m:
                # print(line)
                cnt = 0
                msg += m.group(0)+'\n'
    if hasSeat:
        sendmail(msg)
    else:
        print('no ticket at ' + time)
        print(msg)

if __name__ == '__main__':
    main()

