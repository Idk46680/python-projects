import random
import colorama
from colorama import init, Fore, Style

init()

choices = ['rock', 'paper', 'scissors']

def user_choice():
    user_move = input(Fore.CYAN + "Choose rock, paper or scissors: " + Style.RESET_ALL).lower()

    if user_move not in choices:
        print(Fore.RED + "Invalid choice! Try again!" + Style.RESET_ALL)
        return user_choice()
    
    return user_move

def ai_choice():
    return random.choice(choices)

def decide_winner(user, ai):
    if user == ai:
        print(Fore.YELLOW + "It's a tie!" + Style.RESET_ALL)

    elif (user == "rock" and ai == "scissors") or \
         (user == "paper" and ai == "rock") or \
         (user == "scissors" and ai == "paper"):
        print(Fore.GREEN + "Player wins!" + Style.RESET_ALL)

    else:
        print(Fore.RED + "AI wins!" + Style.RESET_ALL)

def play_again():
    choice = input(Fore.MAGENTA + "Play again? (yes/no): " + Style.RESET_ALL)

    if choice == 'yes':
        return True
    elif choice == 'no':
        return False
    
    else:
        print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
        return play_again()


def play_game():
    print(Fore.MAGENTA + "--- ~ Rock Paper Scissors ~ ---" + Style.RESET_ALL)

    user_input = user_choice()
    ai_input = ai_choice()
        
    print(Fore.BLUE + f"Computer chose: {ai_input}" + Style.RESET_ALL)

    decide_winner(user_input, ai_input)

while True:
    play_game()
    if not play_again():
        break