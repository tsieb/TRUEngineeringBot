from events.on_raw_reaction_remove_handler import on_raw_reaction_remove_handler__
from events.on_raw_reaction_add_handler import on_raw_reaction_add_handler__
from events.on_member_remove_handler import on_member_remove_handler__
from events.on_member_join_handler import on_member_join_handler__
from events.on_message_handler import on_message_handler__
from db_elements import define_messages, define_roles, define_commands
from functions import log, sendEmail
from keep_alive import keep_alive
from datetime import datetime
import discord
import os

# TODO:
# imporove logging
# verify command to restart
# make welcome message more robust/simplify ifelse spam
# after verification - free change state
# slash commands
# remove stop and change message to leave server
# add $help
# improve send_admin_mail to allow spaces in body
# respond function for command response and verification
# reset user

# BUGS:
# handle Key error on delete if - maybe other 
# handle $reset on non user


print("Starting...")

# Initialize Database
define_messages()
define_commands()
define_roles()

# Initialize client
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

# Initialize event handlers
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


# Initialize keep_alive script
keep_alive()

# Start bot
client.run(os.environ['Token'])

# Send email on failure
sendEmail(port = 465, server = "mail.sieb.net", sender = "TRUEBot@engclub.ca", receiver = "trenton@sieb.net", password = str(os.environ['mail_pass']), message = "The bot has died at {deathtime}.".format(deathtime = datetime.now()), reply = "", sender_nick = "TRUE Discord Bot", subject = "FATAL ERROR", username = str(os.environ['username']))
print("Bot is dead")