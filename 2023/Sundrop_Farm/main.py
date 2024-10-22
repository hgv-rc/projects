# Game variables
import random
game_vars = {
    'day': 1,
    'energy': 10,
    'money': 20,
    'bag': {'LET': 0,
            'POT': 0,
            'CAU': 0},
}

seed_list = ['LET', 'POT', 'CAU']
seeds = {
    'LET': {'name': 'Lettuce',
            'price': 2,
            'growth_time': 2,
            'crop_price': 3
            },

    'POT': {'name': 'Potato',
            'price': 3,
            'growth_time': 3,
            'crop_price': 6
            },

    'CAU': {'name': 'Cauliflower',
            'price': 5,
            'growth_time': 6,
            'crop_price': 14
            },
}

farm = [ [None, None, None, None, None],
         [None, None, None, None, None],
         [None, None, 'House', None, None],
         [None, None, None, None, None],
         [None, None, None, None, None] ]

#-----------------------------------------------------------------------
# in_town(game_vars)
#
#    Shows the menu of Albatross Town and returns the player's choice
#    Players can
#      1) Visit the shop to buy seeds
#      2) Visit the farm to plant seeds and harvest crops
#      3) End the day, resetting Energy to 10 and allowing crops to grow
#
#      9) Save the game to file
#      0) Exit the game (without saving)
#-----------------------------------------------------------------------
def in_town(game_vars):
    while True:
        try:
            show_stats(game_vars)
            print("You are in Albatross Town")
            print("-----------------------------")
            print('1) Visit Shop')
            print('2) Visit Farm')
            print('3) End Day')
            print()
            print('9) Save Game')
            print('0) Exit Game')
            print("-----------------------------")
        
            decision_intown = int(input('Your choice? '))
            return decision_intown
        except:
            print('Invalid Input')
            
    

#----------------------------------------------------------------------
# in_shop(game_vars)
#
#    Shows the menu of the seed shop, and allows players to buy seeds
#    Seeds can be bought if player has enough money
#    Ends when player selects to leave the shop
#----------------------------------------------------------------------
def in_shop(game_vars):
    try:
        #Prints Item Shop Menu
        total_in_bag = game_vars['bag']['LET'] + game_vars['bag']['POT'] + game_vars['bag']['CAU']
        counter = 1
        show_stats(game_vars)
        print('What do you wish to buy?')
        print('{:17}{:8}{:15}{:10}'.format('Seed','Price','Days to Grow','Crop Price'))
        print('---------------------------------------------------')
        for i in seeds:
            print('{:<1}{}{:<17}{:<10}{:<15}{:<6}'.format(counter,')', seeds[i]['name'], seeds[i]['price'], seeds[i]['growth_time'], seeds[i]['crop_price'],))
            counter += 1
        print()
        print("0) Leave")
        print('---------------------------------------------------')

        #Prompts choice from user to buy which seeds
        store_input = int(input('Your Choice? '))
        if store_input == 1:
            print('You have ${}'.format(game_vars['money']))
            quantity = int(input('How many do you wish to buy? '))
            if quantity + total_in_bag < 10: #checks whether the quantity that user wants to buy is greater than the total amount of seeds in bag combined with the quantity 
                cost = quantity * seeds['LET']['price']
                if cost <= game_vars['money']:
                    print('You bought {} Lettuce seeds.'.format(quantity))
                    game_vars['bag']['LET'] += quantity
                    game_vars['money'] -= cost
                    in_shop(game_vars)
                if cost > game_vars['money']:
                    print("You can't afford that!")
                    in_shop(game_vars)
            else:
                print('Sorry, not enough storage in your bag')
                in_shop(game_vars)
        if store_input == 2:
            print('You have ${}'.format(game_vars['money']))
            quantity = int(input('How many do you wish to buy? '))
            if quantity + total_in_bag < 10 : #checks whether the quantity that user wants to buy is greater than the total amount of seeds in the bag combined with the quantity 
                cost = quantity * seeds['POT']['price']
                if cost <= game_vars['money']:
                    print('You bought {} Potato seeds.'.format(quantity))
                    game_vars['bag']['POT'] += quantity
                    game_vars['money'] -= cost
                    in_shop(game_vars)
                if cost > game_vars['money']:
                    print("You can't afford that!")
                    in_shop(game_vars)
            else:
                print('Sorry, not enough storage in your bag')
                in_shop(game_vars)
        if store_input == 3:
            print('You have ${}'.format(game_vars['money']))
            quantity = int(input('How many do you wish to buy? '))
            cost = quantity * seeds['CAU']['price']
            if quantity + total_in_bag < 10: #checks whether the quantity that user wants to buy is greater than the total amount of seeds in the bag combined with the quantity 
                if cost <= game_vars['money']:
                    print('You bought {} Cauliflower seeds.'.format(quantity))
                    game_vars['bag']['CAU'] += quantity
                    game_vars['money'] -= cost
                    in_shop(game_vars)
                if cost > game_vars['money']:
                    print("You can't afford that!")
                    in_shop(game_vars)
            else:
                print('Sorry, not enough storage in your bag')
                in_shop(game_vars)
    except:
        print('Invalid input')
    


#----------------------------------------------------------------------
# draw_farm(farm, farmer_row, farmer_col)
#
#    Draws the farm
#    Each space on the farm has 3 rows:
#      TOP ROW:
#        - If a seed is planted there, shows the crop's abbreviation
#        - If it is the house at (2,2), shows 'HSE'
#        - Blank otherwise
#      MIDDLE ROW:
#        - If the player is there, shows X
#        - Blank otherwise
#      BOTTOM ROW:
#        - If a seed is planted there, shows the number of turns before
#          it can be harvested
#        - Blank otherwise
#----------------------------------------------------------------------
def draw_farm(farm, farmer_row, farmer_col):
    for row in range(len(farm)):
        #prints the border between the spaces
        for num_of_plus_rows in range(len(farm)):
            print("+-----", end = '')
        print('+')
    
    
        #top row of blank space   
        for col in range(len(farm)):
            if farm[row][col] == None: #if not none and instead is if farm[row][col] != list, code will not run line 157 cause str is not a list 
                print("|     ",end='')
            elif type(farm[row][col]) == list:
                print('| {} '.format(farm[row][col][0]),end='')
            elif farm[row][col] == 'House':
                print('| HSE ',end='')
        print('|')

        #mid row of blank space
        for col in range(len(farm)):
            if farmer_row==row and farmer_col==col:
                print("|  X  ",end='')
            else:
                print("|     ",end='')
        print('|')

        #bot row of blank space
        for col in range(len(farm)):
            if type(farm[row][col]) == list:
                print('|  {}  '.format(farm[row][col][1]),end='')
            elif farm[row][col] != list:
                print("|     ",end='')
            #reason for type():
            #so that when the program compares the list it returns True instead of False when the code doesn't have type() 
        print('|')
    print('+-----+-----+-----+-----+-----+')
        
            
pass

#----------------------------------------------------------------------
#
#    Handles the actions on the farm. Player starts at (2,2), at the
#      farmhouse.
#
#    Possible actions:
#    W, A, S, D - Moves the player
#      - Will show error message if attempting to move off the edge
#      - If move is successful, Energy is reduced by 1
#
#    P - Plant a crop
#      - Option will only appear if on an empty space
#      - Shows error message if there are no seeds in the bag
#      - If successful, Energy is reduced by 1
#
#    H - Harvests a crop
#      - Option will only appear if crop can be harvested, i.e., turns
#        left to grow is 0
#      - Option shows the money gained after harvesting
#      - If successful, Energy is reduced by 1
#
#    R - Return to town
#      - Does not cost energy
#----------------------------------------------------------------------
def in_farm(game_vars, farm, seeds):
    
    farmer_row = 2
    farmer_col = 2
    while True:        
        draw_farm(farm, farmer_row, farmer_col)
        show_stats(game_vars)
        print("Energy: " + str(game_vars['energy']))
        print("[WASD] Move")
        print("P)lant seed")
        print("R)eturn to Town")
        decision_infarm = input('Your action? ').upper()
        if decision_infarm == 'R':
            break
        #Movement Mechanic ----- Checks energy more than 0, if yes, checks player's input and player position with the farmer_row and farmer_col as they need to be in specific range of cords
        if game_vars['energy'] != 0:
            if decision_infarm == 'W' and 1 <= farmer_row <= 4:
                farmer_row -= 1
                game_vars['energy'] -= 1
            if decision_infarm == 'S' and 0 <= farmer_row <= 3:
                farmer_row += 1
                game_vars['energy'] -= 1
            if decision_infarm == 'A' and 1 <= farmer_col <= 4:
                farmer_col -= 1
                game_vars['energy'] -= 1
            if decision_infarm == 'D' and 0 <= farmer_col <= 3:
                farmer_col += 1
                game_vars['energy'] -= 1
            #Harvest Mechanic --- Checks for user's position with farm[farmer_row][farmer_col] and cross-references with the farm list map. 
            #                     If it detects farm[farmer_row][farmer_col] on the map as a list the program allows the user to harvest the crop
            #                     and then it sets the farm[farmer_row][farmer_col] on the map back to None
            if decision_infarm == 'H':
                if type(farm[farmer_row][farmer_col]) == list:
                    if farm[farmer_row][farmer_col][1] == 0:
                        price_seed = seeds[farm[farmer_row][farmer_col][0]]['crop_price']
                        game_vars['money'] += price_seed
                        game_vars['energy'] -= 1
                        farm[farmer_row][farmer_col] = None

            #Planting Mechanic --- Checks whether current postion of user has a seed e.g ['LET',2]. If not, shows the different seeds that the user can plant and 
            #                      changes the farm[farmer_row][farmer_col] which is None into a list containing the name of seed and growth time
            if decision_infarm == 'P':
                if farm[farmer_row][farmer_col] != None:
                    print("Can't plant here")
                else:
                        print('What do you wish to plant?')
                        print('-----------------------------------------------------')
                        print('{:10}{:17}{:15}{:10}'.format('Seed','Days to Grow','Crop Price','Available'))
                        print('-----------------------------------------------------')
                        counter = 1
                        for i in game_vars['bag']:
                            if i == 'LET':
                                print("{}){:5}{:8}{:15}{:15}".format(counter,seeds.get(i).get('name'),seeds.get(i).get('growth_time'),seeds.get(i).get('crop_price'),game_vars.get('bag').get(i)))
                                counter += 1
                            if i == 'POT':
                                print("{}){:5}{:9}{:15}{:15}".format(counter,seeds.get(i).get('name'),seeds.get(i).get('growth_time'),seeds.get(i).get('crop_price'),game_vars.get('bag').get(i)))
                                counter += 1
                            if i == 'CAU':
                                print("{}){:2}{:4}{:15}{:15}".format(counter,seeds.get(i).get('name'),seeds.get(i).get('growth_time'),seeds.get(i).get('crop_price'),game_vars.get('bag').get(i)))
                                counter += 1
                        print()
                        print("0)Leave")
                        print('-----------------------------------------------------')
                        try:
                            planting_decision = int(input('Your Choice? '))
                            if planting_decision == 1:
                                    if game_vars['bag']['LET'] <= 0:
                                        in_farm(game_vars, farm, seeds)
                                    else:
                                        game_vars['bag']['LET'] -= 1 
                                        List_LET = ['LET',2]           
                                        farm[farmer_row][farmer_col] = List_LET
                                        game_vars['energy'] -= 1
                                            
                            if planting_decision == 2:
                                    if game_vars['bag']['POT'] <= 0:
                                        in_farm(game_vars, farm, seeds)
                                    else:
                                        game_vars['bag']['POT'] -= 1
                                        List_POT = ['POT',3]
                                        farm[farmer_row][farmer_col] = List_POT
                                        game_vars['energy'] -= 1
                                            
                            if planting_decision == 3:
                                    if game_vars['bag']['CAU'] <= 0:
                                        in_farm(game_vars, farm, seeds)
                                    else:
                                        game_vars['bag']['CAU'] -= 1
                                        List_CAU = ['CAU',6]
                                        farm[farmer_row][farmer_col] = List_CAU
                                        game_vars['energy'] -= 1
                            if planting_decision == 0:
                                break
                        except:
                            print('Input Invalid')
                            
        else:
            print('Sorry, you have no energy.')                

#----------------------------------------------------------------------
# show_stats(game_vars)
#
#    Displays the following statistics:
#      - Day
#      - Energy
#      - Money
#      - Contents of Seed Bag
#----------------------------------------------------------------------
def show_stats(game_vars):
    print('+--------------------------------------------------+')
    
    print('{}{:4}{:10}{:8}{:10}{:7}{:11}{}'.format('|', 'Day',str(game_vars['day']), 'Energy:', str(game_vars['energy']), 'Money:', str(game_vars['money']),'|'))
    if game_vars['bag'] == {}:
        print('| You have no seeds.                               |')
    if game_vars['bag'] != {}:
        print('| Your Seeds:                                      |')
    if game_vars['bag']['LET'] != 0:
        print('{:3}{:10}{:6}{:5}{:27}{}'.format('|','Lettuce:','',game_vars['bag']['LET'],'','|'))
    if game_vars['bag']['POT'] != 0:
        print('{:3}{:10}{:6}{:5}{:27}{}'.format('|','Potato:','',game_vars['bag']['POT'],'','|'))
    if game_vars['bag']['CAU'] != 0:
        print('{:3}{:10}{:4}{:5}{:27}{}'.format('|','Cauliflower:','',game_vars['bag']['CAU'],'','|'))
        
    print('+--------------------------------------------------+')
    

#----------------------------------------------------------------------
# end_day(game_vars)
#
#    Ends the day
#      - The day number increases by 1
#      - Energy is reset to 10
#      - Every planted crop has their growth time reduced by 1, to a
#        minimum of 0
#----------------------------------------------------------------------
def end_day(game_vars,farm):
    random_price_gen(seeds)
    #Resets energy & increases the day by 1
    game_vars['day'] += 1
    game_vars['energy'] = 10
    for row in range(len(farm)):
        for col in range(len(farm)):
            if type(farm[row][col]) == list:
                if farm[row][col][1] > 0:
                    farm[row][col][1] -= 1
    pass


#----------------------------------------------------------------------
# save_game(game_vars, farm)
#
#    Saves the game into the file "savegame.txt"
#----------------------------------------------------------------------
def save_game(game_vars, farm):
    with open(r'savegame.txt', 'w') as savefile:
        savefile.write('{}/{}/{}\n'.format(game_vars['day'], game_vars['energy'], game_vars['money']))
        for i in game_vars['bag']:
            savefile.write('{}|'.format(game_vars['bag'][i]))
        savefile.write('\n')
        for row in range(len(farm)):
            for col in range(len(farm)):
                savefile.write('{}+'.format(farm[row][col]))
            savefile.write('\n')


    
    pass

#----------------------------------------------------------------------
# load_game(game_vars, farm)
#
#    Loads the saved game by reading the file "savegame.txt"
#----------------------------------------------------------------------
def load_game(game_vars, farm):   
    with open(r'savegame.txt', 'r') as savefile: 
        new_game_vars = savefile.readline().strip('\n').split('/')
        game_vars['day'] = int(new_game_vars[0])
        game_vars['energy'] = int(new_game_vars[1])
        game_vars['money'] = int(new_game_vars[2])
        new_bag_seeds = savefile.readline().strip('\n').split('|')[:-1] 
        game_vars['bag']['LET'] = int(new_bag_seeds[0])
        game_vars['bag']['POT'] = int(new_bag_seeds[1])
        game_vars['bag']['CAU'] = int(new_bag_seeds[2])
        counter = 0
        while counter != 5:
            new_farm = savefile.readline().strip('\n').split('+')[:-1]
            for i in range(len(new_farm)):
                if new_farm[i] == 'None':
                    new_farm[i] = None
                elif '[' in new_farm[i]: #Detects whether the variable the program is reading is a list aka a seed
                                        #and rips out the seed name and the growth time and makes it into a list instead of a string
                    new_farm[i] = [new_farm[i][2:5],int(new_farm[i][8:9])]
                
            farm[counter] = new_farm
            counter += 1
    return game_vars, farm
    
            
#random price generator
def random_price_gen(seeds):
    seeds['LET']['crop_price'] = random.randint(2,5)
    seeds['POT']['crop_price'] = random.randint(6,12)
    seeds['CAU']['crop_price'] = random.randint(14,18)
    return seeds

            
        



        
            
   

#----------------------------------------------------------------------
#    Main Game Loop
#----------------------------------------------------------------------
while True:
    
    print("----------------------------------------------------------")
    print("Welcome to Sundrop Farm!")
    print()
    print("You took out a loan to buy a small farm in Albatross Town.")
    print("You have 20 days to pay off your debt of $100.")
    print("You might even be able to make a little profit.")
    print("How successful will you be?")
    print("----------------------------------------------------------")
    print('1) Start a new game')
    print('2) Load your saved game')
    print()
    print('0) Exit Game')
# Write your main game loop here
    decision_start_menu = input("Your choice? ")
    try:
        if int(decision_start_menu) != 1 and 2 and 0:
            print('Invalid Input')
            continue
    except:
        print('Invalid Input')
        continue        


    random_price_gen(seeds)
    if int(decision_start_menu) == 1:
        town_decision = 1
        while town_decision != 0 and game_vars['day'] < 21:
            town_decision = in_town(game_vars)
            if town_decision == 1:
                in_shop(game_vars)
            if town_decision == 2:
                in_farm(game_vars, farm, seeds)
            if town_decision == 3:
                end_day(game_vars,farm)
            if town_decision == 9:
                save_game(game_vars, farm)
        if game_vars['day'] == 21:
            if game_vars['money'] - 100 > 0:
                print('You have paid off your debt. Good job dude/girl/idk.')
                print('Your profit is ${}. Good job'.format(game_vars['money'] - 100))
                break  
            if game_vars['money'] - 100 == 0:
                print('You have paid off your debt. Good job dude/girl/idk.')
                print('You have no profit. LOL'.format(game_vars['money'] - 100))
                break
            if game_vars['money'] - 100 < 0:
                print('You tried your best but you did not pay off your debt')
                print('Now you will be sent to the gallows. Bye!')
                break
    if int(decision_start_menu) == 2 and game_vars['day'] < 21:
        try:
            game_vars,farm = load_game(game_vars, farm)
        except:
            print('Your savefile cannot be located or your savefile has been corrupted')
            break
        town_decision = 1
        while town_decision != 0:
            town_decision = in_town(game_vars)
            if town_decision == 1:
                in_shop(game_vars)
            if town_decision == 2:
                in_farm(game_vars, farm, seeds)
            if town_decision == 3:
                end_day(game_vars,farm)
            if town_decision == 9:
                save_game(game_vars, farm)
        if game_vars['day'] == 21:
            if game_vars['money'] - 100 > 0:
                print('You have paid off your debt. Good job dude/girl/idk.')
                print('Your profit is ${}. Good job'.format(game_vars['money'] - 100))
                break  
            if game_vars['money'] - 100 == 0:
                print('You have paid off your debt. Good job dude/girl/idk.')
                print('You have no profit. LOL'.format(game_vars['money'] - 100))
                break
            if game_vars['money'] - 100 < 0:
                print('You tried your best but you did not pay off your debt')
                print('Now you will be sent to the gallows. Bye!')
                break

    if  int(decision_start_menu) == 0:
        break


