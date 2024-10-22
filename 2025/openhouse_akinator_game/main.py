from akinator_python import Akinator
from colorama import Fore, Back, Style

import time
import os
# Clear screen (for decluttering)
def clear():
    if os.name == 'nt': # for windows
        os.system('cls')
    else: # for mac and linux (here, os.name is 'posix')
        os.system('clear')

# Print text character-by-character, ChatGPT-Style
def fancy_print(text: str, speed: float = 0.02):
    for char in text:
        time.sleep(speed)
        print(char, end='', flush=True)
    print() # for the newline


banner = f'''
                                                    {Fore.GREEN}
                        ⢀⣹⣁
                    ⢀⣶⣶⣶⣾⣿⣿⣶⣶⣶⡄
                    ⢨⣿⠉⣉⡉⠉⠉⣉⡉⣿⡇⡄
                    ⢸⣿⣄⣀⣠⣴⣤⣀⣀⣿⡇⠃
                     ⠻⠿⠿⠿⠿⠿⠿⠿⠿⠃                {Style.RESET_ALL}
     ⢸⣿⣿⣿⣿⣿⣿⡇⣿⣿⣇⣴⣿⣿⣿⢠⣶⣶⣶⣶⣶⣶⣶⣶⣶⡄ ⣿⣿⢀⣼⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⢸⣿⡇⢸⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿
     ⢸⣿⣿  ⣿⣿⡇⣿⣿⡇ ⢸⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇ ⣿⣿  ⢸⣿⣿   ⣿⣿   ⢸⣿⡇⢸⣿⡇    ⠻⣿⡇
     ⢸⣿⣿⣤⣤⣿⡿⠃⣿⣿⡇ ⢸⣿⣿⢸⣿⣿⠿⠿⠿⠿⠿⢿⣧⡀ ⣿⣿  ⢸⣿⣿   ⣿⣿   ⢸⣿⡇⢸⣿⡇     ⠈⠃  ⣷⣦
     ⢸⣿⣿⠈⠻⣿⣷⡄⣿⣿⣧⣤⣼⣿⣿⠘⠛⠛⣤⣤⣤⣤⣤⣼⣿⡇ ⣿⣿⣦⣤⣼⣿⣿   ⣿⣿   ⢸⣿⡇⢸⣿⣧⣤⣤⣤⡄⣴⣶⣶⣶⣶⣿⣿
     ⠘⠛⠛  ⠛⠛⠃⠛⠛⠛⠛⠛⠛⠛   ⠿⠿⠿⠿⠿⠿⠿⠃ ⠛⠛⠛⠛⠛⠛⠛   ⠛⠛   ⠘⠛⠃⠘⠛⠛⠛⠛⠛⠃⠛⠛⠛⠛⠛⠛⠛
                    ⢸⣿⣿⣿⣿⣿⢸⣿⡇   ⣿⣿  ⣿⣿ ⣿⣿⣿⣿⣿⣿
                    ⢸⣿⡇   ⢸⣿⡇   ⣿⣿  ⣿⣿ ⣿⣿  ⣿⣿
                    ⢸⣿⡇   ⢸⣿⡇   ⣿⣿  ⣿⣿ ⣿⣿⠻⣿⣿⠉
                    ⢸⣿⣇⣀⣀⣀⢸⣿⣇⣀⣀ ⣿⣿⣀⣀⣿⣿ ⣿⣿⣀⣙⣿⣿
                    ⢸⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿  ⣿⣿⠋⣿⣿ ⣿⣿⣿⣿⣿⣿
'''

print(banner)
fancy_print(f"{Fore.CYAN}{Style.BRIGHT}*psstttt... come to Hillgrove's Openhouse on 23rd November 2024{Style.RESET_ALL}")
fancy_print('''
Hey there! Let's play a simple game. Think of any character, it may be someone from the medieval times all the way up to present day. Your character can even be from a fiction work, so long as your character is sufficiently recognizable\n''')

fancy_print("Have fun, and remember to answer the questions as truthfully as possible.")
print('''
Your answer must be one of these:
    - "y"   for YES
    - "n"   for NO
    - "idk" for I DON'T KNOW
    - "p"   for PROBABLY
    - "pn"  for PROBABLY NOT
    - "b"   for BACK (go back one question)
''')

# Initialisation
aki = Akinator(lang='en')
aki.start_game()

# Main game loop
while True:
    try:
        # print question      "aki.step + 1" for 1-indexing
        print(f"{Fore.YELLOW}Q{aki.step + 1}{Style.RESET_ALL}. {aki.question}")

        # get answer
        ans = input("    ")

        if ans == 'b': # Go back one question
            aki.go_back()
        else:
            # Post answer
            aki.post_answer(ans)

            # If guess is reached
            if aki.answer_id:
                print(f"{aki.name} / {aki.description}")
                ans = input("Is this correct?   ")

                if ans == "n":
                    aki.exclude()
                elif ans == "y":
                    fancy_print(f"{Fore.GREEN}Thanks for playing!{Style.RESET_ALL}")
                    print(f"Full source code can be found at {Fore.CYAN}https://github.com/hgv-rc/projects {Style.RESET_ALL}")
                    break
                else:
                    break


    except Exception as e:
        print(e)
        continue
