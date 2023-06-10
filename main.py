from flask import Flask, request, redirect, url_for, flash, jsonify, render_template
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
        self.abilities = self.roll_stats(racial_bonuses)
        

        temp = self.roll_occupation()
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
        


        return 'Poukaya'
    
    def roll_stats(self, racial_bonuses):
        stats = []

        for i in range(6):
            alea = [randint(1,6) for j in range(4)]
            alea.sort()
            alea.pop(0)
            stats.append(sum(alea))

        
        return [sum(x) for x in zip(stats, racial_bonuses)]
    
    def modifier(self, ability_score):
        return (ability_score//2)-5
    
    def roll_occupation(self):
        temp = ('Occupation', 'Coins', 'Proficiency', 'Weapon', 'Item', 'Clothes')
        return temp
    
    def sheet(self):
        character_sheet =[]

        character_sheet.append(self.player_name)
        character_sheet.append(self.character_name)
        character_sheet.append(self.gender)
        character_sheet.append(self.race)
        character_sheet.append(self.abilities)
        character_sheet.append(self.languages)
        character_sheet.append(self.racial_abilities)

        return character_sheet
    
    def export(self):
        return self.player_name, self.character_name




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
    ('Human', 'NONE') : ['Medium', '30 ft', [], [1, 1, 1, 1, 1, 1], []],
    ('Halfling', 'Lightfoot') : ['Small', '25 ft', ['Halfling'], [0, 2, 0, 0, 0, 1], ['Brave', 'Halfling Nimbleness']],
    ('Halfling', 'Stout') : ['Small', '25 ft', ['Halfling'], [0, 2, 1, 0, 0, 0], ['Brave', 'Halfling Nimbleness']],
    ('Dwarf', 'Hill') : ['Medium', '25 ft', ['Dwarvish'], [0, 0, 2, 0, 1, 0], ['Darkvision 60 ft', 'Dwarven Resilience']],
    ('Dwarf', 'Mountain') : ['Medium', '25 ft', ['Dwarvish'], [1, 0, 2, 0, 0, 0], ['Darkvision 60 ft', 'Dwarven Resilience']],
    ('Gnome', 'Rock') : ['Small', '25 ft', ['Gnomish'], [0, 0, 1, 2, 0, 0], ['Darkvision 60 ft', 'Gnome Cunning']],
    ('Gnome', 'Forest') : ['Small', '25 ft', ['Gnomish'], [0, 1, 0, 2, 0, 0], ['Darkvision 60 ft', 'Gnome Cunning']],
    ('Tiefling', 'NONE') : ['Medium', '30 ft', ['Infernal'], [0, 0, 0, 1, 0, 2], ['Darkvision 60 ft', 'Hellish Resistance']],
    ('Goliath', 'NONE') : ['Medium', '30 ft', ['Giant'], [2, 0, 1, 0, 0, 0], ["Stone's Endurance", 'Mountainborn']],
    ('Elf', 'High') : ['Medium', '30 ft', ['Elvish'], [0, 2, 0, 1, 0, 0], ['Darkvision 60 ft', 'Fey Ancestry', 'Trance']],
    ('Elf', 'Wood') : ['Medium', '30 ft', ['Elvish'], [0, 2, 0, 0, 1, 0], ['Darkvision 60 ft', 'Fey Ancestry', 'Trance']],
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


@app.route("/")
def hello():
    return render_template("accueil.html")



@app.route('/sheet', methods=['POST'])
def create():
    player_name = request.form['player']
    character_name = request.form['character']
    random_name = request.form['name_selector']
    gender = request.form['gender']
    race = request.form['race']

    character = Character(player = player_name, character = character_name, gender = gender, race = race, random_name = random_name)

    data = character.export()
    return render_template("sheet.html", player_name = data[0], character_name = data[1])






if __name__ == '__main__':

    app.run(debug=True)
    
