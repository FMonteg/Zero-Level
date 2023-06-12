import string

#with open('d:/Code/Git/Projets/DnD_Zero/raw_data.txt') as f:
#    lines = f.readlines()


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
    (0,13) : ["Mercenary", (12, "s"), "Simple weapons", "Short sword", "Leather armor", "Traveler's"],
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
    (1,12) : ["Bandit", (6, "g"), "Stealth", "Short sword", "Caltrops (10)", "Traveler's"],
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
    (2,14) : ["Broom maker", (6, "c"), "Woodcarver's tools", "Broom (Quarterstaff)", "4 heads of broomcorn", "Common"],
    (2,15) : ["Sheep Shearer", (4, "s"), "Short sword", "Shears (Shortsword)", "Sheepskin", "Common"],
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
    (5,12) : ["Drummer", (8, "s"), "Drum", "Short Sword", "Drum", "Traveler's"],
    (5,13) : ["Confectioner", (8, "c"), "Cook's utensils", "Wooden spoon (club)", "Cook's utensils", "Common"],
    (5,14) : ["Milliner", (8, "s"), "Weaver's tools", "Dagger", "Weaver's tools", "Fine"],
    (5,15) : ["Barber", (6, "s"), "Medicine", "Scissors (dagger)", "Jaw pliers", "Fine"],
    (5,16) : ["Card Player", (6, "c"), "Playing card set", "Hand crossbow", "Playing card set", "Traveler's"],
    (5,17) : ["Poet", (6, "c"), "Insight", "Quill (dagger)", "1 Parchment", "Common"],
    (5,18) : ["Singer", (6, "c"), "Performance", "Quarterstaff", "Song booklet", "Costume"],
    (5,19) : ["Forger", (10, "s"), "Forgery kit", "Dagger", "Forgery kit", "Common"],
    (5,20) : ["Conman", (6, "g"), "Disguise kit", "Short sword", "Disguise kit", "Fine"],
}


result = {}

for key, item in occupations_table.items():
    weapon = item[3]
    if result.get(weapon):
        continue
    print(weapon)
    w_type = int(input())
    dmg_number = input()
    dmg_dice = input()
    dmg_type = input()
    attributes = []
    temp = input()
    while temp != '':
        attributes.append(temp)
        temp = input()
    result[weapon] = [w_type, dmg_number+'d'+dmg_dice+' '+dmg_type, attributes]



for key, item in result.items():
    print('{0} : {1},'.format(key, item))

    #Weapon : Melee/Ranged, Damagenum, dmgdice, dmg type, Attributes
