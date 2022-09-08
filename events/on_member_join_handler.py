import importlib
from functions import log_print

response_handler = importlib.machinery.SourceFileLoader('response_handler', 'response/response_handler.py').load_module()

async def on_member_join_handler__(client, member):
  await log_print(client, '{0.display_name} joined'.format(member))
  print(member.display_name, "joined")

  if (await response_handler.private_response_handler(client, member = [member, "join"])):
    return
  if (await response_handler.global_response_handler(client, member = [member, "join"])):
    return