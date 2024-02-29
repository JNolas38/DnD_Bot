import discord
import random
import os, asyncio
from discord.ext import commands
import variables
from music_cog import music_cog

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#Global Variables
nameList = []
idList = []


#Events
@client.event
async def on_ready():
    print("The cheese is rolling")
    print("---------------------")


#Auxilary functions
def ChrName (id: int):
    for n in range (len(idList)):
        if idList[n] == id:
            return nameList[n]
    return IdToName(id)

def IdToName (id):
    user = client.get_user(id)
    return format(user.display_name)


#Commands
@client.event
async def on_command_error(ctx, error): #check for wrong commands
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command, try using !h to get a command list")

@client.command()
async def hello(ctx): #Greetings
    await ctx.send("Hey, how you doin?")

@client.command()
async def bye(ctx): #Farewells
    await ctx.send("Smell ya later")

@client.command()
async def loadparty(ctx, file: str=""): #Loads a party from a .txt file
    #Check for erros in command
    if file == "":
        await ctx.send("Error: You have to specify a party to load")
    elif not os.path.isfile("PartyDataBase\\" + file + ".txt"):
        await ctx.send("Error: the party " + file + " doesn't exist")
    elif os.path.getsize("PartyDataBase\\" + file + ".txt") == 0:
        await ctx.send("Error: the party " + file + " is empty")
    
    #function code
    else:
        #Clear the currently loaded party
        if idList != []:
            r = len(idList)
            for n in range (r):
                idList.remove(idList[0])
                nameList.remove(nameList[0])
               
        #Load the given party into the lists
        f = open("PartyDataBase\\" + file + ".txt", "r")
        names = f.readline()
        tempNameList = names.split()
        ids = f.readline()
        tempIdList = ids.split()  
        for n in range (len(tempNameList)):
            idList.append(int(tempIdList[n]))
            nameList.append(tempNameList[n])
        f.close()

        #check for errors in the final lists
        if nameList == []:
            await ctx.send("Error: no characters in the database")
        elif idList == []:
            await ctx.send("Error: no users in the database")
        
        else:
            await ctx.send("Party Loaded!")

@client.command()
async def saveparty(ctx, file: str =""): #saves a party to a .txt file
    #Check for errors
    if file == "":
        await ctx.send("Error: You have to specify a name for the party to save")   
    elif nameList == [] or idList == []:
        await ctx.send("Error: There is no party")
    elif variables.adminRole not in [role.id for role in ctx.author.roles]:
        await ctx.send("Error: You dont have an authorized role")

    else:
        #Check if the file already exists
        if os.path.isfile("PartyDataBase\\" + file + ".txt"):
            #Get comfrimation from user to overwrite existing file
            await ctx.send("A party with the name " + file + " already exists, do you want to overwrite it? (y/n)")
            def check(m): # checking if it's the same user and channel
                return m.author == ctx.author and m.channel == ctx.channel

            try: # waiting for message
                response = await client.wait_for('message', check=check, timeout=30.0) # timeout - how long bot waits for message (in seconds)
            except asyncio.TimeoutError: # returning after timeout
                await ctx.send("Error: Timeout")
                return

            if response.content.lower() not in ("yes", "y"): # lower() makes everything lowercase to also catch: YeS, YES etc.
                return
        
        #function code
        names = ""
        ids = ""
        f = open("PartyDataBase\\" + file + ".txt", "w")
        for n in range (len(idList)):
            names += nameList[n] + " "
            ids += str(idList[n]) + " "
        f.write(names + "\n" + ids)
        f.close()
        await ctx.send("Party saved!")

@client.command()
async def checkparty(ctx, file: str=""): #check the characters of a given party
    
    #Initialize the final string
    finalStr = "The party " + file + " contains:\n"

    #check for errors
    if file == "":
        await ctx.send("Error: You have to specify a party to check")
    elif not os.path.isfile("PartyDataBase\\" + file + ".txt"):
        await ctx.send("Error: Party: " + file + " doesn't exist")
    elif os.path.getsize("PartyDataBase\\" + file + ".txt") == 0:
        await ctx.send("Error: the party " + file + " is empty")

    else:
        #function code
        f = open("PartyDataBase\\" + file + ".txt", "r")
        names = f.readline()
        tempNameList = names.split()
        ids = f.readline()
        tempIdList = ids.split()
        for n in range (len(tempIdList)):
            finalStr += IdToName(int(tempIdList[n])) + ": " + tempNameList[n] + '\n'
        f.close()
        await ctx.send(finalStr)
        
@client.command()
async def partylist(ctx): #Prints list of currently saved parties
    
    #Initialize the final string
    finalStr = ""
    
    #Function code
    for n in os.listdir("PartyDataBase\\"):
        if n.endswith(".txt"):
            y = n.replace(".txt", "")
            finalStr += y + "\n"            
    
    #Check for errors in the final string
    if finalStr == "":
        await ctx.send("Error: There are currently no saved parties")
    else:
        await ctx.send("Currently saved parties:\n" + finalStr)

@client.command()
async def clearparty(ctx): #Clears the currently loaded party
    
    #Get comfirmation from the user
    await ctx.send("Are you sure you want to clear the party? (y/n)")
    def check(m): # checking if it's the same user and channel
        return m.author == ctx.author and m.channel == ctx.channel

    try: # waiting for message
        response = await client.wait_for('message', check=check, timeout=30.0) # timeout - how long bot waits for message (in seconds)
    except asyncio.TimeoutError: # returning after timeout
        await ctx.send("Error: Timeout")
        return

    if response.content.lower() not in ("yes", "y"): # lower() makes everything lowercase to also catch: YeS, YES etc.
        return

    #function code
    r = len(idList)
    for n in range (r):
        idList.remove(idList[0])
        nameList.remove(nameList[0])
    await ctx.send("Party cleared")

@client.command()
async def deleteparty(ctx, file: str = ""): #deletes the given party

    #check for errors
    if variables.adminRole not in [role.id for role in ctx.author.roles]:
        await ctx.send("Error: You dont have an authorized role")
    elif file == "":
        await ctx.send("Error: Specify a party to delete")
    elif not os.path.isfile("PartyDataBase\\" + file + ".txt"):
        await ctx.send ("Error: There is no party with the given name")
    
    else:
        #Get comfirmation from the user
        await ctx.send("Are you sure you want to delete the party " + file + "? (y/n)")
        def check(m): # checking if it's the same user and channel
            return m.author == ctx.author and m.channel == ctx.channel

        try: # waiting for message
            response = await client.wait_for('message', check=check, timeout=30.0) # timeout - how long bot waits for message (in seconds)
        except asyncio.TimeoutError: # returning after timeout
            await ctx.send("Error: Timeout")
            return

        if response.content.lower() not in ("yes", "y"): # lower() makes everything lowercase to also catch: YeS, YES etc.
            return

        #fuction code
        os.remove("PartyDataBase\\" + file + ".txt")
        await ctx.send("The party " + file + " has been deleted")



@client.command(name="roll", aliases=["r"])
async def roll(ctx, arg1: str = "", arg2: str = "", arg3: str = ""): #Rolls a given number of die and adds given modifiers
    
    #Assign default values and initialize the final variables
    rollNum = "20"
    operator = "+0"
    qnt = 1
    finalStr=""
    num_final=0

    #Updates rollNum, operator and qnt
    if len(arg1) > 0:
        if (arg1[0] == "+" or arg1[0] == "-"):
            operator = arg1
        elif (arg1[0] == "d"):
            rollNum = int(arg1[1:])
        else:
            qnt = int(arg1)

    if len(arg2) > 0:
        if (arg2[0] == "+" or arg2[0] == "-"):
            operator = arg2
        elif (arg2[0] == "d"):
            rollNum = int(arg2[1:])
        else:
            qnt = int(arg2)

    if len(arg3) > 0:
        if (arg3[0] == "+" or arg3[0] == "-"):
            operator = arg3
        elif (arg3[0] == "d"):
            rollNum = int(arg3[1:])
        else:
            qnt = int(arg3)

    #roll the dice/die
    for i in range(qnt):
        rollValue = random.randint(1, int(rollNum))
        num_final += rollValue
        if i==0:
            finalStr += str(rollValue)
        else:
            finalStr += ' + ' + str(rollValue)

    # Add modifiers
    if (operator[0] == "+"):
        if (operator[1:] != "0"):
            num_final += int(operator[1:])
            finalStr += operator + " from modifiers"    
    else:
        num_final -= int(operator[1:])
        finalStr += " " + operator + " from modifiers"

    #Final string
    if qnt != 1 or operator != "+0":
        finalStr += " = " + str(max(num_final, 1))

    #Decide name to print
    if ctx.author.id in idList:
        name = ChrName(ctx.author.id)
    else:
        name = format(ctx.author.display_name)

    await ctx.send(name + (" rolled a " + finalStr))

@client.command()
async def coin(ctx): #Flips a coin
    n = random.randint(1,2)
    if n == 1:
        await ctx.send(format(ctx.author.display_name) + " rolled Heads")
    elif n == 2:
        await ctx.send(format(ctx.author.display_name) + " rolled Tails")

@client.command()
async def register(ctx, charName: str=""): #registers a new character and user
    #Check for errors
    if ctx.author.id in idList:
        await ctx.send("Error: User already has a character")
    elif charName in nameList:
        await ctx.send("Error: A Character with this names already exists")
    elif charName == "":
        await ctx.send("Error: you have to give a name to your character")
    
    else:
        #function code
        idList.append(ctx.author.id)
        nameList.append(charName)
        await ctx.send(format(ctx.author.display_name) + " registered the character " + charName)

@client.command()
async def delete(ctx): #Deletes the authors current character
    
    #Check for errors
    if nameList == []:
        await ctx.send("Error: There are no characters")
    elif ctx.author.id not in idList:
        await ctx.send("Error: User already has no character")
    
    else:
        #function code
        id = idList.index(ctx.author.id)
        charName = nameList[id]
        idList.remove(ctx.author.id)
        nameList.remove(charName)
        await ctx.send(format(ctx.author.display_name) + " deleted the character " + charName)

@client.command()
async def charlist(ctx): #Print all currently loaded characters
    
    #initialize final string
    finalStr = ""
    
    #Check for Errors
    if nameList == []:
        await ctx.send("Error: There are no characters")

    else:
        #function code
        for n in range (len(idList)):
            finalStr += IdToName(idList[n]) + ": " + nameList[n] + '\n'
        await ctx.send(finalStr)

@client.command()
async def dontusethisone(ctx): #just dont
    await ctx.send("https://tenor.com/view/dragon-dance-memw-dragon-dance-meme-dragon-meme-dance-gif-3939304025067010268")

@client.command()
async def h(ctx): #print a list of commands
    await ctx.send("hello, bye, loadparty, saveparty, checkparty, partylist, clearparty, deleteparty, roll, coin, register, delete, charlist, play, pause, resume, skip, queue, clear, stop, remove, dontusethisone")


async def main():
    await client.add_cog(music_cog(client))
    await client.start(variables.token)

asyncio.run(main())
