from functions import *
import random

async def on_message_handler__(client, message):
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
      update_user(client, user)
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
      await message.author.send(get_message("email"))
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
        await message.author.send(get_message("verify"))
      else:
        await message.author.send(get_message("invalid_email"))

    elif (user["conv_state"] == 3):
      try:
        if (int(message.content.strip()) == user["verify_code"]):
          await log_print(client, "Sending complete message to " + message.author.display_name)
          await message.author.send(get_message("complete"))
          user["conv_state"] = 96
        else:
          user["attempts"] += 1
          await log_print(client, "User has made " + str(user["attempts"]) + "attempts")
          await message.author.send(get_message("invalid_code"))
      except: 
        pass
      if (user["attempts"] >= 10):
        user["conv_state"] = 90
        await message.author.send(get_message("limit_reached"))
  await update_user(client, user)