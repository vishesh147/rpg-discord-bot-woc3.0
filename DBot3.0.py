import os
import requests
import pymysql
import discord
import random
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from variables import *

class player:
    def __init__(self, id, hp, xp, weapon, ghp, spells, level):
        self.id = id
        self.HP = hp
        self.XP = xp
        self.weapon = weapon
        self.gHP = ghp
        self.spells = spells
        self.level = level
        self.stats = (f"\n**Player ID :** {self.id}\n**Player HP :** {self.HP}\n**Player XP :** {self.XP}\n**Player Weapon : **{self.weapon}\n**Available HP Spells :** {self.spells}\n**Player Level :** {self.level}\n")

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

duel_defence = {5 : "The opponent was stunned by your defense.", 20 : "Opponent attacked your chest. You counter-attacked successfully", -30 : "The opponent attacked quickly. Defense was unsuccessful."}
duel_attacks = {40 : "You hit the opponent on the head.", 5 : "The opponent defended the attack.", 20 : "You slashed the opponent's gut.", -10 : "Oppenent counter-attacked. You were hit on your thigh."}
spells = {100 : "Heal Spell successful. You were fully healed.", 10 : "Spell used. HP increased slightly.", 30 : "Spell successful. HP increased", -25 : "Spell backfired. You were injured badly."}
attacks = {1 : {30 : "You hit the goblin on the head.", 5 : "The goblin defended the attack.", 20 : "You slashed the goblin's gut.", -10 : "The goblin counter-attacked. You were hit on your leg."}
        , 2: {30 : "You hit the Witch on the head.", 5 : "The Witch defended the attack.", 15 : "You slashed the witch's gut.", -10 : "The Witch counter-attacked. You were hit on your leg.", -20 : "The Witch played a spell. You attacked yourself."} 
        , 3: {30 : "You hit the dragon on the head.", 5 : "The dragon defended the attack.", 20 : "You slashed the dragon's tail.", -10 : "The dragon counter-attacked. You were hit on your leg.", -30 : "Attack failed. The Dragon spat fire on you.", -5 : "You were stunned by the dragon's defense."}}         
defence = {1 : {5 : "The goblin was stunned by your defense.", 20 : "The goblin attacked your chest. You counter-attacked successfully", -30 : "The goblin attacked quickly. Defense was unsuccessful."}    
        , 2 : {5 : "The Witch was stunned by your defense.", 20 : "The Witch attacked your chest. You counter-attacked successfully", -30 : "The Witch attacked quickly. Defense was unsuccessful."}
        , 3 : {5 : "The dragon was stunned by your defense.", 20 : "The Dragon attacked your chest. You counter-attacked successfully", -30 : "The dragon attacked quickly. Defense was unsuccessful."}}
spellcounter = 0
xpcounter = 0

def checkplayer(pid):
    user = 0
    checker = 1
    db = pymysql.connect(host="localhost", user="vishesh147", password=mysqlpass, database="playerdata")
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS rpgbotdata(PlayerID varchar(255), HP int, XP int, PlayerWeapon varchar(255), GoblinHP int, Spells int, Level int);')
    try:    
        cursor.execute("SELECT * FROM rpgbotdata WHERE PlayerID = '"+ str(pid) + "';")
        data = list(cursor.fetchone())
        user = player(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
    except:
        checker = 0
    db.close()
    return user, checker
                       
client = commands.Bot(command_prefix = "#")
client.remove_command('help')

@client.event
async def on_ready():
    print("Bot is Ready")

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.blue())
    embed.set_author(name='RPG Bot')
    embed.add_field(name ='Help', value= """**#reg** : Register User to Game Database\n**#play** : Play Solo Adventure Mode\n**#playduel <opponent-id>** : Play duel with another registered player
    **#stats** : Check your stats\n**#dailygift** : Collect daily gift of HP spells ; Works only once a day\n**#buyspells <amount>** : Buy HP spells using XP ; 100XP per spell""")
    await ctx.send(embed=embed)

@client.command(name='reg')
async def register(ctx):
    gamer, check_player = checkplayer(ctx.author)
    def checkweapon(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and (msg.content.lower() in ["sword", "club", "nunchuks"])
    if check_player == 0:
        await ctx.send(f'**Please Enter Weapon :**\n1. Sword\n2. Club\n3. Nunchuks\n')
        msg = await client.wait_for('message', check=checkweapon)
        weapon = msg.content[0].upper() + msg.content[1:].lower()
        db = pymysql.connect(host="localhost", user="vishesh147", password="vishesh147", database="playerdata")
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO rpgbotdata VALUES('" + str(ctx.author) + "', 100, 0, '"+ str(weapon) + "', 100, 0, 1);")
            db.commit()
            await ctx.send(f'*Player Registered Successfully.*')
        except:
            await ctx.send(f'*Some Error Occured. Try Again.*')
    else :
        await ctx.send(f'*Player already Registered. You can play the game.*')
        await ctx.send(f'https://media2.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif')

@client.command()
async def stats(ctx):
    gamer, check_player = checkplayer(str(ctx.author))
    if check_player == 0:     
        await ctx.send(f'*No user stats found. Register yourself to create a profile.*')
        await ctx.send(f'https://media0.giphy.com/media/13n7XeyIXEIrbG/giphy.gif?cid=ecf05e478s6blt3p9yoynbhrwjacpekajyeqfsh3xc0o4rz2&rid=giphy.gif')
    else :
        await ctx.send(gamer.stats)

@client.command()
async def buyspells(ctx, count):
    gamer, check_player = checkplayer(str(ctx.author))
    if check_player == 0:
        await ctx.send(f'*No user found. Register yourself to access shop.*')
        await ctx.send(f'https://media0.giphy.com/media/13n7XeyIXEIrbG/giphy.gif?cid=ecf05e478s6blt3p9yoynbhrwjacpekajyeqfsh3xc0o4rz2&rid=giphy.gif')
    else:
        gamer.XP -= (int(count)*100)
        if gamer.XP < 0:
            await ctx.send(f'*Not enough XP. Play to earn more XP!*')
            await ctx.send(f'https://media1.giphy.com/media/Km2YiI2mzRKgw/giphy.gif')
            gamer.XP += (100*int(count))
        else:
            gamer.spells += int(count)
            db = pymysql.connect(host="localhost", user="vishesh147", password="vishesh147", database="playerdata")
            cursor = db.cursor()
            cursor.execute("UPDATE rpgbotdata SET XP="+str(gamer.XP)+", Spells="+str(gamer.spells)+" WHERE PlayerID = '"+str(ctx.author)+"';" )
            db.commit()
            db.close()     
            await ctx.send(f'{count} spells added successfully!')  

@client.command()
@commands.cooldown(1, 24*60*60, commands.BucketType.user)
async def dailygift(ctx):
    gamer, check_player = checkplayer(str(ctx.author))
    if check_player == 0:
        await ctx.send(f'*No user found. Duh! Register yourself first.*')
        await ctx.send(f'https://media0.giphy.com/media/13n7XeyIXEIrbG/giphy.gif?cid=ecf05e478s6blt3p9yoynbhrwjacpekajyeqfsh3xc0o4rz2&rid=giphy.gif')
    else:
        db = pymysql.connect(host='localhost', user='vishesh147', password='vishesh147', database='playerdata')
        cursor = db.cursor()
        cursor.execute("UPDATE rpgbotdata SET Spells = Spells + 3 WHERE PlayerID = '"+str(ctx.author)+"';")
        db.commit()
        db.close()
        await ctx.send(f'Your daily gift of 3 Spells has been collected!')
        await ctx.send(f'https://media1.tenor.com/images/56ec826d775530725e6fa1a92ec1822a/tenor.gif')
        await ctx.send(f'*Come back tomorrow to collect again* :wink:')
        

@client.command()
async def playduel(ctx, opponent):
   
    def checkplayermove(pmove):
        return pmove.author == ctx.author and pmove.channel == ctx.channel

    def checkoppmove(omove):
        return str(omove.author) == opponent and omove.channel == ctx.channel

    duelcounter=0
    gamer, check_player = checkplayer(str(ctx.author))
    opp, check_opp = checkplayer(str(opponent))
    if check_player == 0:     
        await ctx.send(f'*No user stats found. Register yourself to play duels*')
    elif check_opp == 0:
        await ctx.send(f'*Opponent is not registered. Choose another opponent.*')
    else:
        await ctx.send(f'*Duels are not saved. Players will start with 100HP and XP will not be rewarded.*\nLet the duel begin!\n*Write "exit" to stop.*\n')
        gamer.HP = 100
        opp.HP = 100
        while(1):
            duelcounter+=1
            if (duelcounter%2==0):
                await ctx.send(f'{opponent}, Enter move :\nAttack\nDefend')
                omove = await client.wait_for('message', check=checkoppmove)
                if omove.content.lower()=='attack':
                    hp = random.choice(list(duel_attacks.keys()))
                    resp = duel_attacks[hp]
                    if hp < 0 :
                        opp.editHP(hp)
                    else :
                        gamer.editHP(-hp)
                elif omove.content.lower()=='defend':
                    hp = random.choice(list(duel_defence.keys()))
                    resp = duel_defence[hp]
                    if hp < 0 :
                        opp.editHP(hp)
                    else :
                        gamer.editHP(-hp)
                elif omove.content.lower()=='exit':
                    await ctx.send(f'*See you later. Bye!*\n:wink:')
                    break
            else:
                await ctx.send(f'{ctx.author}, Enter move :\nAttack\nDefend')
                pmove = await client.wait_for('message', check=checkplayermove)
                if pmove.content.lower()=='attack':
                    hp = random.choice(list(duel_attacks.keys()))
                    resp = duel_attacks[hp]
                    if hp < 0 :
                        gamer.editHP(hp)
                    else :
                        opp.editHP(-hp)
                elif pmove.content.lower()=='defend':
                    hp = random.choice(list(duel_defence.keys()))
                    resp = duel_defence[hp]
                    if hp < 0 :
                        gamer.editHP(hp)
                    else :
                        opp.editHP(-hp)
                elif pmove.content.lower()=='exit':
                    await ctx.send(f'*See you later. Bye!*\n:wink:')
                    break
            await ctx.channel.send(f'{resp}')
            await ctx.channel.send(f"{ctx.author}'s HP : {gamer.HP}\n{opponent}'s HP : {opp.HP}\n")
            if opp.HP == 0:
                await ctx.channel.send(f'\n{ctx.author} ***WON!*** \n:champagne_glass:\n*Game Over*')
                break
            elif gamer.HP == 0:
                await ctx.channel.send(f'\n{opponent} ***WON!*** \n:champagne_glass:\n*Game Over*')
                break

@client.command()
async def play(ctx):

    def checkmove(move):
        return move.author == ctx.author and move.channel == ctx.channel 

    gamer, check_player = checkplayer(ctx.author)
    if check_player == 0 :
        await ctx.send(f'*Player NOT Eegistered. Enter "!reg" to register before playing.*')
        await ctx.send(f'https://media0.giphy.com/media/13n7XeyIXEIrbG/giphy.gif?cid=ecf05e478s6blt3p9yoynbhrwjacpekajyeqfsh3xc0o4rz2&rid=giphy.gif')
    else :    
        await ctx.send(f'\nLet the game begin!\n*Write "exit" to stop.*\n')
        while(1):
            global spellcounter
            global xpcounter
            spellcounter+=1
            xpcounter+=5
            if (spellcounter%3==0):
                await ctx.channel.send(f'Enter your move :\nAttack\nDefend\nUse Spell : {gamer.spells}')
            else :  
                await ctx.channel.send(f'Enter your move :\nAttack\nDefend')
            move = await client.wait_for('message', check=checkmove)
            if move.content.lower()=='attack':
                hp = random.choice(list(attacks[gamer.level].keys()))
                resp = attacks[gamer.level][hp]
                if hp < 0 :
                    gamer.editHP(hp)
                else :
                    gamer.editgHP(hp)
            elif move.content.lower()=='defend':
                hp = random.choice(list(defence[gamer.level].keys()))
                resp = defence[gamer.level][hp]
                if hp < 0 :
                    gamer.editHP(hp)
                else :
                    gamer.editgHP(hp)
            elif move.content.lower()=='exit':
                gamer.editXP(xpcounter)
                await ctx.send(f'\n*See you later. Bye!*')
                await ctx.send(f':wink:')
                break
            elif (move.content.lower()=='use spell' and spellcounter%3==0):
                if (gamer.spells>0):
                    gamer.spells-=1
                    hp = random.choice(list(spells.keys()))
                    resp = spells[hp]
                    gamer.editHP(hp)
                else :
                    await ctx.send(f"*Not enough spells. Please buy more from the shop!*")     
                    spellcounter-=1
                    continue           
            else :
                await ctx.channel.send(f'\n*Invalid Move*')
                spellcounter-=1
                continue

            await ctx.channel.send(f'{resp}')
            enemy = {1 : 'Goblin', 2 : 'Witch', 3 : 'Dragon'}
            await ctx.channel.send(f"Your HP : {gamer.HP}\n{enemy[gamer.level]}'s HP : {gamer.gHP}\n")
            if gamer.gHP == 0:
                gamer.level += 1
                if gamer.level == 4:
                    await ctx.channel.send(f'\n***YOU WON!*** :partying_face:\n*Game Over*\n*Attributes Reset. Enter "#play" to play again.*')
                    await ctx.channel.send(f'https://i.giphy.com/media/g9582DNuQppxC/giphy-downsized.gif')
                    gamer.gHP = 100
                    gamer.HP = 100
                    gamer.editXP(xpcounter+500)
                    gamer.level=1
                    break
                else:
                    await ctx.send(f'\n***LEVEL COMPLETED!*** :partying_face:\n*You proceed to level {gamer.level}. HP regenerated to 100.\nEnter "#play" to play level 2.*')
                    img = Image.open(requests.get("https://images.fineartamerica.com/images/artworkimages/mediumlarge/3/mission-passed-respect-gta-yarchy.jpg", stream=True).raw)
                    img = img.crop((100, 100, 800, 550))    
                    i = ImageDraw.Draw(img)
                    f = ImageFont.truetype("impact.ttf", 30)
                    i.text((280, 400), "*LEVEL UP!*", font=f ,fill =(255, 255, 255))
                    img = img.save("levelup.jpg")
                    await ctx.send(file=discord.File('levelup.jpg'))
                    os.remove('levelup.jpg')
                    gamer.HP = 100
                    gamer.gHP = 100
                    gamer.editXP(xpcounter+100)
                    break
            elif gamer.HP == 0:
                await ctx.channel.send(f'\n***YOU LOST!*** :skull_crossbones:\n*Game Over*\n*Attributes Reset. Enter "#play" to try again.*')
                await ctx.channel.send(f'https://media0.giphy.com/media/j6ZlX8ghxNFRknObVk/giphy.gif?cid=ecf05e477238bae8b9e040a7ad793bbee16a8d49b0f31331&rid=giphy.gif')
                gamer.gHP = 100
                gamer.HP = 100
                gamer.editXP(xpcounter+25)
                break
            
        db = pymysql.connect(host="localhost", user="vishesh147", password="vishesh147", database="playerdata")
        cursor = db.cursor()
        cursor.execute("UPDATE rpgbotdata SET HP="+str(gamer.HP)+", XP="+str(gamer.XP)+", GoblinHP="+str(gamer.gHP)+", Spells="+str(gamer.spells)+", Level="+str(gamer.level)+" WHERE PlayerID = '"+str(ctx.author)+"';" )
        db.commit()
        db.close()
  
client.run(bot_token)
