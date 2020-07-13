#!/opt/local/bin/python3
# -*- coding: utf-8 -*-

import os
import requests
import bs4
import smtplib
from email.mime.text import MIMEText
from urllib.parse import urlencode
import time

def getContent():
    url = "https://www.asiapacificex.com/?p=trading_information"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache - Control": "max - age = 0",
        "Connection": "keep - alive",
        "Cookie": "PHPSESSID=0a61gj1o2ud8bd73a5lpjqtm4s; LANG=cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    content = ""
    panel = soup.find(id='collapse1')
    tables = panel.findAll('table')
    for table in tables:
        for line in table.findAll('tr'):
            for l in line.findAll('td'):
                cell = l.getText().strip().replace("\n", "") + "|"
                content += cell
            content += "\r\n\r\n"
        content += "\r\n\r\n"
    return content

def sendemail(content):
    smtp_server = "smtp.163.com"
    smtp_port = 25
    smtp_user = "jsjlzhq@163.com"
    smtp_password = "lzq123"
    recipients = "lizhiqin@xinhua.org"
    msg = MIMEText(content)
    msg["Subject"] = "Apex节假日变更"
    msg["From"] = smtp_user
    msg["To"] = recipients
    email = smtplib.SMTP(smtp_server, int(smtp_port))
    email.login(user=smtp_user, password=smtp_password)
    email.sendmail(smtp_user, recipients, msg.as_string())
    email.close()

def getNewFilename(filename):
    return filename + "_" + time.strftime("%Y%m%d", time.localtime())

def sendToWechat(content):
    subject="Apex节假日变更"
    url = "https://sc.ftqq.com/SCU69199T10cf07dff058d8fc834c59e83834c1f05df86cecdf649.send"
    data={
    'text': subject,
    'desp': content
    }
    requests.get(url, urlencode(data))

if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(__file__))
    content = getContent()
    filename = path + "/apexholiday"
    if os.path.exists(filename):
        fp = open(filename, "r")
        oldContent = fp.read()
        fp.close()
        if content == oldContent:
#            print("apex holiday not change")
            exit()
        else:
            os.rename(filename, getNewFilename(filename))

    print("apex holiday changed")
    fp = open(filename, "w")
    fp.write(content)
    #sendemail(content)
    sendToWechat(content)
    fp.close()

