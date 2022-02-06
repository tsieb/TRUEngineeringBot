import functions

# TODO add log to each cmd

# ---- USER DM COMMANDS ----

  # --- RESTART ---
async def cmd_restart(client, message):
  functions.delete_user(id = message.author.id)
  user = functions.add_user(message.author.id)
  await functions.log(client, '{0.author.display_name} has restarted'.format(message), 0)

  # --- RESEND ---
async def cmd_resend(client, user):
  functions.sendVerification(user)

  # --- CHANGE ---
async def cmd_change(client, message, user):
  await functions.log(client, "Sending email message to " + message.author.display_name, 0)
  await message.author.send(functions.get_message("email"))
  user["conv_state"] = 2


# ---- ADMIN COMMANDS ----

  # --- ADD ---
async def adm_add(client, message, cmd):
  pass
  #TODO re-add this function


  # --- DELETE ---
async def adm_delete(client, message, cmd):
  functions.delete_user(id = cmd[1])
  await message.author.send("User deleted from database")
  try:
    await functions.log(client, '{0.author.display_name} used the $delete command on {1}}'.format(message, client.get_user(cmd[1])), 0)
  except:
    await functions.log(client, '{0.author.display_name} used the $delete command on {1}}'.format(message, cmd[1]), 0)

  # --- RESET ---
async def adm_reset(client, message, cmd):
  user = functions.get_user(cmd[1])
  user["conv_state"] = 0
  functions.update_user(client, user)
  functions.initial_message(client, member = None, id = cmd[1])
  try:
    await functions.log(client, '{0.author.display_name} used the $reset command on {1}}'.format(message, client.get_user(cmd[1])), 0)
  except:
    await functions.log(client, '{0.author.display_name} used the $reset command on {1}}'.format(message, cmd[1]), 0)

  # --- EMAIL ---
async def adm_email(message):
  await message.author.send("""sender = \"\", receiver = \"\", message = \"\", sender_nick = \"\", subject = \"\",reply = \"\"""")

async def adm_send(client, message, cmd):
  functions.send_admin_mail(sender = cmd[1], receiver = cmd[2], message = cmd[3], sender_nick = cmd[4], subject = cmd[5], reply = cmd[6])
  try:
    await functions.log(client, '{0.author.display_name} sent an email to {1}}'.format(message, cmd[2]), 0)
  except:
    await functions.log(client, '{0.author.display_name} used the $add command on {1}}'.format(message, cmd[2]), 0)

  # --- MSG ---
async def adm_msg(client, message, cmd):
  try:
    msg = ""
    for i in cmd[2:]:
      msg += i
    target = await client.fetch_user(cmd[1])
    await target.send(msg)
    await functions.log(client, '{0.author.display_name} used the $msg command on {1} to send {2}}'.format(message, client.get_user(cmd[1]), msg), 0)
  except Exception as e:
    print(e)
    await message.author.send("Invalid target")


async def adm_vote(client, cmd):
  try:
    cmd = input()
    msg = cmd.split(" ")[1:]
    channel_id = msg[0]
    options = {}
    content = ""
    for i in range(len(msg)):
        if (msg[i][1] == "="):
            options[msg[i][0]] = msg[i][2:]
        else:
            content+=msg[i] + " "


    await client.fetch_channel(int(channel_id))
    print(content)
    print(options)
  except:
    pass
