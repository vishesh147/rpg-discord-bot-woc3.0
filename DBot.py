import os
import csv
import discord
import random
from discord.ext import commands


class player:
    def __init__(self, id, hp, xp, weapon, ghp):
        self.id = id
        self.HP = hp
        self.XP = xp
        self.weapon = weapon
        self.gHP = ghp
        self.stats = (f"\nPlayer ID : {self.id}\nPlayer HP : {self.HP}\nPlayer XP : {self.XP}\nPlayer Weapon : {self.weapon}\n")

    def editHP(self, hp):
        self.HP += hp
        if(self.HP>=100):
            self.HP = 100
        elif(self.HP<=0):
            self.HP = 0
    def editXP(self, xp):
        self.XP += xp
        if(self.XP>=1000000):
            self.XP = 1000000
        elif(self.XP<=0):
            self.XP = 0

    def editgHP(self, ghp):
        self.gHP -= ghp
        if(self.gHP>=100):
            self.gHP = 100
        elif(self.gHP<=0):
            self.gHP = 0        


attacks = {40 : "You hit the goblin on the head.", 5 : "The goblin defended the attack.", 20 : "You slashed the goblin's gut.", -10 : "The goblin counter-attacked. You were hit on your leg."}         
defence = {5 : "The goblin was stunned by your defense.", 20 : "The goblin attacked your chest. You counter-attacked successfully", -30 : "The goblin attacked quickly. Defense was unsuccessful."}    
check_player = 0
xpcounter = 0

def checkplayer(pid):
    global check_player
    with open('playerdata.csv', 'a') as new:
        with open('playerdata.csv' , 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for line in csv_reader:
                if (line['Player-ID'] == str(pid)): 
                    check_player = check_player + 1        
                    return  player(line['Player-ID'], int(line['HP']), int(line['XP']), line['Player-Weapon'], int(line['Goblin-HP']))
                    

client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("Bot is Ready")

@client.command(name='reg')
async def register(ctx):
    gamer = checkplayer(ctx.author)
    def checkweapon(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and (msg.content.lower() in ["sword", "club", "nunchuks"])
    if check_player == 0:
        await ctx.send(f'Please Enter Weapon :\n1. Sword\n2. Club\n3. Nunchuks\n')
        msg = await client.wait_for('message', check=checkweapon)
        weapon = msg.content[0].upper() + msg.content[1:].lower()
        with open('playerdata.csv', 'a') as csv_reg:
            newreg = {'Player-ID' : str(ctx.author), 'HP' : 100, 'XP' : 0, 'Player-Weapon': weapon, 'Goblin-HP': 100}
            fields = ['Player-ID', 'HP', 'XP', 'Player-Weapon', 'Goblin-HP']
            csv_append = csv.DictWriter(csv_reg , fieldnames = fields, delimiter = ',')
            csv_append.writeheader()
            csv_append.writerow(newreg)
        await ctx.send(f'*Registered Successfully*')
    else :
        await ctx.send(f'*Player already Registered. You can play the game.*')

@client.command()
async def stats(ctx):
    gamer = checkplayer(ctx.author)
    if check_player == 0:     
        await ctx.send(f'*No user stats found. Register yourself to create a profile.*')
    else :
        await ctx.send(gamer.stats)

@client.command()
async def play(ctx):
    global check_player

    def checkmove(move):
        return move.author == ctx.author and move.channel == ctx.channel 

    gamer = checkplayer(ctx.author)
    if check_player == 0 :
        await ctx.send(f'*Please register before playing.*')
    
    else :    
        await ctx.send(f'\nLet the game begin!\n*Write "exit" to stop.*\n')
        while(1):
            global xpcounter
            xpcounter+=5
            await ctx.channel.send(f'Enter your move :\nAttack\nDefend')
            move = await client.wait_for('message', check=checkmove)
            if move.content.lower()=='attack':
                hp = random.choice(list(attacks.keys()))
                resp = attacks[hp]
            elif move.content.lower()=='defend':
                hp = random.choice(list(defence.keys()))
                resp = defence[hp]
            elif move.content.lower()=='exit':
                gamer.editXP(xpcounter)
                await ctx.send(f'*See you later. Bye!* ;)')
                break
            else :
                await ctx.channel.send(f'*Invalid Move*')
                continue
            if hp < 0 :
                gamer.editHP(hp)
            else :
                gamer.editgHP(hp)
            await ctx.channel.send(f'{resp}')
            await ctx.channel.send(f"Your HP : {gamer.HP}\nGoblin's HP : {gamer.gHP}\n")
            if gamer.gHP == 0:
                await ctx.channel.send(f'\n*YOU WON!* :)\n*Game Over*\n*Attributes Reset. Enter "!play" to play again.*')
                gamer.gHP = 100
                gamer.HP = 100
                gamer.editXP(xpcounter+100)
                break
            elif gamer.HP == 0:
                await ctx.channel.send(f'\n*YOU LOST!* :(\n*Game Over*\n*Attributes Reset. Enter "!play" to try again.*')
                gamer.gHP = 100
                gamer.HP = 100
                gamer.editXP(xpcounter+25)
                break
            
        check_record=0
        data = {'Player-ID': str(ctx.author), 'HP': int(gamer.HP), 'XP': int(gamer.XP), 'Player-Weapon' : str(gamer.weapon), 'Goblin-HP' : int(gamer.gHP)}
        with open('playerdata.csv' , 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            with open('new.csv', 'w', newline='') as new_file:
                fields = ['Player-ID', 'HP', 'XP', 'Player-Weapon', 'Goblin-HP']
                csv_writer = csv.DictWriter(new_file, fieldnames = fields, delimiter=',')
                csv_writer.writeheader()
                for line in csv_reader:
                    if (line['Player-ID']==str(ctx.author)):  
                        csv_writer.writerow(data)
                        check_record = 1
                    else:
                        csv_writer.writerow(line)         
                if (check_record==0) :
                    csv_writer.writerow(data)

        os.remove("playerdata.csv")
        os.rename('new.csv', 'playerdata.csv')

client.run("")