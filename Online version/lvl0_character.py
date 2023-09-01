import json
import os
from random import choice, randint

# Set the working directory to the location of your project
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

class Character:
    def __init__(self, **kwargs):
        self.player_name = kwargs.get("player_name", '')

        self.gender = kwargs.get("gender", 'R')
        if self.gender == 'R':
            self.gender = choice(['M', 'F'])

        selected_race = kwargs.get("race", 'random HIGH_FANTASY')
        if selected_race.split(' ')[0] == 'random':
            self.generate_race(context = selected_race.split(' ')[1])
        else:
            self.generate_race(race = selected_race)
        
        random_name = kwargs.get("random_name", True)
        self.character_name = kwargs.get("character_name", '')
        if random_name:
            self.generate_name()

        self.generate_occupation()
        self.calculate_derived_stats()
        self.generate_trinket()
        self.generate_attack_stats()
        self.generate_racial_traits_descriptions()
        pass

    def generate_race(self, **kwargs):
        context = kwargs.get("context", 'HIGH_FANTASY')
        self.race = kwargs.get("race", 'NONE')
        
        if self.race == 'NONE':
            self.generate_random_race(context)        
        self.generate_subrace()
        
        with open(os.path.join('data', 'lvl0_races_characteristics.json'), 'r') as json_file:
            table = json.load(json_file)
        (self.size, self.speed, extra_language, racial_bonuses, self.racial_abilities) = table[self.race+' '+self.subrace]
        self.languages = ['Common'] + extra_language

        self.generate_attributes(racial_bonuses)
        pass

    def generate_random_race(self, context):
        alea = randint(1,100)        
        with open(os.path.join('data', 'lvl0_races_probability_weights.json'), 'r') as json_file:
            table = json.load(json_file)[context]

        for i in range(len(table)):
            if alea <= table[i][0]:
                self.race = table[i][1]
                break
        pass

    def generate_subrace(self):
        with open(os.path.join('data', 'lvl0_subraces.json'), 'r') as json_file:
            table = json.load(json_file)
        
        if table.get(self.race):
            self.subrace = choice(table[self.race])
        else:
            self.subrace = 'NONE'
        pass

    def generate_name(self):
        with open(os.path.join('data', 'lvl0_names.json'), 'r') as json_file:
            table = json.load(json_file)

        first_name = choice(table[self.race+' '+self.gender])
        
        if table.get(self.race+' O'):
            family_name = choice(table[self.race+' O'])
            self.character_name = first_name + ' ' + family_name
        else:
            self.character_name = first_name

        pass
        
    def generate_attributes(self, racial_bonuses):
        stats = []

        for i in range(6):
            alea = [randint(1,6) for j in range(4)]
            alea.sort()
            alea.pop(0)
            stats.append(sum(alea))

        self.attributes = [sum(x) for x in zip(stats, racial_bonuses)]
        self.highest = choice([i for i in range(6) if self.attributes[i] == max(self.attributes)])
        pass

    def generate_occupation(self):
        alea = randint(1,20)

        with open(os.path.join('data', 'lvl0_occupations.json'), 'r') as json_file:
            table = json.load(json_file)

        (self.occupation, coins, self.proficiency, self.weapon, self.item, self.clothes) = table[self.printable_attributes(self.highest)+' '+str(alea)]
        self.generate_money(coins)
        pass

    def generate_money(self, coins):
        number = randint(1, coins[0])
        if coins[1] == 's':
            type = 'silver'
        elif coins[1] == 'g':
            type = 'gold'
        elif coins[1] == 'c':
            type = 'copper'
        else:
            type = 'electrum'
        
        self.money = '{0} {1} pieces'.format(number, type)
        pass

    def calculate_derived_stats(self):
        self.HP = randint(1,4) + self.modifier(self.attributes[2])
        if self.HP <= 0:
             self.HP = 1
        
        self.initiative = self.printable_modifier(self.attributes[1])

        self.prof_mod = self.printable_modifier(self.attributes[self.highest]+4)

        with open(os.path.join('data', 'lvl0_armors.json'), 'r') as json_file:
            table = json.load(json_file)
        if table.get(self.item):
            self.AC = table[self.item][0] + min(self.modifier(self.attributes[1]), table[self.item][1])
        else:
            self.AC = 10 + self.modifier(self.attributes[1])
        pass

    def generate_trinket(self):
        alea = randint(1,100)        
        with open(os.path.join('data', 'lvl0_trinkets.json'), 'r') as json_file:
            self.trinket = json.load(json_file)[str(alea)]
        pass

    def generate_attack_stats(self):
        with open(os.path.join('data', 'lvl0_weapons.json'), 'r') as json_file:
            (ability, damage, attributes) = json.load(json_file)[self.weapon]
        
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

    def generate_racial_traits_descriptions(self):
        with open(os.path.join('data', 'lvl0_racial_traits_descriptions.json'), 'r') as json_file:
            table = json.load(json_file)

        self.racial_traits_descriptions = {}
        for trait in self.racial_abilities:
            self.racial_traits_descriptions[trait] = table[trait]
        pass

    def modifier(self, ability_score):
        return (ability_score//2)-5

    def printable_modifier(self, attrib):
        modif = self.modifier(attrib)
        if modif<0:
            return str(modif)
        else:
            return '+'+str(modif)
        
    def printable_attributes(self, index):
        attributes = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
        return attributes[index]

    def export_character_sheet(self):
        # Export data for character sheet
        # 
        pass




