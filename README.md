# DnD_Bot


## A discord bot to help when playing DnD over voice call among other things

This project is a bot for discord with the main focus of helping stream line the process of playing with your friends over voice call. It can help with dice rolls, identifying the members of the party and more. It also has functionality to work as a music bot and even play roulette over discord messages.

## Commands:

* **hello:** greets the server
* **bye:** says goodbye
* **loadparty:** loads a party from a .txt file in the PartyDataBase directory
* **saveparty:** saves the currently loaded party unto a .txt file, with a name given by the user, in the PartyDataBase directory
* **checkparty:** names all the characters in a given .txt file in the PartyDataBase directory
* **partylist:** names all the currently saved parties
* **clearparty:** deletes all characters from the currently loaded party
* **deleteparty:** deleetes a given party saved as a .txt in the PartyDataBase directory
* **roll:** roll a given number of die (the players chooses how many sides the die have) and adds any given modifiers
* **coin:** flips a coin
* **register:** register the users character on the currently loaded party
* **delete:** delete the users current character
* **charlist:** names every character in the currently loaded party
* **play:** plays a song or adds it to the queue
* **pause:** pauses the current song
* **resume:** resumes the current song
* **skip:** skips the current song
* **queue:** lists all the songs currently queued
* **clear:** removes all songs currently queued
* **stop:** disconnects the bot from the voice channel
* **remove:** removes the last song added to the queue
* **buyin:** add to your wallet
* **bet:** bet on the next spin
* **spin:** time to spin
* **dontusethisone:** a surprise!

## Cogs:

Other than the main.py file that contains all the bots main logic as well as the code for the DnD commands there are also 2 cog files:
* **music_cog:** this allows you to play songs on voice calls as well as basic commands such as queue, stop, etc.
* **roulette_cog:** this allows people in the server to play roullete (with pretend money of course).

## Getting the bot running

To use this bot on your own discord server you'll have to firtly download the code to an apropriate directory on yur pc. Then set up the bot on your discord server like you would with any other bot. All thats left to do is run the bot from your machine, you'll see a print on your terminal that indicates everything is working, once in the server use "**!**" to input commands. Now use the bot to your heart's content!