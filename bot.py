import os
import discord
import random
import math

client = discord.Client()
deck_dict = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#-------------Shuffle Commands-----------------#
@client.event
async def on_message(m):
  if m.author == client.user:
    return
  if m.content.startswith("c!shuffle"):
    if m.guild is None:
      await m.author.send("You cannot use this in DM.")
      return
    shuffle_cards(m.guild)
    await m.channel.send("Cards are shuffled. 52 left")


  if m.content.startswith("c!draw"):
    if m.guild is None:
      await m.author.send("You cannot use this in DM.")
      return
    
    try:
      num_cards = int(m.content[6:])
    except:
      await m.channel.send("Invalid command.")
      return

    if num_cards <= 0:
      return
    if not (m.guild in deck_dict):
      await m.channel.send("You haven't run any shuffle command yet.")
      return
    if num_cards > len(deck_dict[m.guild]):
      msg = "There are not enough cards. "
      msg += str(len(deck_dict[m.guild]))
      msg += " left."
      await m.channel.send(msg)
      return

    result = draw_cards(num_cards,m.guild)
    await m.author.send(result)
    await m.channel.send("The result has been sent to DM. " + str(len(deck_dict[m.guild])) + " left.")

#-------------Actual Shuffle-----------------#
def shuffle_cards(_guild):
  if not (_guild in deck_dict):
    deck_dict[_guild] = []
  deck_dict[_guild].clear()
  for i in range(0,52):
    deck_dict[_guild].append(i)
  random.shuffle(deck_dict[_guild])

def draw_cards(num,_guild):
  result = "Your cards:" if num!=1 else "Your card"
  result += "\n"
  drawn_cards = []
  for i in range(0,num):
    drawn_cards.append(deck_dict[_guild].pop())
  drawn_cards.sort()
  for i in range(0,num):
    result += card_to_string(drawn_cards[i])
    result += ", " if i < num-1 else "."
    if i < num-1 and math.floor(drawn_cards[i]/13) < math.floor(drawn_cards[i+1]/13):
      result += "\n"
  return result

def card_to_string(c):
  suits = ['♧','♢','♡','♤']
  numbers = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
  return numbers[c%13] + suits[math.floor(c/13)]
#-----------------------------------------#
client.run(os.getenv('TOKEN'))
