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

#Other vars
wordin = ""
listOfWords = ""

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

#Checks word for anagram
def checkWord(word, chkword):
    for letter in word:
        if letter in chkword:
            chkword = chkword.replace(letter, "", 1)
        else:
            return 0
    return 1

#Scans words in a message
def scanMessage(msg):
    msg.lower()
    StringConcat = [""]
    #Open file and read array
    file = open('scanwords.txt', 'r')
    for line in file:
        line = line.replace('\n','')
        line = line.lower()
        if(line in msg):
            StringConcat.append(line)
    file.close()
    return StringConcat
    
#Commands
@client.event
async def on_message(message):

    #Named commands
    if(message.content[:1] == prefix):
        #If message starts with the prefix, it's a command. Handle it as such

        #Command structure:
        #if(message.content == (prefix + "[Command Invoker]")):
        #   log("Running [Command name] command...")
        #   Do stuff
        #   End with:
        #   await client.send_message(client.get_channel(message.channel.id), [Message (result of command)])

        #Help command
        if(message.content[:5] == (prefix + "help")):
            log("Running help command...")
            SplitMessage = message.content.split(" ")
            if(SplitMessage[1] == ""):
                await client.send_message(client.get_channel(message.channel.id),'Idk, man. Just fuck around')
            
            elif(SplitMessage[1] == "anagram"):
                await client.send_message(client.get_channel(message.channel.id),'Usage \';anagram [Word]\' where word is the word you want anagrams of')

            elif(SplitMessage[1] == "ping"):
                await client.send_message(client.get_channel(message.channel.id),'Mostly used to test if the bot is working. If it replies ping, then all is well')

            elif(SplitMessage[1] == "ooer"):
                await client.send_message(client.get_channel(message.channel.id),'Tells everyone a VERY important message')

            elif(SplitMessage[1] == "wednesday"):
                await client.send_message(client.get_channel(message.channel.id),'Is it wednesday, my dudes?')

            elif(SplitMessage[1] == "getPost"):
                await client.send_message(client.get_channel(message.channel.id),'Usage: \'getPost [Sub] [Posts]\' where Sub is the target subreddit, and Posts is the number of posts to get')
                await client.send_message(client.get_channel(message.channel.id),'Posts is limited to 20 to prevent spam (looking at you, sephie)')
                await client.send_message(client.get_channel(message.channel.id),'The target subreddit has to be publicly available')

            elif(SplitMessage[1] == "copypasta"):
                await client.send_message(client.get_channel(message.channel.id), "Gets a random copypasta from r/copypasta")

            elif(SplitMessage[1] == "list"):
                await client.send_message(client.get_channel(message.channel.id),'Commands list: (Type Type \';help [name of command]\' to get help for that command)')
                await client.send_message(client.get_channel(message.channel.id),'anagram')
                await client.send_message(client.get_channel(message.channel.id),'ping')
                await client.send_message(client.get_channel(message.channel.id),'ooer')
                await client.send_message(client.get_channel(message.channel.id),'wednesday')
                await client.send_message(client.get_channel(message.channel.id),'getPost')
                await client.send_message(client.get_channel(message.channel.id),'copypasta')
                await client.send_message(client.get_channel(message.channel.id),'Also, this bot has a 10% chance of giving a random response to any message that is not a command')

            else:
                await client.send_message(client.get_channel(message.channel.id),'Type \';help [name of command]\' to get help for that command')
                await client.send_message(client.get_channel(message.channel.id),'Type \';help list\' to get a list of commands')

        #Anagram command
        elif(message.content[:8] == (prefix + "anagram")):
            log("Running anagram command...")
            SplitMessage = message.content.split(" ")
            if(SplitMessage[1] == ""):
                await client.send_message(client.get_channel(message.channel.id), "Something went wrong, did you type the parameters correctly?")
            else:
                listOfWords = ""
                wordin = SplitMessage[1]
                wordin = wordin.upper()
                WordFile=open("wordlist.txt", "r")
                for line in WordFile:
                    line = line.strip()
                    if checkWord(line,wordin):
                        if(len(line)>2):
                            listOfWords = listOfWords + line + ", "
            WordFile.close()
            if(listOfWords == ""):
                await client.send_message(client.get_channel(message.channel.id), "No anagrams found")
            else:
                await client.send_message(client.get_channel(message.channel.id),listOfWords[:(len(listOfWords) -2)])
        
        #Targets a channel and get it's ID        
        elif (message.content == prefix + "target"):
            log("Runnning target command...")
            await client.send_message(client.get_channel(message.channel.id), message.channel.id)

        #Spam command
        elif (message.content[:5] == prefix + "spam"):
            log("Running Spam command...")
            SplitMessage = message.content.split("|")
            if((int(SplitMessage[1]) > 0 and int(SplitMessage[1]) < 21) or str(message.author.id) == "262753744280616960"):
                for i in range(0, int(SplitMessage[1])):
                    await client.send_message(client.get_channel(message.channel.id), SplitMessage[2])
                await client.send_message(client.get_channel(message.channel.id), "Done")
            else:
                await client.send_message(client.get_channel(message.channel.id), 'Something went wrong, did you type the parameters correctly?')
                await client.send_message(client.get_channel(message.channel.id), 'You can only spam 20 messages, unless you created this bot (rhodso)')

        #Ping command
        elif(message.content == (prefix + "ping")):
            log("Running ping command...")
            await client.send_message(client.get_channel(message.channel.id), 'Pong!')
            #await client.send_message(client.get_channel(message.channel.id), str(message.author.id))

		#Ooer command
        elif(message.content == (prefix + "ooer")):
            log("Running Ooer command...")
            await client.send_message(client.get_channel(message.channel.id), '@everyone Ooer')
        
        #Wednesday command
        elif(message.content == (prefix + "wednesday")):
            log("Running Wednesday command...")
            if(datetime.datetime.now().strftime("%A") == "Wednesday"):
                #It is wednesday, my dudes
                await client.send_message(client.get_channel(message.channel.id), "It is wednesday, my dudes")
                await client.send_message(client.get_channel(message.channel.id), "https://i.redd.it/jk7kw2qzhv711.jpg")
            else:
                await client.send_message(client.get_channel(message.channel.id), "It is not wednesday")
        
        #Copypasta command
        elif(message.content == (prefix + "copypasta")):
            log("Running copypasta command...")
            submission = reddit.subreddit('copypasta').random()
            await client.send_message(client.get_channel(message.channel.id), submission.selftext)

        #getPost command
        elif(message.content[:8] == (prefix + "getPost")):
            log("Running getPost command...")
            SplitMessage = message.content.split(" ")

            #Defaults
            targetSub = "aww"
            NumberOfPosts = 1

            #Try to parse args
            try:
                targetSub = SplitMessage[1]
                NumberOfPosts = int(SplitMessage[2])
                log(" |")
                log(" ->Target sub = " + targetSub)
                log("   Posts requested = " + str(NumberOfPosts))

            #Throw exception if it goes wrong
            except:
                log("Something went wrong in getPost command. Parameters probably not typed correctly")
                await client.send_message(client.get_channel(message.channel.id), 'Something went wrong, did you type the parameters correctly?')
            
            #Limits
            if((messaage.author != "rhodso") & (NumberOfPosts > 20)):
                await client.send_message(client.get_channel(message.channel.id), "Too many posts requested. Post requests limited to 20 to prevent spam")
            else:
                #Get subreddit
                subreddit = reddit.subreddit(targetSub)
            
                #Get posts
                i = 0
                for submission in subreddit.hot(limit=NumberOfPosts): #Need to figure out how to not get stickied posts
                    i = i + 1
                    url = submission.url
                    await client.send_message(client.get_channel(message.channel.id), "Post " + i + "/" + NumberOfPosts + ": " + url)
            
                await client.send_message(client.get_channel(message.channel.id), "Request " + message.content + " finished")

    #Read keyword in message response commands
    elif(message.content != ""):
        
        if(str(message.author.id) != '386480630952624129'):
            returnString = ""

            ListOfWords = scanMessage(message.content)
            if(len(ListOfWords) == 1):
                pass

            elif(len(ListOfWords) == 2):
                 returnString = ":sweat_drops: _Giggity_ :sweat_drops:"
        
            elif(len(ListOfWords) == 3):
                returnString = ":sweat_drops: _Giggity_ _Giggity_ :sweat_drops:"

            else:
                returnString = ":sweat_drops: _Giggity_ _Giggity_ _Goo_ :sweat_drops:"

            for i in range(len(ListOfWords)):
                if(ListOfWords[i] != ""):
                    returnString = returnString + ", \'" + ListOfWords[i] + "\'"
        
            if(returnString != ""):
                await client.send_message(client.get_channel(message.channel.id), returnString)
    
    #Random response
    if(random.randint(1,10) < 2):
        if(str(message.author) != '386480630952624129'):    
            log("Message will be replied to")
            if(str(message.author) == '262753744280616960'):
                await client.send_message(client.get_channel(message.channel.id), 'Praise you, ' + message.author.mention)
            else:
                await client.send_message(client.get_channel(message.channel.id), 'Fuck you, ' + message.author.mention)
    else:
        pass

#Run bot
client.run(str(getToken()))
