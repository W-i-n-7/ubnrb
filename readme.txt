install python and check "add python to path"
open up a command prompt and copy paste
1. py -m pip install --upgrade pip
2. pip install discord.py requests
then open up and edit the python script and fill the following variables with the correct data:
WEBHOOK_URL on line 12
TOKEN on line 13
allowed_users on line 14

where do i get these?
for webhook url make a new server and edit a channel goto integrations and make a webhook copy its url here
for token go to https://discord.com/developers/applications make a new application you can call it whatever then goto bot and reset token then you will see the token copy it here and while you are here scroll down a little and enable the 3 privileged gateway intents
for allowed_users enable developer mode in discord user settings and right click your name in for example a message and select copy id 

how do i invite the bot?
goto https://discord.com/developers/applications then select your application goto OAuth2 > url generator select bot and then in the window below administrator and you will have the url below that
then open up the url and invite it (to send the invite to others simply send the url in discord)
