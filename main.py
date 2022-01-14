import discord
import os
#import requests
#import json
from keep_alive import keep_alive
from replit import db
import random
from functions import getDefaultUser, getUserFromDB, updateUserInDB, sendVerification

# Initialize client
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

# Define messages

reset = True
# Ensure Users are defined in the database
if ("users" not in db.keys() or reset == True):
  db["users"] = []

# Define messages
#if "messages" not in db.keys():
if True:
  db["messages"] = {"welcome": "Welcome stand-in text", "welcome_reactions": ["\U00000031\U0000fe0f\U000020e3", "2️⃣", "3️⃣", "4️⃣", "🛑"] , "email" : "sample email request text","verify": "sample verify text", "complete": "default complete text"}
messages = db["messages"]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
  print("triggered - join by ", member.name)
  user = getUserFromDB(member.id)
  if (member == client.user):
    pass
  elif (not user[1]):
    db["users"].append(user[0])
  user[0]["conv_state"] = 0
  if(user[0]["conv_state"] == 0):
    print("Sending message to", member.display_name)

    msg = await member.send(db["messages"]["welcome"])
    user[0]["react_msg_id"] = msg.id
    for emoji in db["messages"]["welcome_reactions"]:
      await msg.add_reaction(emoji)
  updateUserInDB(user[0])

@client.event
async def on_raw_reaction_add(payload):
  print("triggered - react from", payload.user_id)
  if (payload.event_type != "REACTION_ADD"):
    pass
  elif (payload.user_id == client.user.id):
    pass
  elif (payload.message_id == getUserFromDB(payload.user_id)[0]["react_msg_id"]):
    data = getUserFromDB(payload.user_id)[0]
    if (data["conv_state"] == 0):
      if ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x00000031', '0x0000fe0f', '0x000020e3']):

        data["purpose"] = 1
      elif ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x00000032', '0x0000fe0f', '0x000020e3']):

        data["purpose"] = 2
      elif ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x00000033', '0x0000fe0f', '0x000020e3']):

        data["purpose"] = 3
      elif ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x00000034', '0x0000fe0f', '0x000020e3']):

        data["purpose"] = 4
      elif ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x0001f6d1']):

        data["purpose"] = 0
        data["conv_state"] = 0
    if (data["purpose"] == 1 or data["purpose"] == 2 or data["purpose"] == 3):
      await client.get_user(payload.user_id).send(messages["email"])
      data["conv_state"] = 2
    updateUserInDB(data)


@client.event
async def on_message(message):
  print("triggered - message from", message.author.name)
  if message.author == client.user:
    return
  user = getUserFromDB(message.author.id)
  if (not user[1]):
    print("new")
    db["users"].append(user[0])
  if (message.author.dm_channel == message.channel):
    if(user[0]["conv_state"] == 0):
      print("Sending message to", message.author.display_name)
      msg = await message.author.send(db["messages"]["welcome"])
      user[0]["react_msg_id"] = msg.id
      for emoji in db["messages"]["welcome_reactions"]:
        await msg.add_reaction(emoji)
    elif (user[0]["conv_state"] == 2):

      if (message.content.strip().find("@mytru.ca", 1) != -1 or message.content.strip().find("@tru.ca", 1) != -1):
        user[0]["email"] = message.content.strip("")
        user[0]["verify_code"] = random.randint(10000, 99999)
        user[0]["conv_state"] = 3
        sendVerification(user[0])
        await message.author.send(messages["verify"])
    elif (user[0]["conv_state"] == 3):
      if (message.content.startswith("resend")):
        sendVerification(user[0])
      elif (message.content.startswith("change")):
        await message.author.send(messages["email"])
        user[0]["conv_state"] = 2
      try:
        print(type(user[0]["verify_code"]))
        print(user[0]["verify_code"])
        print(type(int(message.content.strip())))
        print(int(message.content.strip()))
        if (int(message.content.strip()) == user[0]["verify_code"]):
          await message.author.send(messages["complete"])
          user[0]["conv_state"] = 96
      except Exception as e: 
        print(e)
      else:
        user[0]["attempts"] += 1
  updateUserInDB(user[0])

  

#discord.on_member_update(before, after)
#discord.on_voice_state_update(member, before, after)
print("Starting keep_alive script")
keep_alive()
print("Running Bot")
client.run(os.environ['Token'])
print("Bot is dead")