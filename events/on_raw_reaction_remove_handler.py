import importlib
from functions import log_print

response_handler = importlib.machinery.SourceFileLoader('response_handler', 'response/response_handler.py').load_module()

async def on_raw_reaction_remove_handler__(client, payload):
  await log_print(client, '{0.user_id} removed reaction {0.emoji}'.format(payload))
  print(payload.user_id, "reacted with", payload.emoji)

  if (await response_handler.private_response_handler(client, payload = [payload, "remove"])):
    return
  if (await response_handler.global_response_handler(client, payload = [payload, "remove"])):
    return