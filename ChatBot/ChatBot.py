#Imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import datetime
import random
import praw

#Set prefix character
prefix = ";"

#Reddit variables
CLID = "IGAjcEE-70TWfw"
SECT = "zu64wRhKJHCoGHX0HDLh2L34Idk"
AGNT = "ChatBot"

reddit = praw.Reddit(client_id=CLID, client_secret=SECT, user_agent=AGNT)

#Def log method
def log(Message):
    print(str(datetime.datetime.now())+ '   ' + str(Message))

#Def Method to read token from the file
def getToken():
    tokenFile = open('token.txt','r')
    token = tokenFile.read()
    return token

#Define client
client = Bot(description='', command_prefix=prefix, pm_help = False)

#Startup sequence
@client.event
async def on_ready():
    log('Initialising...')
    log('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    log('')
    log('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    log('Ready!')
    return await client.change_presence(game=discord.Game(name='with myself')) 

#Commands
@client.event
async def on_message(message):
    if(message.content[:1] == prefix):
        #If message starts with the prefix, it's a command. Handle it as such

        #Command structure:
        #if(message.content == (prefix + "[Command Invoker]")):
        #   log("Running [Command name] command...")
        #   Do stuff
        #   End with:
        #   await client.send_message(client.get_channel(message.channel.id), [Message (result of command)])

        #Help command
        if(message.content == (prefix + "help")):
            log("Running help command...")
            await client.send_message(client.get_channel(message.channel.id),'Idk, man. Just fuck around')

        #Ping command
        if(message.content == (prefix + "ping")):
            log("Running ping command...")
            await client.send_message(client.get_channel(message.channel.id), 'Pong!')

		#Ooer command
        if(message.content == (prefix + "ooer")):
            log("Running Ooer command...")
            await client.send_message(client.get_channel(message.channel.id), '@everyone Ooer')
        
        #getPost Command
        if(message.content[:8] == (prefix + "getPost")):
            log("Running getPost command...")
            SplitMessage = message.content.split(" ")

            targetSub = "aww"
            NumberOfPosts = 1

            try:
                targetSub = SplitMessage[1]
                NumberOfPosts = int(SplitMessage[2])

            except:
                log("Something went wrong in getPost command. Parameters probably not typed correctly")
                await client.send_message(client.get_channel(message.channel.id), 'Something went wrong, did you type the parameters correctly?')

            subreddit = reddit.subreddit(targetSub)
            
            for submission in subreddit.hot(limit=10): #Need to figure out how to not get stickied posts
                url = submisstion.url
                await client.send_message(client.get_channel(message.channel.id), url)

    elif(random.randint(1,10) == 5):
        #Message is not a command, roll to see if it's a random response
        log("Message will be replied to")
        await client.send_message(client.get_channel(message.channel.id), 'Fuck you, ' + message.author.mention)
    
    else:
        pass
    
    

#Run bot
client.run(str(getToken()))