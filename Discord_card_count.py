import discord
from discord.ext import commands
import math
import smtplib
from email.message import EmailMessage
import threading
import datetime
import time

high = ['a','k','q','j','10']
low = ['2','3','4','5','6']
medium = ['7','8','9']

card_points = ['2','3','4','5','6','7','8','9','10','j','q','k','a']
card_signs = ['Hearts','Clubs','Diamonds','Spades']
deck = {}
card_nums = {'count':0,"num_of_decks":8,"base_bet":1}
for points in range(len(card_points)):
    for signs in range (len(card_signs)):
        card = (card_points[points],card_signs[signs])
        deck.update({card_points[points]:card_nums.get("num_of_decks")*4})

def email_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    to = "PUTYOURNUMBERHERE@txt.att.net REPLACE AFTER @ WITH YOUR OWN CELL PROVIDER"
    msg['to'] = to
    user = "PUTYOUREMAILHERE"
    password = "PUTTHEAPPPASSWORDHERE"

    msg['from'] = "PUTNAMEHERE"

    server = smtplib.SMTP("smtp.gmail.com",587)#would advise using gmail, but others may work
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()


'''
https://i2.wp.com/www.lasvegasjaunt.com/wp-content/uploads/2014/07/blackjack-basic-strategy-chart.jpg?ssl=1
'''

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    x = datetime.datetime.now()
    date = x.date()
    hour = x.hour
    minute = x.minute
    AM = True
    if hour > 12:
        AM = False
        hour = hour - 12
    if minute < 10:
        minute = "0{}".format(minute)
    if AM == True:
        current = "{} {}:{}am".format(date, hour, minute)
    else:
        current = "{} {}:{}pm".format(date, hour, minute)
    email_alert("Bot turned on at {}".format(current),"Basebet: {}\nDecks: {}".format(card_nums.get("base_bet"),card_nums.get("num_of_decks")))
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.author.bot != True:
        print(message.content)
        message.content = message.content.lower()
        if (message.content) in card_points:
            if deck.get(message.content) > 0:
                deck.update({message.content:deck.get(message.content)-1})
                card_nums.update({'count':card_nums.get('count')+1})
            else:
                await message.channel.send("There are no more '{}'.".format(message.content))
        elif message.content == 'bet':
            i = 0
            for card_name in deck:
                if card_name in high:
                    i += deck.get(card_name)
                if card_name in low:
                    i -= deck.get(card_name)
            true_count = round((i)/(int(card_nums.get("num_of_decks")) - (card_nums.get('count')/52)),2)
            if true_count >= 1:
                bet = (math.trunc(int(card_nums.get("base_bet")) * true_count))
                await message.channel.send("Running count: {}".format(i))
                await message.channel.send("True count: {}.".format(true_count))
                await message.channel.send("Bet: {}.".format(bet))
                for q in range(0,bet):
                    t = threading.Thread(target = email_alert, args = ("True Count: {}".format(true_count),"Bet: {}".format(bet),))
                    t.start()
                    time.sleep(.1)
            elif true_count < -3:
                await message.channel.send("True count is less than -3. True count: {} alerting player to go to another table.".format(true_count))
                await message.channel.send("Please shuffle the deck upon the player going to a new table.")
                for q in range(0,20):
                    t = threading.Thread(target = email_alert, args = ("True count {}".format(true_count),"Go to another table!"))
                    t.start()
            else:
                await message.channel.send("Running count: {}".format(i))
                await message.channel.send("True count: {}.".format(true_count))
                await message.channel.send("Bet: {}. Base amount.".format(card_nums.get("base_bet")))
                for q in range(0,card_nums.get("base_bet")):
                    email_alert("True Count: {}".format(true_count),"Bet: {}".format(card_nums.get("base_bet")))
        elif message.content == 'showdeck':
            await message.channel.send(deck)
        elif message.content == 'stats':
            if int(card_nums.get("num_of_decks")) == 1:
                await message.channel.send("Working with {} deck. Baseline bet is {}.".format(card_nums.get("num_of_decks"),card_nums.get("base_bet")))
            else:
                await message.channel.send("Working with {} decks. Baseline bet is {}.".format(card_nums.get("num_of_decks"),card_nums.get("base_bet")))
        elif message.content == 'remaining':
            i = 0
            for card_name in deck:
                i += deck.get(card_name)
            await message.channel.send("{}/{} Remaining.".format(i,int(card_nums.get("num_of_decks"))*52))
        elif message.content == 'shuffle':
            for card_name in deck:
                deck.update({card_name:int(card_nums.get("num_of_decks"))*4})
            await message.channel.send("Shuffling.")
        elif message.content == 'ping':
            await message.channel.send(":ping_pong: pong")
        elif message.content.startswith("add"):
            card = message.content.split("add")[1]
            try:
                deck.update({card:deck.get(card)+1})
                card_nums.update({'count':card_nums.get('count')-1})
                await message.channel.send("Added back {}.".format(card))
            except:
                await message.channel.send("'{}' is not a valid card.".format(card))
        elif message.content == "error":
            for i in range(0,20):
                t = threading.Thread(target = email_alert, args = ("there is an error!","Go to the bathroom!"))
                t.start()
            await message.channel.send("Sent 20 msgs to let him know there is an error.")
        elif message.content == 'commands':
            await message.channel.send("bet, showdeck, shuffle, stats, remaining, ping, add, error, changedeck, changebase")
        elif message.content == 'help':
            await message.channel.send("commands: Show the commands in a simpler list.")
            await message.channel.send("bet: Send a text to the counter with the proper info. DO THIS BEFORE THE NEXT HAND PLEASE!")
            await message.channel.send("showdeck: Shows the deck.")
            await message.channel.send("shuffle: If the dealer shuffles, type shuffle.")
            await message.channel.send("stats: More of a debug, will show base bet and baseline bet.")
            await message.channel.send("remaining: Shows how many cards are left in the deck.")
            await message.channel.send("ping: Pong!")
            await message.channel.send("add: If you made a mistake in inputting cards, e.g. took out an 'a' type adda to add the a back in the deck.")
            await message.channel.send("error: Use if need to tell him to go to the bathroom and call you.")
            await message.channel.send("changedeck: Use this to change the number of decks in the shoe. e.g. there are 2 decks in the shoe, type: changedeck2. Use this at the start of the night since casinos have the same num of cards in each shoe.")
            await message.channel.send("changebase: Use this to change the base bet. Default is 1, only change this if the player knows ahead of time. e.g. changebase2 to change the base bet to 2.")
        elif message.content.startswith("changedeck"):
            decknums = message.content.split("changedeck")[1]
            try:
                for card in deck:
                    deck.update({card:int(decknums)*4})
                card_nums.update({"count":0,"num_of_decks":decknums})
                await message.channel.send("Deck has been updated to {} decks.".format(decknums))
                email_alert("Deck update","{} decks".format(decknums))
            except:
                await message.channel.send("Deck cannot change to '{}'.".format(decknums))
        elif message.content.startswith("changebase"):
            base = message.content.split("changebase")[1]
            try:
                card_nums.update({"base_bet":int(base)})
                await message.channel.send("Base bet has been changed to {}".format(base))
                email_alert("Base Bet update","{} is now the base bet.".format(base))
            except:
                await message.channel.send("Base bet could not be changed to '{}'.".format(base))
        else:
            await message.channel.send("Unrecognized command '{}' try typing help.".format(message.content))




client.run('####USEYOUROWNSEEDNERD####')
