from functions import log, delete_user

async def on_member_remove_handler__(client, member):
  delete_user(id = member.id)
  await log(client, '{0.display_name} has left the server'.format(member), 1)