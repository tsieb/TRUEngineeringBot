from functions import log, add_role, is_new, get_user, get_role, log_print, get_message, update_user

async def on_raw_reaction_add_handler__(client, payload):
  if (payload.user_id == client.user.id):
    return
  try:
    await log(client, '{0.member.display_name} has reacted with {0.emoji}  in {0.channel_id}'.format(payload), 0)
  except:
    await log(client, '{0.user_id} has reacted with {0.emoji} in {0.channel_id}'.format(payload), 0)

  if (payload.message_id == 932827444933718088):
    await add_role(client, payload.user_id, get_role("club"))
    await log(client, '{0.user_id} has been given the club role'.format(payload), 0)
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
        await user_obj.send(get_message("email"))
        user["conv_state"] = 2
      else:
        await log_print(client, "Sending manual verification message to" + user_obj.display_name)
        await user_obj.send(get_message("manual"))
        user["conv_state"] = 4
  await update_user(client, user)