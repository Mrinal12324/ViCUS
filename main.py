import discord
import os
import requests
import json
import random
from replit import db


client =discord.Client()

sad_words=["sad","depressed","unhappy","angry","n=miserable"]

st_encourage =["Cheer up!","Hang in there","On my Way"]

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragement(index):
  encouragements=db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"]=encouragements

def get_quote():
  respone = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(respone.text)

  quote=json_data[0]['q']  + ' -' + json_data[0]['a']
  return(quote)
def get_image():
  resp=requests.get("https://api.unsplash.com/photos/random?client_id={1.key}".format(os.getenv('Unsplash')))
  json_img=json.loads(resp.text)

  img=json_img[0]['title']+' of'+json_img[0]['cover_photo']
  return(img)



@client.event
async def on_ready():
  print('We have loggedd as  {0.user} :)'.format(client))
@client.event
async def on_message(message):
  if message.author==client.user:
    return

  msg=message.content
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
  
  if message.content.startswith('$inspire'):
    quote=get_quote()
    await message.channel.send(quote)

  #if msg.startswith('$image'):
  #  imag=get_image()
  #  await message.channel.send(imag)
  options=st_encourage
  if "encouragements" in db.keys():
    options=options + db["encouragements"]
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(st_encourage))

  if msg.startswith('$new'):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouragements message added.")
  
  if msg.stratswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements=db["encouragements"]
    await msg.send(encouragements)




client.run(os.getenv('TOKEN'))
client.run(os.getenv('Unsplash'))