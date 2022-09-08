from functions import log, initial_message

async def on_member_join_handler__(client, member):
  if (member == client.user):
    return
  await initial_message(client, member)
  await log(client, '{0.display_name} has joined the server'.format(member), 1)