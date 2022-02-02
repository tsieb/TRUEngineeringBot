

# ========== Global Responses ==========

async def global_response_handler(client, message = None, member = None, payload = None):
  if message:
    for i in db["global_response"]["message"]:
      if (i["location"] == message.id):
        await i["handler"](client, message)

  elif member:
    for i in db["global_response"]["member"]:
      if (i["location"] == member.id):
        await i["handler"](client, member)

  elif payload:
    for i in db["global_response"]["payload"]:
      if (i["location"] == payload.message_id):
        await i["handler"](client, member)
        return(True)



# ========== Private Responses ==========

async def private_response_handler(client, message = None, member = None, payload = None):
  if message:
    for i in get_user(message.author.id):
      if (i["location"] == message.channel.id):
        if (await i["handler"](client, message = message)):
          return(True)
  elif member:
    for i in get_user(member.id):
      if (await i["handler"](client, member = member)):
        return(True)
  elif payload:
    for i in get_user(payload.user_id):
      if (i["location"] == payload.channel_id):
        if (await i["handler"](client, member)):
          return(True)
  return(False)


# ========== Commands ==========

async def command_handler(client, message):
  if (message.content[0] == db["settings"]["prefix"]):
    if (get_user(message.author.id)["role"] == "admin"):
      for i in db["commands"]["admin"]:
        if (message.content.startswith(db["settings"]["prefix"]+i)):
          if (await db["commands"]["admin"][i](client, message)):
            return(True)
  return(False)