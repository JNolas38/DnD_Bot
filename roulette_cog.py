from ast import alias
import discord
from discord.ext import commands
import asyncio
import random


class roulette_cog (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.playerlist = []
        self.wallets = []
        self.table = []
        self.bets = []


    @commands.command(name="buyin", aliases=["buy", "bi"], help="Adds an amount to your wallet")
    async def buyin(self, ctx, amount: int):

        if ctx.author.id not in self.playerlist:
            self.playerlist.append(ctx.author.id)
            self.wallets.append(amount)
            self.bets.append(0)
            self.table.append('')
            await ctx.send("Welcome, you now have " + str(amount) + " in your wallet!")
        else:
            for n in range (len(self.playerlist)):
                if self.playerlist[n] == ctx.author.id:
                    self.wallets[n] += amount
                    await ctx.send("You added " + str(amount) + " to your wallet! You now have " + str(self.wallets[n]))

    @commands.command (name="bet", aliases = ["placebet"], help="Place a bet for the next spin")
    async def bet(self, ctx, amount: int, guess: str = ''):

        if ctx.author.id not in self.playerlist:
            await ctx.send ("Error: You must first make a buy in before plassing a bet!")
            return
        for m in range (len(self.playerlist)):
            if self.playerlist[m] == ctx.author.id:
                if self.wallets[m] < amount:
                    await ctx.send("Error: You tried to bet " + str(amount) + " but only have " + str(self.wallets[m]) + " in your wallet")
                    return


        for n in range(len(self.playerlist)):
            if self.playerlist[n] == ctx.author.id:
                
                if self.bets[n] == 0:
                    self.bets[n] += amount
                    self.wallets[n] -= amount
                    self.table[n] = guess
                    await ctx.send("You have bet " + str(amount) + " on " + guess + " for the next spin")
                 
                else:
                    await ctx.send("You already have a bet in place for the next spin! Are you sure you want to bet more? (y/n)")
                    def check(m): # checking if it's the same user and channel
                        return m.author == ctx.author and m.channel == ctx.channel
                    try: # waiting for message
                        response = await self.bot.wait_for('message', check=check, timeout=30.0) # timeout - how long bot waits for message (in seconds)               
                    except asyncio.TimeoutError: # returning after timeout
                        await ctx.send("Error: Timeout")
                        return

                    if response.content.lower() not in ("yes", "y"): # lower() makes everything lowercase to also catch: YeS, YES etc.
                        return

                    self.bets[n] += amount
                    self.wallets[n] -= amount
                    
                    if self.table[n] != guess and guess != '':
                        await ctx.send("You are betting on a different guess, do you wish to change your guess? (y/n)")
                        def check(m): # checking if it's the same user and channel
                            return m.author == ctx.author and m.channel == ctx.channel
                        try: # waiting for message
                            response = await self.bot.wait_for('message', check=check, timeout=30.0) # timeout - how long bot waits for message (in seconds)               
                        except asyncio.TimeoutError: # returning after timeout
                            await ctx.send("Error: Timeout")
                            return

                        if response.content.lower() not in ("yes", "y"): # lower() makes everything lowercase to also catch: YeS, YES etc.
                            await ctx.send("You added " + str(amount) + " to your bet on " + guess + "! You now have " +str(self.bets[n]))
                            return
                    
                    self.table[n] = guess
                    await ctx.send("You added " + str(amount) + " to your bet on " + guess + "! You now have " +str(self.bets[n]))
    
    @commands.command (name="spin", aliases = ["spinaroni"], help="Time to spin!")
    async def spin(self, ctx):
        await ctx.send("Spinning...")
        await asyncio.sleep(1)
        await ctx.send("Spinning...")
        await asyncio.sleep(1)
        await ctx.send("Spinning...")
        await asyncio.sleep(1)

        spin = random.randrange(0, 36)
        await ctx.send (str(spin))


        if spin != 0:
            if spin % 2 == 0:
                pair = 'even'
            else:
                pair = 'odd'

        #process the spin
        for n in range(len(self.playerlist)):
            if self.table[n] != '':
                win = True
                user = self.bot.get_user(self.playerlist[n])
                
                #single number
                if self.table[n] == str(spin):
                    pot = self.bets[n] * 35
                    
                #even and odd
                elif self.table[n] == pair:
                    pot = self.bets[n]

                #loss
                else:
                    pot = 0
                    win = False
                    
                #reset the bet
                self.bets[n] = 0
                self.wallets[n] += pot
                self.table[n] = ''
                
                #message the winners and losers
                if win:
                    await ctx.send("Congratulations! you won " + str(pot) + " and now have " + str(self.wallets[n]) + " on your wallet!")
                else: 
                    await ctx.send("You lost " + format(user.display_name) + "! Remember 99 in 100 gamblers quit right before winning a jackpot!")



    @commands.command (name="checkwallet", aliases = ["checkw", "cw"], help="Check your current wallet")
    async def checkwallet(self, ctx):
        if ctx.author.id not in self.playerlist:
            await ctx.send("Error: you don't currently have a wallet")
        else:
            for n in range (len(self.playerlist)):
                if ctx.author.id == self.playerlist[n]:
                    await ctx.send("You currently have " + str(self.wallets[n]) + " in your wallet")

    @commands.command (name="checkbet", aliases = ["checkb", "cb"], help="Check your bet for the next spin")
    async def checkbet(self, ctx):
        if ctx.author.id not in self.playerlist:
            await ctx.send("Error: you don't currently have a wallet")
        else:
            for n in range (len(self.playerlist)):
                if ctx.author.id == self.playerlist[n]:
                    if self.bets[n] == 0:
                        await ctx.send("You currently dont have a bet on the next spin")
                    else:
                        await ctx.send("You currently have " + str(self.bets[n]) + " bet on " + self.table[n] + " for the next spin")

async def setup(bot):
    await bot.add_cog(roulette_cog(bot))