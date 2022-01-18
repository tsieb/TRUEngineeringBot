import discord
import os
from keep_alive import keep_alive
from replit import db
from events.on_member_join_handler import on_member_join_handler__
from events.on_member_remove_handler import on_member_remove_handler__
from events.on_message_handler import on_message_handler__
from events.on_raw_reaction_add_handler import on_raw_reaction_add_handler__
from events.on_raw_reaction_remove_handler import on_raw_reaction_remove_handler__
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


@client.event
async def on_ready():
  await log(client, 'We have logged in as {0.user}'.format(client), 1)

@client.event
async def on_member_remove(member):
  await on_member_remove_handler__(client, member)

@client.event
async def on_member_join(member):
  await on_member_join_handler__(client, member)

@client.event
async def on_raw_reaction_remove(payload):
  await on_raw_reaction_remove_handler__(client, payload)

@client.event
async def on_raw_reaction_add(payload):
  await on_raw_reaction_add_handler__(client, payload)

@client.event
async def on_message(message):
  await on_message_handler__(client, message)



print("Starting keep_alive script")
keep_alive()
print("Running Bot")
client.run(os.environ['Token'])
sendEmail(port = 465, server = "mail.sieb.net", sender = "TRUEBot@engclub.ca", receiver = "trenton@sieb.net", password = str(os.environ['mail_pass']), message = "The bot has died at {deathtime}.".format(deathtime = datetime.now()), reply = "", sender_nick = "TRUE Discord Bot", subject = "FATAL ERROR", username = str(os.environ['username']))
print("Bot is dead")