import os
import random
import hashlib
import getpass
import smtplib
import binascii

from email.mime.text import MIMEText


msg_template = """Hello,

your token is: "{token}"
(copy and paste it without the quotation marks)
go here to vote: {url}

Thank you
"""

sender = "thead@cern.ch"
vote_url = "http://goo.gl/forms/HHLmMv8SH0"
salt = os.environ.get("LHCB_SALT", "saltyfish")

lhcb_collaborators = ["betatim@gmail.com",
                      #"kevin.dungs@gmail.com",
                      "igor@babuschkin.de"
]

username = 'thead'
password = getpass.getpass("SMTP server password: ")

s = smtplib.SMTP('smtp.cern.ch', port=587)

try:
    # identify ourselves and prompt server for supported features
    s.ehlo()
    if s.has_extn("STARTTLS"):
        s.starttls()
        # have to re-identify after starting TLS
        s.ehlo()

    s.login(username, password)

    for addr in lhcb_collaborators:
        dk = hashlib.pbkdf2_hmac('sha256', addr, salt, 100000)
        token = binascii.hexlify(dk)
        
        msg = MIMEText(msg_template.format(token=token,
                                           url=vote_url))
        msg['Subject'] = 'Please vote #1'
        msg['From'] = sender
        msg['To'] = addr
        s.sendmail(sender, [addr], msg.as_string())

finally:
    s.quit()
