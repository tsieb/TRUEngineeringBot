import discord
import os
from replit import db
import smtplib, ssl

messages = db["messages"]

async def initial_message(client, member = None, id = None):
  if(id):
    member = client.fetch_user(id)
  log_print(client, "Sending welcome message to " + member.display_name)
  user = add_user(member.id)
  msg = await member.send(db["messages"]["welcome"])
  for emoji in db["messages"]["welcome_reactions"]:
    await msg.add_reaction(emoji)
  user["react_msg_id"] = msg.id
  await update_user(user, client)


def is_admin(id):
  if(int(id) == int(os.environ['admin'])):
    return True
  return False

async def dm_print(client, message):
  print(message)
  id = os.environ['admin']
  admin = await client.fetch_user(id)
  await admin.send(message)
  await log_print(client, message)


async def log_print(client, message):
  id = os.environ['channel']
  channel = await client.fetch_channel(id)
  await channel.send(message)

def is_new(id):
  if str(id) in db:
    return False
  return True

def add_user(id):
  if str(id) in db:
      print("User already exists")
  else:
      db[str(id)] = getDefaultUser(id)
  return(db[str(id)])

def get_user(id):
  return db.get(str(id))

async def update_user(user, client):
  db[str(user["user_id"])] = user
  guild = client.get_guild(623986499477700652)
  member = guild.get_member(user["user_id"])
  engclub = guild.get_role(931759411641331752)
  eng = guild.get_role(887072932604575796)
  unv = guild.get_role(932086744776605729)
  if (user["conv_state"] == 96):
    await member.remove_roles(unv)
    if (user["purpose"] == 1):
      await member.add_roles(eng)
    elif (user["purpose"] == 2):
      await member.add_roles(engclub)
    elif (user["purpose"] == 3):
      await member.add_roles(eng)
      await member.add_roles(engclub)
  else:
    await member.add_roles(unv)
  


def delete_user(user = None, id = None):
  if user != None:
    id = str(user["user_id"])
    del db[id]
  elif id != None:
    del db[str(id)]
  else:
    print("Unable to find user")



def getDefaultUser(id):
  return({"user_id": id, "conv_state": 0, "purpose": None, "email": None, "react_msg_id": None, "verify_code": None, "attempts": 0})

def send_admin_mail(sender = "", receiver = "", message = "", sender_nick = "", subject = "",reply = ""):
  sendEmail(port = 465, server = "mail.sieb.net", sender = sender, receiver = receiver, password = os.environ['mail_pass'], message = message, reply = reply, sender_nick = sender_nick, subject = subject, username = os.environ['username'])

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



  