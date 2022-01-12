import discord
import os
#import requests
#import json
from keep_alive import keep_alive
from replit import db

client = discord.Client()

if "users" not in db.keys():
  db["users"] = []

def getDefaultUser(id):
  return({"user_ID": id, "conv_state": 0, "purpose": 0, "email": ""})


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


98 - Respond: will review this message and get back to you.

99 - Canceled entry. Kick from server
'''
messages = {"welcome": "Welcome stand-in text"}
#User db format:
#{"user_ID": integer, "conv_state": integer, "purpose": integer, "email": ""},... {}]\

async def msg(context, user: discord.User, message):
    await user.send(message)

@client.event
async def on_member_join(member):
  saved = True
  for i in db["users"]:
    if (i["user_ID"] == member.id):
      saved = True
      data = i
      break
  if(saved == False):
    data = getDefaultUser(member.id)
    db["users"].append(data)
  if(data["conv_state"] == 0):
    await client.create_dm(member)
    await client.send_message(member.dm_channel, messages["welcome"])
  
async def on_message(message):
  saved = False

  if message.author == client.user:
    return
  if(message.author.dm_channel != None and message.author.dm_channel == message.channel):
    pass
  for i in db["users"]:
    if (i["user_ID"] == message.author.id):
      saved = True
      break
  if(saved == False):
    db["users"].append(getDefaultUser(message.author.id))
  
  # Select the appropriate user entry
  for user in db["users"]:
      if (user["user_ID"] == message.author.id):

      #COMMANDS

        # NEW CHARACTER COMMAND
        if msg.startswith("$new"):
          if (user["char_name"] != ""):
            user["conv_state"] = 2
            await message.channel.send("You already have a character stored. Would you like to overwrite? (y/n)")
            break
          else:
            user["conv_state"] = 1
            await message.channel.send("You have now initiated character creation.\nPlease type your character's name.")
            break

        # MOVE USER COMMAND
        elif message.content.startswith('$move'):
          channel = client.get_channel(891630860841918504)
          await message.author.move_to(channel)
          print("Moved " + message.author.name)
          break
        
        # USER DATA COMMAND
        elif message.content.startswith('$data'):
          await message.channel.send(user)
          break

        # PAUSE COMMAND
        elif message.content.startswith('$pause'):
          member = await client.fetch_user(int(os.environ['DM']))
          await member.send(str(message.author) + " (" + user["char_name"] + ") has requested a pause!")
          break
          
        
      #CONV_STATES

        #1 - Character name
        elif (user["conv_state"] == 1):
          user["char_name"] = msg
          user["conv_state"] = 3
          await message.channel.send("Hi, " + msg + ". Enter your character's modifiers for each stat.\n Enter them in one message in the order of STR DEX CON INT WIS CHA. (eg. -1 2 4 -3 2 2)")
          break
        
        #2 - Overwrite Request
        elif (user["conv_state"] == 2):
          try:
            if ((msg.lower() == "y") or (msg.lower() == "ye") or (msg.lower() == "yes")):
              user["conv_state"] = 1
              await message.channel.send("You have now initiated character creation.\nPlease type your character's name.")
              break
            elif (msg.lower() == "n" or msg.lower() == "no"):
              user["conv_state"] = 0
              await message.channel.send("Okay!")
              break
            else:
              await message.channel.send("Invalid entry. Please try again")
              break
          except:
            await message.channel.send("Invalid entry. Please try again")
            break

        #3 - Character stats
        elif (user["conv_state"] == 3):
          try:
            msg = msg.strip()
            msg = msg.split(" ", 5)
            for i in range(6):
              msg[i] = int(msg[i])
            user["stats"] = msg
            user["conv_state"] = 0
            await message.channel.send("Awesome, your character has been saved!")
            break
              
          except:
            await message.channel.send("Invalid entry. Please try again")
            break
        
       
  

#discord.on_member_update(before, after)
#discord.on_voice_state_update(member, before, after)

keep_alive()
client.run(os.environ['Token'])