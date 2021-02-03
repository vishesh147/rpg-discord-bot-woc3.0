import csv
import os
import string


class player:
    def __init__(self, id, _class, _diff):
        self.id = id
        self.HP = 100
        self.XP = 0
        self.difficulty = _diff
        self.class_ = _class

    def editHP(self):
        s_HP = input("\nEnter new value to increase HP by : ")
        if s_HP.isdigit() or (s_HP[0]=='-' and s_HP[1:].isdigit()):
            HP = int(s_HP)
        else :
            print("\nERROR : Invalid Value (Enter integral value)")
            return self.editHP()
        self.HP += HP
        if(self.HP>=100):
            self.HP = 100
            print("Attribute set to max value = 100")
        elif(self.HP<=0):
            self.HP = 0
            print("Attribut set to min value = 0")
        else :
            print("Attribute Successfully Changed") 

    def editXP(self):
        s_XP = input("\nEnter new value to increase XP by : ")
        if s_XP.isdigit() or (s_XP[0]=='-' and s_XP[1:].isdigit()):
            XP = int(s_XP)
        else :
            print("\nERROR : Invalid Value (Enter integral value)")
            return self.editXP()
        self.XP += XP
        if(self.XP>=1000000):
            self.XP = 1000000
            print("Attribute set to max value = 1000000")
        elif(self.XP<=0):
            self.XP = 0
            print("Attribute set to min value = 0")
        else :
            print("Attribute Successfully Changed") 

    def editclass(self):
        d_class = {1 : 'Ninja', 2 : 'Samurai', 3 : 'Barbarian'}
        clas = input("\nSelect Class :\n1. Ninja\n2. Samurai\n3. Barbarian\n")
        if (clas in ['1', '2', '3']):
            self.class_ = d_class[int(clas)]
            print("Class Successfully Changed") 
        else:
            print("\nERROR : Invalid Index")
            return self.editclass()

    def editdiff(self):
        diffs = {'E' : 'Easy', 'N' : 'Normal', 'H' : 'Hard'}
        diff = input("\nSelect Difficulty :\nE = Easy\nN = Normal\nH = Hard\n")
        if(diff in ['E', 'e', 'N', 'n', 'H', 'h']):
            self.difficulty = diffs[diff.upper()]
            print("Difficulty Successfully Changed")   
        else:
            print("\nERROR : Invalid Index")
            return self.editdiff()

    def stats(self):
        print(f"\nPlayer ID : {self.id}\nPlayer HP : {self.HP}\nPlayer XP : {self.XP}\nPlayer Class : {self.class_}\nDifficulty : {self.difficulty}\n")





def input_class():
    dict_class = {1 : 'Ninja', 2 : 'Samurai', 3 : 'Barbarian'}
    print("\nPlease Select Class :\n1. Ninja\n2. Samurai\n3. Barbarian\n")
    c = input()
    if c in ['1', '2', '3']:    
        return dict_class[int(c)]
    else:
        print("\nERROR : Invalid Index")
        return input_class()

def input_diff():
    dict_diff = {'E' : 'Easy', 'N' : 'Normal', 'H' : 'Hard'}
    print("\nPlease Select Difficulty Level:\nE = Easy\nN = Normal\nH = Hard\n")
    d = input()
    if d in ['E', 'e', 'N', 'n', 'H', 'h']:
        return dict_diff[d.upper()]
    else:
        print("\nERROR : Invalid Index")
        return input_diff()



check_player=0
p_id = input("Enter Player ID : ")
with open('playerdata.csv', 'a') as new:
    with open('playerdata.csv' , 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for line in csv_reader:
            if (line['player-id']==p_id):           
                gamer = player(line['player-id'], line['player-class'], line['difficulty'])
                gamer.HP = int(line['HP'])
                gamer.XP = int(line['XP'])
                check_player = 1            
            
if (check_player==0):            
    gamer = player(p_id, input_class(), input_diff())

switch = { 1 : 'gamer.editHP()', 2 : 'gamer.editXP()', 5 : 'gamer.stats()', 3 : 'gamer.editdiff()', 4 : 'gamer.editclass()'}
while(1):
    print("\nPlease Enter Index From Menu :\n1. Change HP\n2. Change XP\n3. Change Difficulty\n4. Change Character Class\n5. Get Current Stats\n6. Exit")
    s_key = input()
    if s_key.isdigit():
        key=int(s_key)
    else:
        print("ERROR : Invalid Index Value")
        continue
    if key==6:
        break
    elif((key<1) or (key>6)):
        print("ERROR : Invalid Index Value")
        continue
    else:
        eval(switch[key])


check_record=0
data = {'player-id': str(p_id), 'HP': int(gamer.HP), 'XP': int(gamer.XP), 'player-class':str(gamer.class_), 'difficulty' : str(gamer.difficulty)}
with open('playerdata.csv' , 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    with open('new.csv', 'w', newline='') as new_file:
        fields = ['player-id', 'HP', 'XP', 'player-class', 'difficulty']
        csv_writer = csv.DictWriter(new_file, fieldnames = fields, delimiter=',')
        csv_writer.writeheader()
        for line in csv_reader:
            if (line['player-id']==p_id):  
                csv_writer.writerow(data)
                check_record = 1
            else:
                csv_writer.writerow(line)         
        if (check_record==0) :
            csv_writer.writerow(data)

os.remove("playerdata.csv")
os.rename('new.csv', 'playerdata.csv')

#-visheshpatel