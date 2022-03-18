import importlib
from functions import log_print

response_handler = importlib.machinery.SourceFileLoader('response_handler', '../response/response_handler.py').load_module()

async def on_message_handler__(client, message):
  await log_print(client, '{0.author.display_name} messaged {0.content}'.format(message))
  print(message.author.display_name, "messaged", message.content)
  if response_handler.command_handler(client, message):
    return
  if response_handler.global_response_handler(client, message = message):
    return
  if response_handler.private_response_handler(client, message = message):
    return
