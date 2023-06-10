from flask import Flask, request, render_template
#import string
from random import choice, randint




app = Flask(__name__)




class Character(object):
    def __init__(self, **kwargs):
        self.player_name = kwargs.get("player", '')

        self.gender = kwargs.get("gender", 'random')
        if self.gender =='random':
            self.gender = choice(['M', 'F'])


        self.race = kwargs.get("race", 'random HIGH_FANTASY')
        if self.race.split(' ')[0] == 'random':
            self.race = self.random_race(self.race.split(' ')[1])
        self.subrace = 'NONE'
        if subraces.get(self.race):
            self.subrace = choice(subraces[self.race])
        
        random_name = kwargs.get("random_name", True)
        if random_name:
            self.character_name = self.random_name(self.race, self.gender)
        else:
            self.character_name = kwargs.get("character", '')


        (self.size, self.speed, extra_language, racial_bonuses, self.racial_abilities) = racial_traits[(self.race, self.subrace)]
        self.languages = ['Common'] + extra_language

        self.roll_stats(racial_bonuses)
        







        #POUKAYA
        self.roll_occupation()

        #POUKAYA
        self.compute_attacks()


        pass
    
    def random_race(self, context):
        alea = randint(1,100)
        table = races_table[context]

        for i in range(len(table)):
            if alea <= table[i][0]:
               race = table[i][1]
               break

        return race

    def random_name(self, race, gender):
        

        #POUKAYA
        return 'Poukaya'
    
    def roll_stats(self, racial_bonuses):
        stats = []

        for i in range(6):
            alea = [randint(1,6) for j in range(4)]
            alea.sort()
            alea.pop(0)
            stats.append(sum(alea))

        
        self.attributes = [sum(x) for x in zip(stats, racial_bonuses)]

        self.HP = randint(1,4) + self.modifier(self.attributes[2])
        if self.HP <= 0:
             self.HP = 1
        
        self.AC = 10 + self.modifier(self.attributes[1])
        self.initiative = self.modifier(self.attributes[1])

        pass


    
    def modifier(self, ability_score):
        return (ability_score//2)-5
    
    def roll_occupation(self):

        attrib_max = choice([i for i in range(6) if self.attributes[i] == max(self.attributes)])
        alea = randint(1,20) 

        (self.occupation, coins, self.proficiency, self.weapon, self.item, self.clothes) = occupations_table[(0, alea)]
        #POUKAYA Tirer les pièces et la trinket
        #POUKAYA Traiter les vêtements
        #POUKAYA Gérer les armes et armures




        self.gold = "2 gold pieces"
        self.atk = "+5"
        self.dmg = "1d6+2"
        self.weapon_attributes = "Light, Two-handed"
        self.prof_mod = "+12"
        self.trinket = "Five-leaf clover"


        pass
    
    def compute_attacks(self):
        pass
    
    
    def export(self):
        data = []


        data.append(self.character_name)
        data.append(self.player_name)
        data.append(self.gender)

        if self.subrace == 'NONE':
            data.append(self.race)
        else:
             data.append('{0} ({1})'.format(self.race, self.subrace))
        
        data.append(self.size)


        data.append(self.occupation)
        data.append(self.HP)
        data.append(self.AC)
        data.append(self.initiative)
        data.append(self.speed)


        for i in range(6):
            data.append(self.attributes[i])
            data.append(self.modifier(self.attributes[i]))

        data.append(self.proficiency)
        data.append('+2') #data.append(self.prof_mod)
        data.append(self.clothes)
        data.append(self.weapon)
        data.append(self.atk)
        data.append(self.dmg)
        data.append(self.weapon_attributes)


        data += self.racial_abilities
        data.append(self.item)
        data.append(self.trinket)
        data.append(self.gold)


        return data
    






races_table = {'HIGH_FANTASY' : [(20, 'Human'), (30, 'Halfling'),
                                 (40, 'Dwarf'), (50, 'Gnome'),
                                 (60, 'Tiefling'), (65, 'Goliath'),
                                 (75, 'Elf'), (85, 'Half-Orc'),
                                 (90, 'Aarakocra'), (100, 'Dragonborn')],
            'HUMAN_DOMINATED' : [(64, 'Human'), (69, 'Halfling'),
                                 (74, 'Dwarf'), (79, 'Gnome'),
                                 (85, 'Tiefling'), (90, 'Goliath'),
                                 (93, 'Elf'), (95, 'Half-Orc'),
                                 (97, 'Aarakocra'), (100, 'Dragonborn')]
               }


subraces = {'Halfling' : ['Lightfoot', 'Stout'],
            'Dwarf' : ['Hill', 'Mountain'],
            'Gnome' : ['Rock', 'Forest'],
            'Elf' : ['High', 'Wood'],
            'Dragonborn' : ['Red', 'Blue', 'Green', 'White', 'Black', 'Brass', 'Copper', 'Bronze', 'Silver', 'Gold']
            }



racial_traits = {#Size, Speed, Extra Language, Ability Bonuses, Racial abilities
    ('Human', 'NONE') : ['Medium', '30 ft', [], [1, 1, 1, 1, 1, 1], ['Inspiration', 'Focus']],
    ('Halfling', 'Lightfoot') : ['Small', '25 ft', ['Halfling'], [0, 2, 0, 0, 0, 1], ['Brave', 'Halfling Nimbleness']],
    ('Halfling', 'Stout') : ['Small', '25 ft', ['Halfling'], [0, 2, 1, 0, 0, 0], ['Brave', 'Halfling Nimbleness']],
    ('Dwarf', 'Hill') : ['Medium', '25 ft', ['Dwarvish'], [0, 0, 2, 0, 1, 0], ['Darkvision 60 ft', 'Dwarven Resilience']],
    ('Dwarf', 'Mountain') : ['Medium', '25 ft', ['Dwarvish'], [1, 0, 2, 0, 0, 0], ['Darkvision 60 ft', 'Dwarven Resilience']],
    ('Gnome', 'Rock') : ['Small', '25 ft', ['Gnomish'], [0, 0, 1, 2, 0, 0], ['Darkvision 60 ft', 'Gnome Cunning']],
    ('Gnome', 'Forest') : ['Small', '25 ft', ['Gnomish'], [0, 1, 0, 2, 0, 0], ['Darkvision 60 ft', 'Gnome Cunning']],
    ('Tiefling', 'NONE') : ['Medium', '30 ft', ['Infernal'], [0, 0, 0, 1, 0, 2], ['Darkvision 60 ft', 'Hellish Resistance']],
    ('Goliath', 'NONE') : ['Medium', '30 ft', ['Giant'], [2, 0, 1, 0, 0, 0], ["Stone's Endurance", 'Mountainborn']],
    ('Elf', 'High') : ['Medium', '30 ft', ['Elvish'], [0, 2, 0, 1, 0, 0], ['Darkvision 60 ft', 'Trance']],
    ('Elf', 'Wood') : ['Medium', '30 ft', ['Elvish'], [0, 2, 0, 0, 1, 0], ['Darkvision 60 ft', 'Trance']],
    ('Half-Orc', 'NONE') : ['Medium', '30 ft', ['Orcish'], [2, 0, 1, 0, 0, 0], ['Darkvision 60 ft', "Relentless Endurance"]],
    ('Aarakocra', 'NONE') : ['Medium', '25 ft', ['Aarakocra'], [0, 2, 0, 0, 1, 0], ['Flight', 'Talons']],
    ('Dragonborn', 'Red') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Fire)", 'Breath Weapon (cone)']],
    ('Dragonborn', 'Blue') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Lightning)", 'Breath Weapon (line)']],
    ('Dragonborn', 'Green') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Poison)", 'Breath Weapon (cone)']],
    ('Dragonborn', 'White') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Cold)", 'Breath Weapon (cone)']],
    ('Dragonborn', 'Black') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Acid)", 'Breath Weapon (line)']],
    ('Dragonborn', 'Brass') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Fire)", 'Breath Weapon (line)']],
    ('Dragonborn', 'Copper') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Acid)", 'Breath Weapon (line)']],
    ('Dragonborn', 'Bronze') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Lightning)", 'Breath Weapon (line)']],
    ('Dragonborn', 'Silver') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Cold)", 'Breath Weapon (cone)']],
    ('Dragonborn', 'Gold') : ['Medium', '30 ft', ['Draconic'], [2, 0, 0, 0, 0, 1], ["Damage Resistance (Fire)", 'Breath Weapon (cone)']],

}


occupations_table = {#(Attribute (0 to 5), Number (1 to 20)) -> Occupation, Coins, Proficiency, Weapon, Item, Clothes
    (0,1) : ["Blacksmith", (12, "s"), "Smith's tools", "Light hammer", "Smith's tools", "Common"],
    (0,2) : ["Miner", (20, "c"), "Investigation", "Handaxe", "Miner's pick", "Common"],
    (0,3) : ["Teamster", (8, "s"), "Strength saving throws", "Whip", "Block and tackle", "Common"],
    (0,4) : ["Bodyguard", (10, "g"), "Heavy armor", "Maul", "Ringmail", "Traveler's"],
    (0,5) : ["Plowman/woman", (10, "c"), "Nature", "Quarterstaff", "A bag of good soil", "Common"],
    (0,6) : ["Rough", (6, "s"), "Intimidation", "Club", "Leather armor", "Common"],
    (0,7) : ["Butcher", (20, "s"), "Handaxes", "Butcher knife (handaxe)", "5 pounds of jerky", "Common"],
    (0,8) : ["Gladiator", (12, "g"), "Simple weapons", "Net", "Chain shirt", "Traveler's"],
    (0,9) : ["Woodcutter", (6, "s"), "Nature", "Handaxe", "A tie of cut wood", "Common"],
    (0,10) : ["Carpenter", (6, "g"), "Carpenter's tools", "Light hammer", "Carpenter's tools", "Common"],
    (0,11) : ["Milkman/Milkmaid", (8, "s"), "Animal handling", "Club", "Metal bucket", "Common"],
    (0,12) : ["Executioner", (12, "s"), "Intimidation", "Greataxe", "Basket", "Common"],
    (0,13) : ["Mercenary", (12, "s"), "Simple weapons", "Short sword", "Leather armor", "Traveler's"],
    (0,14) : ["Bone carver", (6, "s"), "Woodcarver's tools", "Bone knife (dagger)", "3 large animal bones", "Common"],
    (0,15) : ["Mason", (10, "c"), "Mason's tools", "Light hammer", "Mason's tools", "Common"],
    (0,16) : ["Grinder", (8, "s"), "Animal handling", "Dagger", "Grinding stone", "Common"],
    (0,17) : ["Platner", (8, "s"), "Smith's tools", "Maul", "Sheet of metal", "Common"],
    (0,18) : ["Porter", (8, "c"), "Perception", "Broom (quarterstaff)", "Lye soap", "Common"],
    (0,19) : ["Jailer", (4, "s"), "Investigation", "Club", "A set of keys", "Common"],
    (0,20) : ["Wagoner", (12, "c"), "Land vehicles (wagon)", "Whip", "Wagon bolts", "Common"],
}



@app.route("/")
def hello():
    return render_template("accueil.html")





@app.route('/char-sheet', methods=['GET', 'POST'])
def create():
    player_name = request.args.get('player')
    character_name = request.args.get('character')
    gender = request.args.get('gender')
    race = request.args.get('race')
    random_name = request.args.get('random_name')

    character = Character(player = player_name, character = character_name, gender = gender, race = race, random_name = random_name)
    data = character.export()

    return render_template("sheet.html", character_name = data[0], player_name = data[1], gender = data[2], race = data[3],
                           size = data[4], occupation = data[5], HP = data[6], AC = data[7], Init = data[8], Spd = data[9],
                           STR = data[10], mod_STR = data[11], DEX = data[12], mod_DEX = data[13], CON = data[14], mod_CON = data[15],
                           INT = data[16], mod_INT = data[17], WIS = data[18], mod_WIS = data[19], CHA = data[20], mod_CHA = data[21],
                           proficiency = data[22], mod_prof = data[23], clothes= data[24], weapon = data[25], ATK = data[26], DMG = data[27],
                           weapon_attributes = data[28], RT1 = data[29], RT2 = data[30], item = data[31], trinket = data[32], gold = data[33])


    







if __name__ == '__main__':

    app.run(debug=True)
    
