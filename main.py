import discord
import os
#import requests
#import json
from keep_alive import keep_alive
from replit import db
import random

client = discord.Client()

if "users" not in db.keys():
  db["users"] = []

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

def sendEmail(user):
  pass

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

'''
Conversation state:
0 - Initiate conversation on join.
  Welcome to the TRUEngineering Server. 
  Are you joining as an engineering student, looking for the engineering program, both or neither?
  store answer with user
    if 1, 2, or 3 go to 1. If 4 ask for reason of joining and go to 98
  
1 - Request email
  If valid email given. Generate code. Send email. go to 2

2 - Check entered code against stored user code
  If correct code. give user active role based on original request. go to 5
  otherwise ask to renter code, email or cancel. 
  if code go to 2 if email go to 1 if cancel go to 99

96 - Verified

97 - Pause interaction

98 - Respond: will review this message and get back to you.

99 - Canceled entry. Kick from server
'''
messages = {"welcome": "Welcome stand-in text", "welcome_reactions": [":one:", ":two:", ":three:", ":four:", ":stop_sign:"], "email": "sample email request text","verify": "sample verify text", "complete": "default complete text"}

async def msg(context, user: discord.User, message):
    await user.send(message)

@client.event
async def on_member_join(member):
  print("triggered - join")
  user = getUserFromDB(member.id)
  if (member == client.user):
    pass
  elif (not user[1]):
    db["users"].append(user[0])
  elif(user[0]["conv_state"] == 0):
    await client.create_dm(member)
    msg = await client.send_message(member.dm_channel, messages["welcome"])
    for emoji in messages["welcome_reactions"]:
      await client.add_reaction(msg, emoji)

@client.event
async def on_raw_reaction_add(payload):
  print("triggered - react")
  if (payload.event_type == "REACTION_ADD"):
    pass
  elif (payload.member == client.user):
    pass
  elif (payload.message_id == getUserFromDB(payload.member.id)[0]["react_msg_id"]):
    data = getUserFromDB(payload.member.id)[0]
    if (data["conv_state"] == 0):
      if (payload.emoji.name == ":one:"):
        data["purpose"] = 1
      elif (payload.emoji.name == ":two:"):
        data["purpose"] = 2
      elif (payload.emoji.name == ":three:"):
        data["purpose"] = 3
      elif (payload.emoji.name == ":four:"):
        data["purpose"] = 4
      elif (payload.emoji.name == ":stop_sign:"):
        data["purpose"] = 0
        data["conv_state"] = 97
    if (data["purpose"] == 1 or data["purpose"] == 2 or data["purpose"] == 3):
      await client.send_message(payload.member.dm_channel, messages["email"])
      data["conv_state"] = 2
  updateUserInDB(data)

@client.event
async def on_message(message):
  print("triggered - message")
  if message.author == client.user:
    return
  user = getUserFromDB(message.author.id)
  if (not user[1]):
    db["users"].append(user[0])
  if (message.author.dm_channel == message.channel):
    if (user[0]["conv_state"] == 2):
      if (message.content.strip().find("@mytru.ca", 1) != -1 or message.content.strip().find("@tru.ca", 1) != -1):
        user["email"] = message.content.strip()
        user["verify_code"] = random.randint(10000, 99999)
        user["conv_state"] = 3
        sendEmail(user)
        await client.send_message(message.author.dm_channel, messages["verify"])
    elif (user[0]["conv_state"] == 3):
      try:
        if (message.content.strip() == user[0]["verify_code"]):
          await client.send_message(message.author.dm_channel, messages["complete"])
          user[0]["conv_state"] = 96
      except:
        if (message.content == "resend"):
          await client.send_message(message.author.dm_channel, messages["email"])
          user["conv_state"] = 2
      else:
        user["attempts"] += 1
  updateUserInDB(user[0])

  

#discord.on_member_update(before, after)
#discord.on_voice_state_update(member, before, after)

keep_alive()
client.run(os.environ['Token'])