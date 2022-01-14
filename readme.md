# Thompson Rivers University Student Union Engineering Club Discord Bot
This is the python code for the Discord bot made by Trenton Sieb. The bot is designed to provide user verification for the TRU Engineering Discord server.

## Conversation States:

The user is welcomed to the TRUE server and their data `conv_state` is set to 0.

### 0. -  *Initial state.*
A choice is offered between joining the server as an engineering student, a club member, both or neither.
The choice is offered by sending a message with five reactions available to the user.
If the user reacts to the message using the emojis provided, specific actions are taken.

1. Set `user["conv_state"] = 1` and `user["purpose"] = 1` 
2. Set `user["conv_state"] = 1` and `user["purpose"] = 2`
3. Set `user["conv_state"] = 1` and `user["purpose"] = 1`
 
### 1. - *Request email*

 :one: emoji, the 
The 1, 2, or 3 go to 1. If 4 ask for reason of joining and go to 98
  If valid email given. Generate code. Send email. go to 2

2 - Check entered code against stored user code
  If correct code. give user active role based on original request. go to 5
  otherwise ask to renter code, email or cancel. 
  if code go to 2 if email go to 1 if cancel go to 99

96 - Verified

97 - Pause interaction

98 - Respond: will review this message and get back to you.

99 - Canceled entry. Kick from server