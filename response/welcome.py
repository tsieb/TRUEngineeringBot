async def welcome_handler(client, message = None, payload = None, member = None):
  if member:
    user = get_user(member.id)
  elif payload:
    user = get_user(payload.user_id)
  elif message:
    user = get_user(message.author.id)
  if(not("welcome" in user["response"])):
      user = await welcome_message(client, user)
  elif (user["response"]["welcome"]["conv_state"] in [range(90, 100)]):
    return False

  
    
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

  elif (user["response"]["welcome"]["conv_state"] == 0 and payload):
    if (payload.message_id == user["response"]["welcome"]["react_msg_id"]):

  elif (user["response"]["welcome"]["conv_state"] == 2 and message):
    if (message.content.strip().find("@mytru.ca", 1) != -1 or message.content.strip().find("@tru.ca", 1) != -1):
      user["email"] = message.content.strip("")
      user["response"]["welcome"]["verify_code"] = random.randint(10000, 99999)
      user["response"]["welcome"]["conv_state"] = 3
      user["response"]["welcome"]["attempts"] = 0
      sendVerification(user)
      await log_print(client, "Sending verify message to " + message.author.display_name)
      await message.author.send(get_message("verify"))
    else:
      await message.author.send(get_message("invalid_email"))

  elif (user["response"]["welcome"]["conv_state"] == 3 and message):
    try:
      if (int(message.content.strip()) == user["response"]["welcome"]["verify_code"]):
        await log_print(client, "Sending complete message to " + message.author.display_name)
        await message.author.send(get_message("complete"))
        user["response"]["welcome"]["conv_state"] = 96
        await log(client, '{0.author.display_name} has completed verification.'.format(message), 1)
      else:
        user["response"]["welcome"]["attempts"] += 1
        await log_print(client, "User has made " + str(user["response"]["welcome"]["attempts"]) + "attempts")
        await message.author.send(get_message("invalid_code"))
    except: 
      # TODO Add invalid entry message
      pass
    if (user["response"]["welcome"]["attempts"] >= 10):
      user["response"]["welcome"]["conv_state"] = 90
      await message.author.send(get_message("limit_reached"))

async def welcome_message(client, user):
  user["response"]["welcome"] = {}
  user["response"]["welcome"]["conv_state"] = 0
  member = client.get_user(user["user_id"])
  msg = await member.send(get_message("welcome"))
  for emoji in get_message("welcome_reactions")):
    await msg.add_reaction(emoji)
  user["response"]["welcome"]["react_msg_id"] = msg.id
  await log_print(client, "Sending welcome message to " + member.display_name)
  return user
  
def sendVerification(user):
  password = os.environ['mail_pass']
  username = os.environ['username']
  port = 465
  server = "mail.sieb.net"
  sender = "noreply@engclub.ca"
  receiver = user["email"]
  subject = "TRUE Verification Email"
  message = "Thanks for joining the TRUE Discord Server.\nYour validation code is:\t{code}\n\nIf you did not request this verification email, you can simply ignore it.".format(code = user["verify_code"])
  sendEmail(port = port, server = server, sender = sender, receiver = receiver, password = password, message = message, reply = "siebt19@mytru.ca", sender_nick = "TRUSU Engineering Club", subject = subject, username = username)
