import discord
import os
from keep_alive import keep_alive
from replit import db
import random
from functions import *
from datetime import datetime

# TODO:
# verify command to restart
# make welcome message more robust/simplify ifelse spam
# after verification - free change state
# slash commands
# move each event to seperate file

# BUGS:


# Define messages
messages = {"welcome": "Welcome to the TRU Engineering Discord server.\nPlease use the reactions below to define your reason for joining the server.\n1 - Engineering Student\n2 - TRUSU Engineering Club\n3 - Engineering Student and Club\n4 - Neither an engineering student nor a club member\n5 - TRU professor\nStop will halt all further messages\n*At any point you can type `restart` to begin the process again.*", "welcome_reactions": ["\U00000031\U0000fe0f\U000020e3", "\U00000032\U0000fe0f\U000020e3", "\U00000033\U0000fe0f\U000020e3", "\U00000034\U0000fe0f\U000020e3", "\U00000035\U0000fe0f\U000020e3", "🛑"] , "email" : "Please type your TRU email. It must end with `@mytru.ca` or `@tru.ca`.","verify": "A Verification emaill has been sent to you. Please enter the code provided below.\n*Enter `resend` to resend the email to the same address\nEnter `change` to enter a new email address*", "complete": "Thanks for verifying your account! You now have access to the server. Please read the rules before chatting. If you ever decide to leave the server, all your data will be deleted and you will need to re-verify. All the code for the bot can be viewed on GitHub", "invalid_email": "The email you entered is invalid", "invalid_code": "The code you entered is wrong", "manual": "Why would you like to join the TRU Engineering Discord server?\nYour reply will be sent directly to the admin for manual verification.", "manual_response": "You will be notified within 48 hours of the result.", "limit_reached":"You have entered the maximum number of attempts. If you still wish to gain access to the server, DM the admin."}
db["messages"] = messages

roles = {"club": 931759411641331752, "student": 887072932604575796, "unverified": 932086744776605729}
db["roles"] = roles


print("Starting...")
# Initialize client
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

async def log(message, channel):
  if channel == 0:
    log0 = await client.fetch_channel(932902698926374943)
    await log0.send(message)
  else:
    log0 = await client.fetch_channel(932902698926374943)
    log1 = await client.fetch_channel(750519246269972490)
    await log0.send(message)
    await log1.send(message)
  print(message)


async def add_role(user_id, role_id):
  guild = client.get_guild(623986499477700652)
  member = guild.get_member(user_id)
  role = guild.get_role(role_id)
  await member.add_roles(role)

async def remove_role(user_id, role_id):
  guild = client.get_guild(623986499477700652)
  member = guild.get_member(user_id)
  role = guild.get_role(role_id)
  await member.remove_roles(role)
  

@client.event
async def on_ready():
  await log('We have logged in as {0.user}'.format(client), 1)



@client.event
async def on_member_remove(member):
  delete_user(id = member.id)
  await log('{0.display_name} has left the server'.format(member), 1)



@client.event
async def on_member_join(member):
  if (member == client.user):
    return
  await initial_message(client, member)
  await log('{0.display_name} has joined the server'.format(member), 1)



@client.event
async def on_raw_reaction_remove(payload):
  if (payload.user_id == client.user.id):
    return
  try:
    await log('{0.member.display_name} has removed reaction {0.emoji} in {0.channel_id}'.format(payload), 0)
  except:
    await log('{0.user_id} has removed reaction {0.emoji} in {0.channel_id}'.format(payload), 0)
  if (payload.message_id == 932827444933718088):
    await add_role(payload.user_id, roles["club"])
    await log('{0.user_id} has removed the club  role'.format(payload), 0)



@client.event
async def on_raw_reaction_add(payload):
  if (payload.user_id == client.user.id):
    return
  try:
    await log('{0.member.display_name} has reacted with {0.emoji} in {0.channel_id}'.format(payload), 0)
  except:
    await log('{0.user_id} has reacted with {0.emoji} in {0.channel_id}'.format(payload), 0)

  if (payload.message_id == 932827444933718088):
    await add_role(payload.user_id, roles["club"])
    await log('{0.user_id} has been given the club role'.format(payload), 0)
  if(is_new(payload.user_id)):
    #TODO handle better
    return
  user = get_user(payload.user_id)
  
  if (payload.message_id == user["react_msg_id"]):
    if (user["conv_state"] == 0):
      if ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x00000031', '0x0000fe0f', '0x000020e3']):
        user["purpose"] = 1
      elif ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x00000032', '0x0000fe0f', '0x000020e3']):
        user["purpose"] = 2
      elif ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x00000033', '0x0000fe0f', '0x000020e3']):
        user["purpose"] = 3
      elif ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x00000034', '0x0000fe0f', '0x000020e3']):
        user["purpose"] = 4
      elif ([f"0x{ord(c):08x}" for c in payload.emoji.name] == ['0x0001f6d1']):
        user["purpose"] = None
        user["conv_state"] = 0
      if (user["purpose"] == 1 or user["purpose"] == 2 or user["purpose"] == 3):
        user_obj = client.get_user(payload.user_id)
        await log_print(client, "Sending email message to" + user_obj.display_name)
        await user_obj.send(messages["email"])
        user["conv_state"] = 2
      else:
        await log_print(client, "Sending manual verification message to" + user_obj.display_name)
        await user_obj.send(messages["manual"])
        user["conv_state"] = 4
  print("reaction")
  await update_user(user, client)


# TODO if conv = 0 and msgid = None send welcome
@client.event
async def on_message(message):
  
  if message.author == client.user:
    return
  if message.author.bot:
    return
  print("Triggered: " + message.author.display_name)
  if(is_admin(message.author.id)):
    cmd = message.content.split()

  # ---- ADMIN COMMANDS ----
    # --- ADD ---
    if(message.content.startswith("$add")):
      initial_message(client, member = None, id = cmd[1])
    
    # --- DELETE ---
    elif(message.content.startswith("$delete")):
      delete_user(id = cmd[1])
      await message.author.send("User deleted from database")
    
    # --- RESET ---
    elif(message.content.startswith("$delete")):
      user = get_user(cmd[1])
      user["conv_state"] = 0
      update_user(user)
      initial_message(client, member = None, id = cmd[1])
    
    # --- EMAIL ---
    elif(message.content.startswith("$email")):
      await message.author.send("""sender = \"\", receiver = \"\", message = \"\", sender_nick = \"\", subject = \"\",reply = \"\"""")
    elif(message.content.startswith("$send")):
      send_admin_mail(sender = cmd[1], receiver = cmd[2], message = cmd[3], sender_nick = cmd[4], subject = cmd[5], reply = cmd[6])

    # --- MSG ---
    elif(message.content.startswith("$msg")):
      try:
        msg = ""
        for i in cmd[2:]:
          msg += i
        target = await client.fetch_user(cmd[1])
        await target.send(msg)
      except Exception as e:
        print(e)
        await message.author.send("Invalid target")


  print(message.author.display_name, "messaged", message.content)
  if (is_new(message.author.id)):
    add_user(message.author.id)
    await initial_message(client, message.author)
  user = get_user(message.author.id)
  if (message.author.dm_channel == message.channel):
    
  # ---- USER DM COMMANDS ----
    # --- RESTART ---
    if(message.content.startswith("restart")):
      user["conv_state"] = 0
      user["react_msg_id"] = None

    # --- RESEND ---
    elif (message.content.startswith("resend") and user["conv_state"] == 3):
      sendVerification(user)

    # --- CHANGE ---
    elif (message.content.startswith("change") and user["conv_state"] == 3):
      await log_print(client, "Sending email message to " + message.author.display_name)
      await message.author.send(messages["email"])
      user["conv_state"] = 2

    #TODO move back to function
    if(user["conv_state"] == 0 and user["react_msg_id"] == None):
      await initial_message(client, message.author)
      
    elif (user["conv_state"] == 2):
      if (message.content.strip().find("@mytru.ca", 1) != -1 or message.content.strip().find("@tru.ca", 1) != -1):
        user["email"] = message.content.strip("")
        user["verify_code"] = random.randint(10000, 99999)
        user["conv_state"] = 3
        sendVerification(user)
        await log_print(client, "Sending verify message to " + message.author.display_name)
        await message.author.send(messages["verify"])
      else:
        await message.author.send(messages["invalid_email"])

    elif (user["conv_state"] == 3):
      try:
        if (int(message.content.strip()) == user["verify_code"]):
          await log_print(client, "Sending complete message to " + message.author.display_name)
          await message.author.send(messages["complete"])
          user["conv_state"] = 96
        else:
          user["attempts"] += 1
          await log_print(client, "User has made " + str(user["attempts"]) + "attempts")
          await message.author.send(messages["invalid_code"])
      except: 
        pass
      if (user["attempts"] >= 10):
        user["conv_state"] = 90
        await message.author.send(messages["limit_reached"])
  print("msg")
  await update_user(user, client)


print("Starting keep_alive script")
keep_alive()
print("Running Bot")
client.run(os.environ['Token'])
sendEmail(port = 465, server = "mail.sieb.net", sender = "TRUEBot@engclub.ca", receiver = "trenton@sieb.net", password = str(os.environ['mail_pass']), message = "The bot has died at {deathtime}.".format(deathtime = datetime.now()), reply = "", sender_nick = "TRUE Discord Bot", subject = "FATAL ERROR", username = str(os.environ['username']))
print("Bot is dead")