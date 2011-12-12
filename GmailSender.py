#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gmail SMTP script by joon
# Snippets from the following codes were used:
#  http://www.go4expert.com/forums/showthread.php?t=7567
#  http://docs.python.org/library/email-examples.html?highlight=sendmail
#  http://djkaos.wordpress.com/2009/04/08/python-gmail-smtp-send-email-script/

import smtplib
from email.mime.text import MIMEText

class GmailSender:
    def __init__(self, smtpuser, smtppass):
        smtpserver = 'smtp.gmail.com'

        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.ehlo()
        session.starttls()
        session.ehlo()

        session.login(smtpuser, smtppass)

        self.session = session
        self.sender = smtpuser

    def sendMail(self, recipients, subject, msg):
        msg = MIMEText(msg)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipients

        smtpresult = self.session.sendmail(self.sender, [recipients], msg.as_string())

        if smtpresult:
          errstr = ""
          for recip in smtpresult.keys():
              errstr = """Could not delivery mail to: %s

        Server said: %s
        %s

        %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
          raise smtplib.SMTPException, errstr

        #self.session.close()


if __name__ == "__main__":
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('config.ini')

    gmail = GmailSender(config.get('google', 'user'), config.get('google', 'pw'))
    gmail.sendMail('abc@abc.net', 'This is title of msg', 'Body of msg')




