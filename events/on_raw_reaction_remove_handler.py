from functions import log, add_role, get_role

async def on_raw_reaction_remove_handler__(client, payload):
  if (payload.user_id == client.user.id):
    return
  try:
    await log(client, '{0.member.display_name} has removed reaction {0.emoji} in {0.channel_id}'.format(payload), 0)
  except:
    await log(client, '{0.user_id} has removed reaction {0.emoji} in {0.channel_id}'.format(payload), 0)
  if (payload.message_id == 932827444933718088):
    await add_role(client, payload.user_id, get_role("club"))
    await log(client, '{0.user_id} has removed the club  role'.format(payload), 0)