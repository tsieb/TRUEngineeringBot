from replit import db
import functions
import importlib


# ========== Global Responses ==========
async def global_response_handler(client, message = None, member = None, payload = None):
  if message:
    for i in db["global_responses"]["message"]:
      if ("dm" in db["global_responses"]["message"][i]["location"] and message.channel.type == "private" or message.channel.id in db["global_responses"]["message"][i]["location"]):
        print("Calling message public function")
        module = importlib.import_module("response." + db["global_responses"]["message"][i]["handler"][0])
        if await getattr(module, db["global_responses"]["message"][i]["handler"][1])(client, message = message):
          return True

  elif member: # member = [member_object, "trigger_type"]
    for i in db["global_responses"]["member"]:
      if (member[1] in db["global_responses"]["member"][i]["trigger"]):
        module = importlib.import_module("response." + db["global_responses"]["member"][i]["handler"][0])
        if await getattr(module, db["global_responses"]["member"][i]["handler"][1])(client, member = member):
          return True

  elif payload: # payload = [payload_object, "trigger_type"]
    for i in db["global_responses"]["payload"]:
      if (payload[0].message_id in db["global_responses"]["payload"][i]["location"] or payload[0].channel_id in db["global_responses"]["payload"][i]["location"]):
        print("Calling payload public function")
        module = importlib.import_module("response." + db["global_responses"]["payload"][i]["handler"][0])
        if await getattr(module, db["global_responses"]["message"][i]["handler"][1])(client, payload = payload):
          return(True)

        
# ========== Private Responses ==========
async def private_response_handler(client, message = None, member = None, payload = None):
  if message:
    user = functions.get_user(message.author.id)
    if len(user["response"]) > 0:
      for i in user["response"]:
        if ((message.channel.id in user["response"][i]["trigger"]) or ("dm" in user["response"][i]["trigger"] and message.channel.type == "private")):
          print("Calling message private function")
          module = importlib.import_module("response." + user["response"][i]["handler"][0]) # TODO make more robust, longer module path
          if (await getattr(module, user["response"][i]["handler"][1])(client, message = message)):
            return(True)
  elif member: #TODO add leave member
    user = functions.get_user(member[0].id)
    for i in user["response"]:
      if "user_id" in i:
        if (i["user_id"] == member[0].id):
          if (await getattr(importlib.import_module(i["handler"][0]), i[1])(client, user, member = member)): # member is [member_object, "trigger_type"]
            return(True)
  elif payload:
    user = functions.get_user(payload[0].user_id)
    if len(user["response"]) > 0:
      for i in user["response"]:
          if ((payload[0].message_id in user["response"][i]["trigger"])):
            print("Calling payload private function")
            module = importlib.import_module("response." + user["response"][i]["handler"][0]) # TODO make more robust, longer module path
            if (await getattr(module, user["response"][i]["handler"][1])(client, payload = payload)): # Payload is [payload_object, "trigger_type"]
              return(True)
  return(False)


# ========== Commands ==========
async def command_handler(client, message):
  if message.content == "":
    return(False)
  if (message.content[0] == db["settings"]["prefix"]):
    if (functions.get_user(message.author.id)["role"] == "admin"): # TODO in settings have array of server roles to permit commands
      for k, v in db["commands"]["admin"]:
        if (message.content.startswith(db["settings"]["prefix"]+k)):
          if (await getattr(importlib.import_module(v[0]), v[1])(client, message)):
            return(True)
    else:
      for k, v in db["commands"]["admin"]:
        if (message.content.startswith(db["settings"]["prefix"]+k)):
          if (await getattr(importlib.import_module("response." + v[0]), v[1])(client, message)):
            return(True)
  return(False)