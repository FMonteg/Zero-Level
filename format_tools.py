import string

occupation = []
coin_num = []
coin_type = []
proficiency = []
weapon = []
item = []
clothes = []

for i in range(20):
    print("Occupation number {0}:".format(i+1))
    occupation.append(input())
    coin_num.append(input())
    coin_type.append(input())
    proficiency.append(input())
    weapon.append(input())
    item.append(input())
    clothes.append(input())

for i in range(20):
    print('(0,{0}) : ["{1}", ({2}, "{3}"), "{4}", "{5}", "{6}", "{7}"],'.format(i+1, occupation[i], coin_num[i], coin_type[i], proficiency[i], weapon[i], item[i], clothes[i]))


