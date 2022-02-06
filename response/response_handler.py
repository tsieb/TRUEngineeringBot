from replit import db
import functions
import importlib

# ========== Global Responses ==========

async def global_response_handler(client, message = None, member = None, payload = None):
  if message:
    for i in db["global_response"]["message"]:
      if (i["location"] == message.id):
        await getattr(importlib.import_module(i["handler"][0]), i[1])(client, message)

  elif member:
    for i in db["global_response"]["member"]:
      if (i["location"] == member.id):
        await getattr(importlib.import_module(i["handler"][0]), i[1])(client, member)

  elif payload:
    for i in db["global_response"]["payload"]:
      if (i["location"] == payload.message_id):
        await getattr(importlib.import_module(i["handler"][0]), i[1])(client, payload)
        return(True)


# ========== Private Responses ==========

async def private_response_handler(client, message = None, member = None, payload = None):
  if message:
    for i in functions.get_user(message.author.id):
      if (i["location"] == message.channel.id):
        if (await getattr(importlib.import_module(i["handler"][0]), i[1])(client, message = message)):
          return(True)
  elif member:
    for i in functions.get_user(member.id):
      if (await getattr(importlib.import_module(i["handler"][0]), i[1])(client, member = member)):
        return(True)
  elif payload:
    for i in functions.get_user(payload.user_id):
      if (i["location"] == payload.channel_id):
        if (await getattr(importlib.import_module(i["handler"][0]), i[1])(client, payload = payload)):
          return(True)
  return(False)


# ========== Commands ==========

async def command_handler(client, message):
  if (message.content[0] == db["settings"]["prefix"]):
    if (functions.get_user(message.author.id)["role"] == "admin"):
      for k, v in db["commands"]["admin"]:
        if (message.content.startswith(db["settings"]["prefix"]+k)):
          if (await getattr(importlib.import_module(v[0]), v[1])(client, message)):
            return(True)
    else:
      for k, v in db["commands"]["admin"]:
        if (message.content.startswith(db["settings"]["prefix"]+k)):
          if (await getattr(importlib.import_module(v[0]), v[1])(client, message)):
            return(True)
  return(False)