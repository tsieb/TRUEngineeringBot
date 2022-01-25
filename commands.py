from functions import delete_user, add_user, sendVerification, log, get_message, initial_message, get_user, update_user, send_admin_mail

# TODO add log to each cmd

# ---- USER DM COMMANDS ----

  # --- RESTART ---
async def cmd_restart(client, message):
  delete_user(id = message.author.id)
  user = add_user(message.author.id)
  await log(client, '{0.author.display_name} has restarted'.format(message), 0)

  # --- RESEND ---
async def cmd_resend(client, user):
  sendVerification(user)

  # --- CHANGE ---
async def cmd_change(client, message, user):
  await log(client, "Sending email message to " + message.author.display_name, 0)
  await message.author.send(get_message("email"))
  user["conv_state"] = 2


# ---- ADMIN COMMANDS ----

  # --- ADD ---
async def adm_add(client, message, cmd):
  initial_message(client, member = None, id = cmd[1])
  try:
    await log(client, '{0.author.display_name} used the $add command on {1}}'.format(message, client.get_user(cmd[1])), 0)
  except:
    await log(client, '{0.author.display_name} used the $add command on {1}}'.format(message, cmd[1]), 0)
        
# --- DELETE ---
async def adm_delete(client, message, cmd):
  delete_user(id = cmd[1])
  await message.author.send("User deleted from database")
  try:
    await log(client, '{0.author.display_name} used the $delete command on {1}}'.format(message, client.get_user(cmd[1])), 0)
  except:
    await log(client, '{0.author.display_name} used the $delete command on {1}}'.format(message, cmd[1]), 0)

# --- RESET ---
async def adm_reset(client, message, cmd):
  user = get_user(cmd[1])
  user["conv_state"] = 0
  update_user(client, user)
  initial_message(client, member = None, id = cmd[1])
  try:
    await log(client, '{0.author.display_name} used the $reset command on {1}}'.format(message, client.get_user(cmd[1])), 0)
  except:
    await log(client, '{0.author.display_name} used the $reset command on {1}}'.format(message, cmd[1]), 0)

# --- EMAIL ---
async def adm_email(message):
  await message.author.send("""sender = \"\", receiver = \"\", message = \"\", sender_nick = \"\", subject = \"\",reply = \"\"""")

async def adm_send(client, message, cmd):
  send_admin_mail(sender = cmd[1], receiver = cmd[2], message = cmd[3], sender_nick = cmd[4], subject = cmd[5], reply = cmd[6])
  try:
    await log(client, '{0.author.display_name} sent an email to {1}}'.format(message, cmd[2]), 0)
  except:
    await log(client, '{0.author.display_name} used the $add command on {1}}'.format(message, cmd[2]), 0)

# --- MSG ---
async def adm_msg(client, message, cmd):
  try:
    msg = ""
    for i in cmd[2:]:
      msg += i
    target = await client.fetch_user(cmd[1])
    await target.send(msg)
    await log(client, '{0.author.display_name} used the $msg command on {1} to send {2}}'.format(message, client.get_user(cmd[1]), msg), 0)
  except Exception as e:
    print(e)
    await message.author.send("Invalid target")