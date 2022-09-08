import functions
import random
import response_handler

async def welcome_handler(client, message = None, payload = None, member = None):
  # Collect the user data
  if message:
    user = functions.get_user(message.author.id)
  elif payload:
    user = functions.get_user(payload[0].user_id)
  elif member:
    user = functions.get_user(member[0].id)

    
  if(not("welcome" in user["response"])): # Check if user has started the welcome flow
    user = await welcome_send_message(client, user)
    
  elif (user["response"]["welcome"]["conv_state"] in [range(90, 100)]): # Check if user has completed the welcome flow
    return False
    
  if (user["response"]["welcome"]["conv_state"] == 0 and payload): # Save welcome reactions
    for i in welcome_get_reaction():
      if ([f"0x{ord(c):08x}" for c in payload.emoji.name] == i[1]):
        if (i[2] != None):
          for i in i[2]: user["purpose"].append(i[2])
            
    if (user["purpose"] != [] and user["purpose"] != ["other"]): # Check then start email flow
      user_obj = client.get_user(payload.user_id)
      await user_obj.send(functions.get_message("email"))
      user["response"]["welcome"]["conv_state"] = 2
      await functions.log_print(client, "Sending email message to" + user_obj.display_name) 
      
    elif (user["purpose"] == ["other"]): # Check then start other flow
      user_obj = client.get_user(payload.user_id)
      await user_obj.send(functions.get_message("manual"))
      user["conv_state"] = 4
      await functions.log_print(client, "Sending manual verification message to" + user_obj.display_name)

  elif (user["response"]["welcome"]["conv_state"] == 2 and message): # Check for valid email then continue to verify step
    if (message.content.strip().find("@mytru.ca", 1) != -1 or message.content.strip().find("@tru.ca", 1) != -1):
      user["email"] = message.content.strip("")
      user["response"]["welcome"]["verify_code"] = random.randint(10000, 99999)
      user["response"]["welcome"]["conv_state"] = 3
      user["response"]["welcome"]["attempts"] = 0
      welcome_send_verification(user)
      await functions.log_print(client, "Sending verify message to " + message.author.display_name)
      await message.author.send(functions.get_message("verify"))
    else:
      await message.author.send(functions.get_message("invalid_email"))

  elif (user["response"]["welcome"]["conv_state"] == 3 and message): # Check verify code then verify user
    try:
      if (int(message.content.strip()) == user["response"]["welcome"]["verify_code"]):
        await functions.log_print(client, "Sending complete message to " + message.author.display_name)
        await message.author.send(functions.get_message("complete"))
        user["response"]["welcome"]["conv_state"] = 96
        await functions.log(client, '{0.author.display_name} has completed verification.'.format(message), 1)
      else:
        user["response"]["welcome"]["attempts"] += 1
        await functions.log_print(client, "User has made " + str(user["response"]["welcome"]["attempts"]) + "attempts")
        await message.author.send(functions.get_message("invalid_code"))
    except: 
      # TODO Add invalid entry message
      pass
    if (user["response"]["welcome"]["attempts"] >= 10): # Check for exceeded attempts then disable verification
      user["response"]["welcome"]["conv_state"] = 90
      await message.author.send(functions.get_message("limit_reached"))

async def welcome_send_message(client, user):
  user["response"]["welcome"] = {"handler":["welcome", "welcome_handler"], "trigger":["dm", "add_reaction"]}
  user["response"]["welcome"]["conv_state"] = 0
  member = client.get_user(user["user_id"])
  msg = await member.send(functions.get_message("welcome"))
  for emoji in welcome_get_reaction():
    await msg.add_reaction(emoji[0])
  user["response"]["welcome"]["msg_id"] = msg.id
  await functions.log_print(client, "Sending welcome message to " + member.display_name)
  return user

def welcome_send_verification(user):
  password = function.get_secret('mail_pass')
  username = function.get_secret('username')
  port = 465
  server = "mail.sieb.net"
  sender = "noreply@engclub.ca"
  receiver = user["email"]
  subject = "TRUE Verification Email"
  message = "Thank you for joining the TRUE Discord Server.\nYour validation code is:\t{code}\n\nIf you did not request this verification email, please ignore it.".format(code = user["verify_code"])
  functions.sendEmail(port = port, server = server, sender = sender, receiver = receiver, password = password, message = message, reply = "siebt19@mytru.ca", sender_nick = "TRUSU Engineering Club", subject = subject, username = username)

def welcome_get_reaction():
  return([["\U00000031\U0000fe0f\U000020e3", ['0x00000031', '0x0000fe0f', '0x000020e3'], ["student"] ], ["\U00000032\U0000fe0f\U000020e3", ['0x00000032', '0x0000fe0f', '0x000020e3'], ["club"] ], ["\U00000033\U0000fe0f\U000020e3", ['0x00000033', '0x0000fe0f', '0x000020e3'], ["student", "club"] ], ["\U00000034\U0000fe0f\U000020e3", ['0x00000034', '0x0000fe0f', '0x000020e3'], ["other"] ], ["\U00000035\U0000fe0f\U000020e3", ['0x00000035', '0x0000fe0f', '0x000020e3'], ["faculty"] ], ["🛑", ['0x0001f6d1'], None]])