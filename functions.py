import discord
import os
from replit import db
import random
import smtplib, ssl

messages = db["messages"]

def getDefaultUser(id):
  return({"user_ID": id, "conv_state": 0, "purpose": None, "email": None, "react_msg_id": None, "verify_code": None, "attempts": 0})

def getUserFromDB(id):
  for i in db["users"]:
    if (i["user_ID"] == id):
      return((i, True))
  return((getDefaultUser(id), False))

def updateUserInDB(user):
  for i in db["users"]:
    if (user["user_ID"] == i["user_ID"]):
      i = user

def sendEmail(port = 465, server = "", sender = "", receiver = "", password = "", message = "", reply = "", sender_nick = "", subject = "", username = ""):
  if (username == ""):
    username = sender
  message = """\
From: {mail_from}
Reply-to: {reply}
To: {mail_to}
Subject: {subject}
      
{message}
""".format(mail_from = sender_nick + "<" + sender + ">", reply = reply, mail_to = receiver, subject = subject, message = message, )

  with smtplib.SMTP_SSL(server, port) as server:
      server.login(username, password)
      server.sendmail(sender, receiver, message)
  print("Sent email to:", receiver)

def sendVerification(user):
  print("attempting send")
  password = os.environ['mail_pass']
  username = os.environ['username']
  port = 465
  server = "mail.sieb.net"
  sender = "noreply@engclub.ca"
  receiver = user["email"]
  subject = "TRUE Verification Email"
  message = "Thanks for joining the TRUE Discord Server.\nYour validation code is:\t{code}\n\nIf you did not request this verification email, you can simply ignore it.".format(code = user["verify_code"])
  sendEmail(port = port, server = server, sender = sender, receiver = receiver, password = password, message = message, reply = "siebt19@mytru.ca", sender_nick = "TRUSU Engineering Club", subject = subject, username = username)
