from functions import is_admin, initial_message, delete_user, get_user, update_user, send_admin_mail, is_new, add_user, sendVerification, log_print, get_message, log

async def on_message_handler__(client, message):
  await log_print(client, '{0.author.display_name} messaged {0.content}'.format(message))
  print(message.author.display_name, "messaged", message.content)
  if command_handler(client, message):
    return
  if global_response_handler(client, message = message):
    return
  if private_response_handler(client, message = message):
    return
