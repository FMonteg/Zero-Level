from flask import Flask, request, render_template
#import string
from random import choice, randint




app = Flask(__name__)




class Character(object):
    def __init__(self, **kwargs):
        self.player_name = kwargs.get("player", '')

        self.gender = kwargs.get("gender", 'random')
        if self.gender == 'R':
            self.gender = choice(['M', 'F'])


        self.race = kwargs.get("race", 'random HIGH_FANTASY')
        if self.race.split(' ')[0] == 'random':
            self.race = self.random_race(self.race.split(' ')[1])
        self.subrace = 'NONE'
        if subraces.get(self.race):
            self.subrace = choice(subraces[self.race])
        
        random_name = kwargs.get("name_selector", True)
        if random_name:
            self.random_name()
        else:
            self.character_name = kwargs.get("character", '')


        (self.size, self.speed, extra_language, racial_bonuses, self.racial_abilities) = racial_traits[(self.race, self.subrace)]
        self.languages = ['Common'] + extra_language

        self.roll_stats(racial_bonuses)
        
        self.roll_occupation()

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








    def random_name(self):

        first_name = choice(names_table[(self.race, self.gender)])
        
        if names_table.get((self.race, 'O')):
            family_name = choice(names_table[(self.race, 'O')])
            self.character_name = first_name + ' ' + family_name
        else:
            self.character_name = first_name
        pass

        



    










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
        
        
        self.initiative = self.printable_modifier(self.attributes[1])

        pass


    






    def modifier(self, ability_score):
        return (ability_score//2)-5
    







    def printable_modifier(self, attrib):
        modif = self.modifier(attrib)
        if modif<0:
            return str(modif)
        else:
            return '+'+str(modif)
    


    def roll_occupation(self):

        attrib_max = choice([i for i in range(6) if self.attributes[i] == max(self.attributes)])
        alea = randint(1,20) 
        (self.occupation, coins, self.proficiency, self.weapon, self.item, self.clothes) = occupations_table[(attrib_max, alea)]
        self.prof_mod = self.printable_modifier(self.attributes[attrib_max]+4)

        if armor_table.get(self.item):
            self.AC = armor_table[self.item][0] + min(self.modifier(self.attributes[1]), armor_table[self.item][1])
        else:
            self.AC = 10 + self.modifier(self.attributes[1])

        self.gold = self.roll_money(coins)

        self.trinket = trinket_table[randint(1,100)]

        pass

    def roll_money(self, coins):
        number = randint(1, coins[0])
        if coins[1] == 's':
            type = 'silver'
        elif coins[1] == 'g':
            type = 'gold'
        elif coins[1] == 'c':
            type = 'copper'
        else:
            type = 'electrum'
        
        return '{0} {1} pieces'.format(number, type)
    
    def compute_attacks(self):

        (ability, damage, attributes) = weapons_table[self.weapon]
        
        if 'Finesse' in attributes and self.attributes[1]>self.attributes[0]:
            ability = 1
        
        self.atk = self.printable_modifier(self.attributes[ability]+4)

        temp = damage.split(' ')
        if temp[1] == 'b':
            temp[1] = 'bludgeoning'
        elif temp[1] == 's':
            temp[1] = 'slashing'
        elif temp[1] == 'p':
            temp[1] = 'piercing'
        else:
            temp[1] = 'special'
        temp[0] += self.printable_modifier(self.attributes[ability])
        self.dmg = ' '.join(temp)

        self.weapon_attributes = ", ".join(attributes)

        pass
    







    
    def export(self):
        data = []


        data.append(self.character_name)
        data.append(self.player_name)
        if self.gender=='M':
            data.append('Male')
        else:
            data.append('Female')

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
            data.append(self.printable_modifier(self.attributes[i]))

        data.append(self.proficiency)
        data.append(self.prof_mod)
        data.append(self.clothes)
        data.append(self.weapon)
        data.append(self.atk)
        data.append(self.dmg)
        data.append(self.weapon_attributes)

        for ab in self.racial_abilities:
            data.append(ab)
            data.append(racial_traits_descriptions[ab])
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
    ('Halfling', 'Lightfoot') : ['Small', '25 ft', ['Halfling'], [0, 2, 0, 0, 0, 1], ['Lucky', 'Halfling Nimbleness']],
    ('Halfling', 'Stout') : ['Small', '25 ft', ['Halfling'], [0, 2, 1, 0, 0, 0], ['Lucky', 'Halfling Nimbleness']],
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

racial_traits_descriptions = {
    'Inspiration' : 'Once per day, when you make an attack roll, saving throw, or ability check, you can use your inspiration to get advantage on that roll.',
    'Focus' : 'If you are not stressed out by the situation, you are able to concentrate to get an average result on an ability check. You may consider you got a 10 on a dice without rolling it, but the action is ten times longer to execute.',
    'Lucky' : 'When you roll a 1 on the d20 for an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll.',
    'Halfling Nimbleness' : 'You can move through the space of any creature that is of a size larger than yours.',
    'Darkvision 60 ft' : "You have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can’t discern color in darkness, only shades of gray.",
    'Dwarven Resilience' : "You have advantage on saving throws against poison, and you have resistance against poison damage.",
    'Gnome Cunning' : "You have advantage on all Intelligence, Wisdom, and Charisma saving throws against magic.",
    'Hellish Resistance' : "You have resistance to fire damage.",
    "Stone's Endurance" : "You can focus yourself to occasionally shrug off injury. When you take damage, you can use your reaction to roll a d12. Add your Constitution modifier to the number rolled and reduce the damage by that total. After you use this trait, you can’t use it again until you finish a short or long rest.",
    'Mountainborn' : "You have resistance to cold damage. You’re also acclimated to high altitude, including elevations above 20,000 feet.",
    'Trance' : "Elves don’t need to sleep. Instead, they meditate deeply, remaining semiconscious, for 4 hours a day. While meditating, you can dream after a fashion; such dreams are actually mental exercises that have become reflexive through years of practice. After resting in this way, you gain the same benefit that a human does from 8 hours of sleep.",
    "Relentless Endurance" : "When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead. You can’t use this feature again until you finish a long rest.",
    'Flight' : "You have a flying speed of 50 feet. To use this speed, you can’t be wearing medium or heavy armor.",
    'Talons' : "Your talons are natural weapons, which you can use to make unarmed strikes. If you hit with them, you deal slashing damage equal to 1d4 + your Strength modifier, instead of the bludgeoning damage normal for an unarmed strike.",
    "Damage Resistance (Fire)" : "You have resistance to fire damage due to your draconic ancestry.", 
    "Damage Resistance (Lightning)" : "You have resistance to lightning damage due to your draconic ancestry.", 
    "Damage Resistance (Poison)" : "You have resistance to poison damage due to your draconic ancestry.", 
    "Damage Resistance (Acid)" : "You have resistance to acid damage due to your draconic ancestry.", 
    "Damage Resistance (Cold)" : "You have resistance to cold damage due to your draconic ancestry.", 
    'Breath Weapon (cone)' : "You can use your action to exhale destructive energy. Your damage resistance determines the damage type of the exhalation. When you use your breath weapon, each creature in a 15 feet cone must make a Constitution saving throw, the DC for this saving throw equals 10 + your Constitution modifier. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. After you use your breath weapon, you can’t use it again until you complete a short or long rest.",
    'Breath Weapon (line)' : "You can use your action to exhale destructive energy. Your damage resistance determines the damage type of the exhalation. When you use your breath weapon, each creature in a 5 by 30 feet line must make a Dexterity saving throw, the DC for this saving throw equals 10 + your Constitution modifier. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. After you use your breath weapon, you can’t use it again until you complete a short or long rest.",
}



occupations_table = {#(Attribute (0 to 5), Number (1 to 20)) -> Occupation, Coins, Proficiency, Weapon, Item, Clothes
    #Strength based occupations
    (0,1) : ["Blacksmith", (12, "s"), "Smith's tools", "Light hammer", "Smith's tools", "Common"],
    (0,2) : ["Miner", (20, "c"), "Investigation", "Handaxe", "Miner's pick", "Common"],
    (0,3) : ["Teamster", (8, "s"), "Strength saving throws", "Whip", "Block and tackle", "Common"],
    (0,4) : ["Bodyguard", (10, "g"), "Athletics", "Maul", "Ring mail", "Traveler's"],
    (0,5) : ["Plowman/woman", (10, "c"), "Nature", "Quarterstaff", "A bag of good soil", "Common"],
    (0,6) : ["Rough", (6, "s"), "Intimidation", "Club", "Leather armor", "Common"],
    (0,7) : ["Butcher", (20, "s"), "Handaxes", "Butcher knife (handaxe)", "5 pounds of jerky", "Common"],
    (0,8) : ["Gladiator", (12, "g"), "Simple weapons", "Net", "Chain shirt", "Traveler's"],
    (0,9) : ["Woodcutter", (6, "s"), "Nature", "Handaxe", "A tie of cut wood", "Common"],
    (0,10) : ["Carpenter", (6, "g"), "Carpenter's tools", "Light hammer", "Carpenter's tools", "Common"],
    (0,11) : ["Milkman/Milkmaid", (8, "s"), "Animal handling", "Club", "Metal bucket", "Common"],
    (0,12) : ["Executioner", (12, "s"), "Intimidation", "Greataxe", "Basket", "Common"],
    (0,13) : ["Mercenary", (12, "s"), "Simple weapons", "Shortsword", "Leather armor", "Traveler's"],
    (0,14) : ["Bone carver", (6, "s"), "Woodcarver's tools", "Bone knife (dagger)", "3 large animal bones", "Common"],
    (0,15) : ["Mason", (10, "c"), "Mason's tools", "Light hammer", "Mason's tools", "Common"],
    (0,16) : ["Grinder", (8, "s"), "Animal handling", "Dagger", "Grinding stone", "Common"],
    (0,17) : ["Platner", (8, "s"), "Smith's tools", "Maul", "Sheet of metal", "Common"],
    (0,18) : ["Porter", (8, "c"), "Perception", "Broom (quarterstaff)", "Lye soap", "Common"],
    (0,19) : ["Jailer", (4, "s"), "Investigation", "Club", "A set of keys", "Common"],
    (0,20) : ["Wagoner", (12, "c"), "Land vehicles (wagon)", "Whip", "Wagon bolts", "Common"],
    #Dexterity based occupations
    (1,1) : ["Pickpocket", (12, "s"), "Sleight of haand", "Shortsword", "Thieves' tools", "Common"],
    (1,2) : ["Haberdasher", (12, "g"), "Persuasion", "Dagger", "3 yards fine cloth", "Fine"],
    (1,3) : ["Orphan", (4, "c"), "Stealth", "Club", "A beggar's cup", "Common"],
    (1,4) : ["Circus Acrobat", (8, "s"), "Acrobatics", "Scimitar", "Portable trampoline", "Costume"],
    (1,5) : ["Glassblower", (10, "s"), "Glassblower's tools", "Blowgun (10 needles)", "Glassblower's tools", "Common"],
    (1,6) : ["Messenger", (6, "s"), "Persuasion", "Quarterstaff", "Bell", "Traveler's"],
    (1,7) : ["Locksmith", (4, "g"), "Thieves' tools", "Dagger", "Lock", "Common"],
    (1,8) : ["Weaver", (12, "s"), "Weaver's tools", "Dagger", "Weaver's tools", "Common"],
    (1,9) : ["Hunter", (10, "s"), "Nature", "Shortbow (20 arrows)", "Deer skin", "Common"],
    (1,10) : ["Contortionist", (6, "g"), "Performance", "Flail", "Circus flier", "Costume"],
    (1,11) : ["Potter", (12, "s"), "Potter's tools", "Quarterstaff", "Potter's tools", "Common"],
    (1,12) : ["Bandit", (6, "g"), "Stealth", "Shortsword", "Caltrops (10)", "Traveler's"],
    (1,13) : ["Basketweaver", (4, "c"), "Weaver's tools", "Dagger", "Weaver's tools", "Common"],
    (1,14) : ["Bookbinder", (6, "s"), "Calligrapher's supplies", "Knife (dagger)", "Spool of thread", "Common"],
    (1,15) : ["Fletcher", (8, "s"), "Ranged weapons", "Shortbow", "A quiver of arrows (30)", "Common"],
    (1,16) : ["Gilder", (4, "g"), "Jeweler's tools", "Knife (dagger)", "Smelting pot", "Fine"],
    (1,17) : ["Miniaturist", (6, "c"), "Painter's supplies", "Brush (club)", "Painter's supplies", "Common"],
    (1,18) : ["Chicken Butcher", (6, "c"), "Cook's ustensils", "Butcher knife (handaxe)", "A chicken carcass", "Common"],
    (1,19) : ["Glovemaker", (8, "s"), "Leatherworker's tools", "Knife (dagger)", "A pair of fine leather gloves", "Common"],
    (1,20) : ["Jeweler", (4, "g"), "Jeweler's tools", "Dagger", "Jeweler's tools", "Fine"],
    #Constitution based occupations
    (2,1) : ["Gong Farmer", (12, "c"), "Constitution saving throws", "Club", "Sack of manure", "Common"],
    (2,2) : ["Pig Farmer", (10, "s"), "Animal handling", "Pitchfork (spear)", "5 lb cured ham", "Common"],
    (2,3) : ["Leatherworker", (6, "g"), "Leatherworker's Tools", "Dagger", "Leatherworker's tools", "Common"],
    (2,4) : ["Rat Catcher", (12, "c"), "Animal Handling", "Net", "Bag (with dead rats)", "Common"],
    (2,5) : ["Seaman", (8, "s"), "Sailing Ship", "Shortsword", "50' Rope", "Traveler's"],
    (2,6) : ["Tavern Cook", (6, "s"), "Cook's Utensils", "Cast Iron Pan (Club)", "Cook's utensils", "Common"],
    (2,7) : ["Brewer", (6, "g"), "Brewer's Supplies", "Steel Beer Stein (Club)", "Brewer's Supplies", "Common"],
    (2,8) : ["Chandler", (10, "s"), "Investigation", "Scissors (Dagger)", "Fine candles (50)", "Common"],
    (2,9) : ["Apiarist", (6, "g"), "Animal Handling", "Quarterstaff", "Padded armor", "Common"],
    (2,10) : ["Stone Carver", (6, "s"), "Performance", "Chisel (Dagger)", "3 uncarved bust-sized stone blocks", "Common"],
    (2,11) : ["Undertaker", (8, "s"), "Insight", "Light hammer", "Bouquet of dried flowers", "Fine"],
    (2,12) : ["Grave Digger", (12, "c"), "Athletics", "Greatclub", "Shovel", "Common"],
    (2,13) : ["Chestmaker", (12, "c"), "Woodcarver's tools", "Club", "Chest", "Common"],
    (2,14) : ["Broom maker", (6, "c"), "Woodcarver's tools", "Broom (quarterstaff)", "4 heads of broomcorn", "Common"],
    (2,15) : ["Sheep Shearer", (4, "s"), "Shortsword", "Shears (Shortsword)", "Sheepskin", "Common"],
    (2,16) : ["Parchmenter", (6, "s"), "Investigation", "Dagger", "Parchment (3 sheets)", "Common"],
    (2,17) : ["Smelter", (8, "s"), "Tinkerer's tools", "Light hammer", "Iron ingot", "Common"],
    (2,18) : ["Cooper", (8, "c"), "Carpenter's tools", "Light hammer", "Wooden plank", "Common"],
    (2,19) : ["Haenyeo (Diver)", (6, "s"), "Athletics", "Dagger", "A bushel of oysters", "Common"],
    (2,20) : ["Roofer", (12, "c"), "Carpenter's tools", "Light hammer", "Carpenter's tools", "Common"],
    #Intelligence based occupations
    (3,1) : ["Bookkeeper", (8, "s"), "Investigation", "Dagger", "Abacus", "Common"],
    (3,2) : ["Tax Collector", (12, "p"), "Intimidation", "Longsword", "Money sack", "Fine"],
    (3,3) : ["Wizard's Apprentice", (10, "s"), "Arcana", "Quarterstaff", "Book on arcane subject", "Fine"],
    (3,4) : ["Apothecary", (8, "s"), "Medicine", "Sickle", "Healer's kit", "Common"],
    (3,5) : ["Tinker", (6, "s"), "Tinker's Tools", "Hand Crossbow", "Tinker's tools", "Common"],
    (3,6) : ["Tutor", (8, "s"), "History", "Quarterstaff", "School book", "Common"],
    (3,7) : ["Navigator", (6, "g"), "Navigator's Tools", "Shortsword", "Navigator's tools", "Common"],
    (3,8) : ["Pastry Cook", (8, "s"), "Cook's utensils", "Rolling Pin (club)", "Cook's utensils", "Common"],
    (3,9) : ["Cartographer", (10, "s"), "Cartographer's Tools", "Compass (dagger)", "Cartographer's tools", "Traveler's"],
    (3,10) : ["Interpreter", (8, "g"), "History", "Quarterstaff", "Book", "Traveler's"],
    (3,11) : ["Scrivener", (8, "s"), "Calligrapher's Supplies", "Dagger", "Calligrapher's supplies", "Common"],
    (3,12) : ["Banker", (10, "p"), "Insight", "Quarterstaff", "Abacus", "Fine"],
    (3,13) : ["Barrister", (4, "g"), "Persuasion", "Club", "Law decree", "Fine"],
    (3,14) : ["Clockmaker", (6, "g"), "Tinker's tools", "Dagger", "A small clock", "Common"],
    (3,15) : ["Lampwright", (10, "s"), "Glassblower's tools", "Quarterstaff", "Lantern", "Common"],
    (3,16) : ["Lensgrinder", (6, "s"), "Tinker's tools", "Sickle", "Magnifying glass", "Common"],
    (3,17) : ["Portraitist", (12, "s"), "Painter's supplies", "Dagger", "Painter's supplies", ""],
    (3,18) : ["Herald", (4, "s"), "Performance", "Quarterstaff", "Speaking trumpet", "Common"],
    (3,19) : ["Astronomer", (8, "c"), "Perception", "Quarterstaff", "Wheel Chart", "Fine"],
    (3,20) : ["Knifeman", (12, "g"), "Medicine", "Dagger", "Jar of leeches", "Common"],
    #Wisdom based occupations
    (4,1) : ["Herbalist", (12, "s"), "Medicine", "Club", "Healer's kit", "Common"],
    (4,2) : ["Sexton", (12, "g"), "Religion", "Mace", "Holy symbol (emblem)", "Vestments"],
    (4,3) : ["Squire", (6, "s"), "History", "Longsword", "Shield", "Fine"],
    (4,4) : ["Friar", (8, "s"), "Religion", "Quarterstaff", "Holy Symbol (reliquary)", "Traveler's"],
    (4,5) : ["Woodward", (8, "s"), "Nature", "Quarterstaff", "Druidic focus (totem)", "Common"],
    (4,6) : ["Tracker", (8, "s"), "Survival", "Shortsword", "Hide armor", "Common"],
    (4,7) : ["Painter", (8, "c"), "Painter's supplies", "Dagger", "Painter's supplies", "Common"],
    (4,8) : ["Ostler", (8, "s"), "Animal Handling", "Whip", "Saddlebags", "Common"],
    (4,9) : ["Baker", (6, "s"), "Cook's Utensils", "Rolling Pin (club)", "Cook's utensils", "Common"],
    (4,10) : ["Servant", (12, "c"), "Perception", "Club", "Towel", "Common"],
    (4,11) : ["Trapper", (12, "s"), "Survival", "Light Crossbow (20 Bolts)", "Hunting trap", "Common"],
    (4,12) : ["Beadle", (12, "c"), "Religion", "Quarterstaff (with religious ornament)", "Holy Symbol", "Vestments"],
    (4,13) : ["Cheesemaker", (12, "c"), "Cook's utensils", "Quarterstaff", "10lb cheese wheel", "Common"],
    (4,14) : ["Bowyer", (4, "s"), "Ranged weapons", "Longbow (10 arrows)", "A bundle of 5 bow staves", "Common"],
    (4,15) : ["Cobbler", (12, "c"), "Cobbler's Tools", "Dagger", "Cobbler's tools", "Common"],
    (4,16) : ["Furrier", (4, "s"), "Survival", "Longbow (10 arrows)", "A badger fur", "Common"],
    (4,17) : ["Watchman", (6, "s"), "Perception", "Spear", "Leather Armor", ""],
    (4,18) : ["Midwife", (8, "c"), "Medicine", "Club", "Bucket", "Common"],
    (4,19) : ["Falconer", (12, "c"), "Animal Handling", "Shortbow (10 arrows)", "Bird bait", "Common"],
    (4,20) : ["Shaman", (8, "c"), "Nature", "Spear", "Druidic Focus (Totem)", "Common"],
    #Charisma based occupations
    (5,1) : ["Barker", (8, "g"), "Perception", "Club", "Speaking trumpet", "Costume"],
    (5,2) : ["Minstrel", (10, "g"), "Lute", "Dagger", "A lute", "Costume"],
    (5,3) : ["Alewife / Innkeeper", (6, "g"), "Charisma saving throws", "Club", "A grocery list", "Common"],
    (5,4) : ["Low Noble", (12, "p"), "Deception", "Rapier", "Papers declaring nobility", "Fine"],
    (5,5) : ["Costermonger", (6, "s"), "Persuasion", "Quarterstaff", "A dozen perfect apples", "Common"],
    (5,6) : ["Fishmonger", (6, "s"), "Perception", "Dagger", "Fishing tackle", "Common"],
    (5,7) : ["Mime", (10, "g"), "Performance", "Club", "Disguise kit", "Costume"],
    (5,8) : ["Storyteller", (12, "s"), "Performance", "Dagger", "Journal & pen", "Costume"],
    (5,9) : ["Diplomat", (12, "g"), "Insight", "Longsword", "Official papers", "Fine"],
    (5,10) : ["Peddlar", (10, "s"), "Persuasion", "Club", "Bag of trinkets", "Traveler's"],
    (5,11) : ["Fortune-Teller", (6, "s"), "Performance", "Ornate Dagger", "Crystal ball", "Costume"],
    (5,12) : ["Drummer", (8, "s"), "Drum", "Shortsword", "Drum", "Traveler's"],
    (5,13) : ["Confectioner", (8, "c"), "Cook's utensils", "Wooden spoon (club)", "Cook's utensils", "Common"],
    (5,14) : ["Milliner", (8, "s"), "Weaver's tools", "Dagger", "Weaver's tools", "Fine"],
    (5,15) : ["Barber", (6, "s"), "Medicine", "Scissors (dagger)", "Jaw pliers", "Fine"],
    (5,16) : ["Card Player", (6, "c"), "Playing card set", "Hand Crossbow", "Playing card set", "Traveler's"],
    (5,17) : ["Poet", (6, "c"), "Insight", "Quill (dagger)", "1 Parchment", "Common"],
    (5,18) : ["Singer", (6, "c"), "Performance", "Quarterstaff", "Song booklet", "Costume"],
    (5,19) : ["Forger", (10, "s"), "Forgery kit", "Dagger", "Forgery kit", "Common"],
    (5,20) : ["Conman", (6, "g"), "Disguise kit", "Shortsword", "Disguise kit", "Fine"],
}




armor_table = {#(X, Y) where AC = X + mod.DEX (max Y)
    "Leather armor" : (11, 10),
    "Hide armor" : (12, 2),
    "Shield" : (12, 10),
    "Padded armor" : (11, 10),
    "Chain shirt" : (13, 2),
    "Ring mail" : (14, 0),
}


trinket_table = {
    1 : "A mummified goblin hand",
    2 : "A piece of crystal that faintly glows in the moonlight",
    3 : "A gold coin minted in an unknown land",
    4 : "A diary written in a language you don't know",
    5 : "A brass ring that never tarnishes",
    6 : "An old chess piece made from glass",
    7 : "A pair of knucklebone dice, each with a skull symbol on the side that would normally show six pips",
    8 : "A small idol depicting a nightmarish creature that gives you unsettling dreams when you sleep near it",
    9 : "A rope necklace from which dangles four mummified elf fingers",
    10 : "The deed for a parcel of land in a realm unknown to you",
    11 : "A 1-ounce block made from an unknown material",
    12 : "A small cloth doll skewered with needles",
    13 : "A tooth from an unknown beast",
    14 : "An enormous scale, perhaps from a dragon",
    15 : "A bright green feather",
    16 : "An old divination card bearing your likeness",
    17 : "A glass orb filled with moving smoke",
    18 : "A 1-pound egg with a bright red shell",
    19 : "A pipe that blows bubbles",
    20 : "A glass jar containing a weird bit of flesh floating in pickling fluid",
    21 : "A tiny gnome-crafted music box that plays a song you dimly remember from your childhood",
    22 : "A small wooden statuette of a smug halfling",
    23 : "A brass orb etched with strange runes",
    24 : "A multicolored stone disk",
    25 : "A tiny silver icon of a raven",
    26 : "A bag containing forty-seven humanoid teeth, one of which is rotten",
    27 : "A shard of obsidian that always feels warm to the touch",
    28 : "A dragon's bony talon hanging from a plain leather necklace",
    29 : "A pair of old socks",
    30 : "A blank book whose pages refuse to hold ink, chalk, graphite, or any other substance or marking",
    31 : "A silver badge in the shape of a five-pointed star",
    32 : "A knife that belonged to a relative",
    33 : "A glass vial filled with nail clippings",
    34 : "A rectangular metal device with two tiny metal cups on one end that throws sparks when wet",
    35 : "A white, sequined glove sized for a human",
    36 : "A vest with one hundred tiny pockets",
    37 : "A small, weightless stone block",
    38 : "A tiny sketch portrait of a goblin",
    39 : "An empty glass vial that smells of perfume when opened",
    40 : "A gemstone that looks like a lump of coal when examined by anyone but you",
    41 : "A scrap of cloth from an old banner",
    42 : "A rank insignia from a lost legionnaire",
    43 : "A tiny silver bell without a clapper",
    44 : "A mechanical canary inside a gnome-crafted lamp",
    45 : "A tiny chest carved to look like it has numerous feet on the bottom",
    46 : "A dead sprite inside a clear glass bottle",
    47 : "A metal can that has no opening but sounds as if it is filled with liquid, sand, spiders, or broken glass (your choice)",
    48 : "A glass orb filled with water, in which swims a clockwork goldfish",
    49 : "A silver spoon with an M engraved on the handle",
    50 : "A whistle made from gold-colored wood",
    51 : "A dead scarab beetle the size of your hand",
    52 : "Two toy soldiers, one with a missing head",
    53 : "A small box filled with different-sized buttons",
    54 : "A candle that can't be lit",
    55 : "A tiny cage with no door",
    56 : "An old key",
    57 : "An indecipherable treasure map",
    58 : "A hilt from a broken sword",
    59 : "A rabbit's foot",
    60 : "A glass eye",
    61 : "A cameo carved in the likeness of a hideous person",
    62 : "A silver skull the size of a coin",
    63 : "An alabaster mask",
    64 : "A pyramid of sticky black incense that smells very bad",
    65 : "A nightcap that, when worn, gives you pleasant dreams",
    66 : "A single caltrop made from bone",
    67 : "A gold monocle frame without the lens",
    68 : "A 1-inch cube, each side painted a different color",
    69 : "A crystal knob from a door",
    70 : "A small packet filled with pink dust",
    71 : "A fragment of a beautiful song, written as musical notes on two pieces of parchment",
    72 : "A silver teardrop earring made from a real teardrop",
    73 : "The shell of an egg painted with scenes of human misery in disturbing detail",
    74 : "A fan that, when unfolded, shows a sleeping cat",
    75 : "A set of bone pipes",
    76 : "A four-leaf clover pressed inside a book discussing manners and etiquette",
    77 : "A sheet of parchment upon which is drawn a complex mechanical contraption",
    78 : "An ornate scabbard that fits no blade you have found so far",
    79 : "An invitation to a party where a murder happened",
    80 : "A bronze pentacle with an etching of a rat's head in its center",
    81 : "A purple handkerchief embroidered with the name of a powerful archmage",
    82 : "Half of a floorplan for a temple, castle, or some other structure",
    83 : "A bit of folded cloth that, when unfolded, turns into a stylish cap",
    84 : "A receipt of deposit at a bank in a far-flung city",
    85 : "A diary with seven missing pages",
    86 : "An empty silver snuffbox bearing an inscription on the surface that says 'dreams'",
    87 : "An iron holy symbol devoted to an unknown god",
    88 : "A book that tells the story of a legendary hero's rise and fall, with the last chapter missing",
    89 : "A vial of dragon blood",
    90 : "An ancient arrow of elven design",
    91 : "A needle that never bends",
    92 : "An ornate brooch of dwarven design",
    93 : "An empty wine bottle bearing a pretty label that says, 'The Wizard of Wines Winery, Red Dragon Crush, 331422-W'",
    94 : "A mosaic tile with a multicolored, glazed surface",
    95 : "A petrified mouse",
    96 : "A black pirate flag adorned with a dragon's skull and crossbones",
    97 : "A tiny mechanical crab or spider that moves about when it's not being observed",
    98 : "A glass jar containing lard with a label that reads, 'Griffon Grease'",
    99 : "A wooden box with a ceramic bottom that holds a living worm with a head on each end of its body",
    100 : "A metal urn containing the ashes of a hero",
}


names_table = {#Family names in (race, O), first names in (race, M) and (race, F) if exist
    ('Elf', 'O') : ['Amakiir', 'Amastacia', 'Galanodel', 'Holimion', 'Ilphelkiir', 'Liadon', 'Melianne', 'Naïlo', 'Siannodel', 'Xiloscient'],
    ('Elf', 'M') : ['Adran', 'Aelar', 'Aramil', 'Arannis', 'Aust', 'Beiro', 'Berrian', 'Carric', 'Enialis', 'Erdan', 'Erevan', 'Galinndan', 'Hadarai', 'Heian', 'Himo', 'Immeral', 'Ivellios', 'Laucian', 'Mindartis', 'Paelias', 'Peren', 'Quarion', 'Riardon', 'Rolen', 'Soveliss', 'Thamior', 'Tharivol', 'Theren', 'Varis'],
    ('Elf', 'F') : ['Adrie', 'Althaea', 'Anastrianna', 'Andraste', 'Antinua', 'Bethrynna', 'Birel', 'Caelynn', 'Drusilia', 'Enna', 'Felosial', 'Ielenia', 'Jelenneth', 'Keyleth', 'Leshanna', 'Lia', 'Meriele', 'Mialee', 'Naivara', 'Quelenna', 'Quillathe', 'Sariel', 'Shanairra', 'Shava', 'Silaqui', 'Theirastra', 'Thia', 'Vadania', 'Valanthe', 'Xanaphia'],

    ("Halfling", "M") : ['Alton', 'Ander', 'Cade', 'Corrin', 'Eldon', 'Errich', 'Finnan', 'Garret', 'Lindal', 'Lyle', 'Merric', 'Milo', 'Osborn', 'Perrin', 'Reed', 'Roscoe', 'Wellby'],
    ("Halfling", "F") : ['Andry', 'Bree', 'Callie', 'Cora', 'Euphémie', 'Jillian', 'Kithri', 'Lavinia', 'Lidda', 'Merla', 'Nedda', 'Paela', 'Portia', 'Séraphine', 'Shaena', 'Trym', 'Vani', 'Verna'],
    ("Halfling", "O") : ['Bonbaril', 'Feuilledethé', 'Grandpré', 'Hautecolline', 'Lancepavé', 'Pasdépines', 'Ramassebrosse', 'Roulecolline', 'Souslabranche', 'Vertbouteille'],

    ("Dwarf", "M") : ['Adrik', 'Albérich', 'Baern', 'Barendd', 'Brottor', 'Bruenor', 'Dain', 'Darrak', 'Delg', 'Eberk', 'Einkil', 'Fargrim', 'Flint', 'Gardain', 'Harbek', 'Kildrak', 'Morgran', 'Orsik', 'Oskar', 'Rangrim', 'Rurik', 'Taklinn', 'Thoradin', 'Thorin', 'Tordek', 'Traubon', 'Travok', 'Ulfgar', 'Veit', 'Vondal'],
    ("Dwarf", "F") : ['Ambre', 'Artin', 'Audhild', 'Bardryn', 'Dagnal', 'Diesa', 'Eldeth', 'Falkrunn', 'Finellen', 'Gunnloda', 'Gurdis', 'Helja', 'Hlin', 'Kathra', 'Kristryd', 'Ilde', 'Liftrasa', 'Mardred', 'Riswynn', 'Sannl', 'Torbera', 'Torgga', 'Vistra'],
    ("Dwarf", "O") : ['Balderk', 'Barbegelée', 'Dankil', 'Forgefeu', 'Fortenclume', 'Gorunn', 'Holderhek', 'Loderr', 'Lutgehr', 'Marteaudeguerre', 'Poing de Fer', 'Rumnaheim', 'Strakeln', 'Torunn', 'Ungart'],

    ("Half-Orc", "M") : ['Dench', 'Feng', 'Gell', 'Henk', 'Holg', 'Imsh', 'Keth', 'Krusk', 'Mhurren', 'Ront', 'Shump', 'Thokk'],
    ("Half-Orc", "F") : ['Baggi', 'Emen', 'Engong', 'Kansif', 'Myev', 'Neega', 'Ovak', 'Ownka', 'Shautha', 'Sutha', 'Vola', 'Volen', 'Yevelda'],

    ("Dragonborn", "M") : ['Arjhan', 'Balasar', 'Bharash', 'Donaar', 'Ghesh', 'Heskan', 'Kriv', 'Medrash', 'Mehen', 'Nadarr', 'Pandjed', 'Patrin', 'Rhogar', 'Shamash', 'Shedinn', 'Tarhun', 'Torinn'],
    ("Dragonborn", "F") : ['Akra', 'Biri', 'Daar', 'Farideh', 'Harann', 'Flavilar', 'Jheri', 'Kava', 'Korinn', 'Mishann', 'Nala', 'Perra', 'Raiann', 'Sora', 'Surina', 'Thava', 'Uadjit'],
    ("Dragonborn", "O") : ['Clethtinthiallor', 'Daardendrian', 'Delmirev', 'Drachedandion', 'Fenkenkabradon', 'Kepeshkmolik', 'Kerrhylon', 'Kimbatuul', 'Linxakasendalor', 'Myastan', 'Nemmonis', 'Norixius', 'Ophinshtalajiir', 'Prexijandilin', 'Shestendeliath', 'Turnuroth', 'Verthisathurgiesh', 'Yarjerit'],

    ("Gnome", "M") : ['Alston', 'Alvyn', 'Boddynock', 'Brocc', 'Burgell', 'Dimble', 'Eldon', 'Erky', 'Fonkin', 'Frug', 'Gerbo', 'Gimble', 'Glim', 'Jebeddo', 'Kellen', 'Namfoodle', 'Orryn', 'Roondar', 'Seebo', 'Sindri', 'Warryn', 'Wrenn', 'Zook'],
    ("Gnome", "F") : ['Bimpnottin', 'Breena', 'Caramip', 'Carlin', 'Donella', 'Duvamil', 'Ella', 'Ellyjobell', 'Ellywick', 'Lilli', 'Loopmottin', 'Lorilla', 'Mardnab', 'Nissa', 'Nyx', 'Oda', 'Orla', 'Roywyn', 'Shamil', 'Tana', 'Waywocket', 'Zanna'],
    ("Gnome", "O") : ['Beren', 'Daergel', 'Folkor', 'Garrick', 'Nackle', 'Murnig', 'Ningel', 'Raulnor', 'Scheppen', 'Timbers', 'Turen'],

    ("Tiefling", "M") : ['Akmenos', 'Amnon', 'Barakas', 'Damakos', 'Ekemon', 'Iados', 'Kairon', 'Leucis', 'Melech', 'Mordai', 'Morthos', 'Pelaios', 'Skamos', 'Therai'],
    ("Tiefling", "F") : ['Akta', 'Anakis', 'Bryseis', 'Criella', 'Damaia', 'Ea', 'Kallista', 'Lerissa', 'Makaria', 'Nemeia', 'Orianna', 'Phelaia', 'Rieta'],

    ("Aarakocra", "M") : ['Aera', 'Aial', 'Aur', 'Deekek', 'Errk', 'Heehk', 'Ikki', 'Kleeck', 'Oorr', 'Ouss', 'Quaf', 'Quierk', 'Salleek', 'Urreek', 'Zeed'],
    ("Aarakocra", "F") : ['Aera', 'Aial', 'Aur', 'Deekek', 'Errk', 'Heehk', 'Ikki', 'Kleeck', 'Oorr', 'Ouss', 'Quaf', 'Quierk', 'Salleek', 'Urreek', 'Zeed'],

    ("Goliath", "M") : ['Aukan', 'Eglath', 'Gae-Al', 'Gauthak', 'Ilikan', 'Keothi', 'Kuori', 'Lo-Kag', 'Manneo', 'Maveith', 'Nalla', 'Orilo', 'Paavu', 'Pethani', 'Thalai', 'Thotham', 'Uthal', 'Vaunea', 'Vimak'],
    ("Goliath", "F") : ['Aukan', 'Eglath', 'Gae-Al', 'Gauthak', 'Ilikan', 'Keothi', 'Kuori', 'Lo-Kag', 'Manneo', 'Maveith', 'Nalla', 'Orilo', 'Paavu', 'Pethani', 'Thalai', 'Thotham', 'Uthal', 'Vaunea', 'Vimak'],
    ("Goliath", "O") : ['Anakalathai', 'Elanithino', 'Gathakanathi', 'Kalagiano', 'Katho-Olavi', 'Kolae-Gileana', 'Ogolakanu', 'Thuliaga', 'Thunukalathi', 'Vaimei-Laga'],

    ("Human", "M") : ['Aseir', 'Bardeid', 'Haseid', 'Khemed', 'Mehmem', 'Sudeiman', 'Zasheir', 'Darvin', 'Dorn', 'Evendur', 'Gorstag', 'Grim', 'Helm', 'Malark', 'Morn', 'Randal', 'Stedd', 'Bor', 'Fodel', 'Glar', 'Grigor', 'Igan', 'Ivor', 'Kosef', 'Mival', 'Orel', 'Pavel', 'Sergor', 'Ander', 'Blath', 'Bran', 'frath', 'Geth', 'Lander', 'Luth', 'Malcer', 'Stor', 'Taman', 'Urth', 'Aoth', 'Bareris', 'Ehput-Ki', 'Kethot', 'Mumed', 'Ramas', 'So-Kehur', 'Thazar-De', 'Urhur', 'Borivik', 'Faurgar', 'Jandar', 'Kanithar', 'Madislak', 'Ralmevik', 'Shaumar', 'Vladislak', 'An', 'Chen', 'Chi', 'Fai', 'Jiang', 'Jun', 'Lian', 'Long', 'Meng', 'On', 'Shan', 'Shui', 'Wen', 'Anton', 'Diero', 'Marcon', 'Pieron', 'Rimardo', 'Romero', 'Salazar', 'Umbero'],
    ("Human", "F") : ['Atala', 'Ceidil', 'Hama', 'Jasmal', 'Meilil', 'Seipora', 'Yasheira', 'Zasheida', 'Arveene', 'Esvele', 'Jhessail', 'Kerri', 'Lureene', 'Miri', 'Rowan', 'Shandri', 'Tessele', 'Alethra', 'Kara', 'Katernin', 'Mara', 'Natali', 'Olma', 'Tana', 'Zora', 'Amafrey', 'Betha', 'Cefrey', 'Kethra', 'Mara', 'Olga', 'Silifrey', 'Westra', 'Arizima', 'Chathi', 'Nephis', 'Nulara', 'Murithi', 'Sefris', 'Thola', 'Umara', 'Zolis', 'Fyevarra', 'Hulmarra', 'Immith', 'Imzel', 'Navarra', 'Shevarra', 'Tammith', 'Yuldra', 'Bai', 'Chao', 'Jia', 'Lei', 'Mei', 'Qiao', 'Shui', 'Tai', 'Belama', 'Dona', 'Faila', 'Jalana', 'Luisa', 'Marta', 'Quara', 'Selise', 'Vonda'],
    ("Human", "O") : ['Basha', 'Dumein', 'Jassan', 'Khalid', 'Mostana', 'Pashar', 'Rein', 'Amblecrown', 'Buckman', 'Dundragon', 'Evenwood', 'Greycastle', 'Tallstag', 'Bersk', 'Chernin', 'Dotsk', 'Kulenov', 'Marsk', 'Nemetsk', 'Shemov', 'Starag', 'Brightwood', 'Helder', 'Hornraven', 'Lackman', 'Stormwind', 'Windrivver', 'Ankhalab', 'Anskuld', 'Fezim', 'Hahpet', 'Nathandem', 'Sepret', 'Uuthrakt', 'Chergoba', 'Dyernina', 'Iltazyara', 'Murnyethara', 'Stayanoga', 'Ulmokina', 'Chien', 'Huang', 'Kao', 'Kung', 'Lao', 'Ling', 'Mei', 'Pin', 'Shin', 'Sum', 'Tan', 'Wan', 'Agosto', 'Astorio', 'Calabra', 'Domine', 'Falone', 'Marivaldi', 'Pisacar', 'Ramondo'],
}

weapons_table = {#Weapon : Melee/Ranged, Damage, Attributes
                'Light hammer' : [0, '1d4 b', ['Light', 'Thrown']],
                'Handaxe' : [0, '1d6 s', ['Light', 'Thrown']],
                'Whip' : [0, '1d4 s', ['Finesse', 'Reach']],
                'Maul' : [0, '2d6 b', ['Heavy', 'Two-handed']],
                'Quarterstaff' : [0, '1d6 b', ['Versatile (1d8)']],
                'Club' : [0, '1d4 b', ['Light']],
                'Butcher knife (handaxe)' : [0, '1d6 s', ['Light', 'Thrown']],
                'Net' : [1, '0 b', ['Thrown', 'Special']],
                'Greataxe' : [0, '2d6 s', ['Heavy', 'Two-handed']],
                'Bone knife (dagger)' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
                'Dagger' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
                'Broom (quarterstaff)' : [0, '1d6 b', ['Versatile (1d8)']],
                'Shortsword' : [0, '1d6 p', ['Finesse', 'Light']],
                'Scimitar' : [0, '1d6 s', ['Finesse', 'Light']],
                'Blowgun (10 needles)' : [1, '1d1 p', ['Loading']],
                'Shortbow (20 arrows)' : [1, '1d6 p', ['Two-handed']],
                'Flail' : [0, '1d8 b', []],
                'Knife (dagger)' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
                'Shortbow' : [1, '1d6 p', ['Two-handed']],
                'Brush (club)' : [0, '1d4 b', ['Light']],
                'Pitchfork (spear)' : [0, '1d6 p', ['Versatile (1d8)', 'Thrown']],
                'Cast Iron Pan (club)' : [0, '1d4 b', ['Light']],
                'Steel Beer Stein (club)' : [0, '1d4 b', ['Light']],
                'Scissors (dagger)' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
                'Chisel (dagger)' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
                'Greatclub' : [0, '1d8 b', ['Two-handed']],
                'Shears (shortsword)' : [0, '1d6 p', ['Finesse', 'Light']],
                'Longsword' : [0, '1d8 s', ['Versatile (1d10)']],
                'Sickle' : [0, '1d4 s', ['Light']],
                'Hand Crossbow' : [1, '1d6 p', ['Light', 'Loading']],
                'Rolling Pin (club)' : [0, '1d4 b', ['Light']],
                'Compass (dagger)' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
                'Mace' : [0, '1d6 b', []],
                'Light Crossbow (20 Bolts)' : [1, '1d8 p', ['Two-handed', 'Loading']],
                'Quarterstaff (with religious ornament)' : [0, '1d6 b', ['Versatile (1d8)']],
                'Longbow (10 arrows)' : [1, '1d8 p', ['Heavy', 'Two-handed']],
                'Spear' : [0, '1d6 p', ['Versatile (1d8)', 'Thrown']],
                'Shortbow (10 arrows)' : [1, '1d6 p', ['Two-handed']],
                'Rapier' : [0, '1d8 p', ['Finesse']],
                'Ornate Dagger' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
                'Wooden spoon (club)' : [0, '1d4 b', ['Light']],
                'Scissors (dagger)' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
                'Quill (dagger)' : [0, '1d4 p', ['Finesse', 'Light', 'Thrown']],
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
                           weapon_attributes = data[28], RT1 = data[29], RTD1 = data[30], RT2 = data[31], RTD2 = data[32],
                           item = data[33], trinket = data[34], gold = data[35])


    

if __name__ == '__main__':

    app.run(debug=True)
    
