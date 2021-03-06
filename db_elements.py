from replit import db

def define_messages():
  messages = {"welcome": "Welcome to the TRU Engineering Discord server.\nPlease use the reactions below to define your reason for joining the server.\n1 - Engineering Student\n2 - TRUSU Engineering Club\n3 - Engineering Student and Club\n4 - Neither an engineering student nor a club member\n5 - TRU professor\nStop will halt all further messages\n*At any point you can type `restart` to begin the process again.*", "welcome_reactions": ["\U00000031\U0000fe0f\U000020e3", "\U00000032\U0000fe0f\U000020e3", "\U00000033\U0000fe0f\U000020e3", "\U00000034\U0000fe0f\U000020e3", "\U00000035\U0000fe0f\U000020e3", "🛑"] , "email" : "Please type your TRU email. It must end with `@mytru.ca` or `@tru.ca`.","verify": "A Verification emaill has been sent to you. Please enter the code provided below.\n*Enter `resend` to resend the email to the same address\nEnter `change` to enter a new email address*", "complete": "Thanks for verifying your account! You now have access to the server. Please read the rules before chatting. If you ever decide to leave the server, all your data will be deleted and you will need to re-verify. All the code for the bot can be viewed on GitHub", "invalid_email": "The email you entered is invalid", "invalid_code": "The code you entered is wrong", "manual": "Why would you like to join the TRU Engineering Discord server?\nYour reply will be sent directly to the admin for manual verification.", "manual_response": "You will be notified within 48 hours of the result.", "limit_reached":"You have entered the maximum number of attempts. If you still wish to gain access to the server, DM the admin."}
  
  db["messages"] = messages

def define_roles():
  roles = {"club": 931759411641331752, "student": 887072932604575796, "unverified": 932086744776605729}
  db["roles"] = roles

def define_commands():
  commands = {}
  db["commands"] = commands