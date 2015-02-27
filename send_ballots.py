import os
import random
import hashlib
import getpass
import smtplib
import binascii

from email.mime.text import MIMEText


subject = "LHCb vote #1"
msg_template = """Hello, 1,2, 1,2,3

test the west? Is this on?

Welcome to the LHCb election system. To cast your
vote go to:

{url}

When casting your vote enter your token:

"{token}"

(copy and paste it without the quotation marks)

We will not prevent you from spoiling your ballot
by voting multiple times or selecting the same
candidate multiple times so please pay attention
when casting your vote.

Once voting closes you will be sent a spreadsheet
and a list of all valid tokens. With this you
will be able to verify your vote and the
outcome of the election.

Thank you
"""
vote_url = "http://goo.gl/forms/HHLmMv8SH0"
salt = raw_input("Salt to make tokens unique: ")
sender = "thead@cern.ch"

lhcb_collaborators = ["betatim@gmail.com",
                  ]

token_fname = "valid_tokens.txt"
username = 'thead'
password = getpass.getpass("SMTP server password: ")

s = smtplib.SMTP('smtp.cern.ch', port=587)

valid_tokens = []

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
        valid_tokens.append(token + "\n")
        
        msg = MIMEText(msg_template.format(token=token,
                                           url=vote_url))
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = addr
        s.sendmail(sender, [addr], msg.as_string())

finally:
    s.quit()

print
print "List of valid tokens, needed for verifying results,"
print "was written in random order to: {token_fname}".format(token_fname=token_fname)

random.shuffle(valid_tokens)

out = open(token_fname, 'w')
out.writelines(valid_tokens)
out.close()
