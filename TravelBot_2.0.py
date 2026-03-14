import re, random
from colorama import Fore, init

init(autoreset=True)

destinations = {
    "beaches" : ["Bali", "Maldives", "Phuket", "Cox' Bazar"],
    "mountains" : ["Swiss Alps", "Rocky mountains", "Himalayas", "Mount Fuji"],
    "cities" : ["Tokyo", "Paris", "New York", "London"],
    "forests": ["Amazon Rainforest", "Sundarbans", "Samana Peninsula", "Daintree Rainforest"],
    "historic sites": ["Rome's Collesseum", "Athens's Parthenon", "Istanbul's Hagia Sophia Grand Mosque", "The Great Wall of China"]
}

jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do travelers always feel warm? Because all of their destinations are hot spots!",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why do computers overheat? Because they run on Adrenalin!"
]

def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def recommend():
    print(Fore.CYAN + "TravelBot: Beaches, mountains, cities, forests or historic sites?")
    preference = input (Fore.YELLOW + "You: ")
    preference = normalize_input(preference)

    if preference in destinations:
        suggestion = random.choice(destinations[preference])
        print(Fore.GREEN + f"TravelBot: How about {suggestion}?")
        print(Fore.CYAN + "TravelBot: Do you like it? (yes/no)")
        answer = input(Fore.YELLOW + "You: ").lower()

        if answer == "yes":
            print(Fore.GREEN + f"TravelBot: Awesome! Enjoy {suggestion}!")
        elif answer == "no":
            print(Fore.RED + "Let's try another.")
            recommend()
        else:
            print(Fore.RED + "TravelBot: Sorry, I don't have that type of destination.")
            recommend()

def packing_tips_cities():
    print(Fore.CYAN + "TravelBot: Where to? (cities): ")
    location = normalize_input(input(Fore.YELLOW + "You: "))
    print(Fore.CYAN + f"TravelBot: How many days?: ")
    days = input(Fore.YELLOW + "You: ")

    print(Fore.GREEN + f"TravelBot: Packing tips for {days} days in {location} (city):")
    print(Fore.GREEN + "- Pack versatile and comfortable clothes.")
    print(Fore.GREEN + "- Bring chargers/adapters and power banks.")
    print(Fore.GREEN + "- Bring backpack with essential items.")
    print(Fore.GREEN + "- Use maps for navigation.")

def packing_tips_forests():
    print(Fore.CYAN + "TravelBot: Where to? (forest): ")
    location = normalize_input(input(Fore.YELLOW + "You: "))
    print(Fore.CYAN + f"TravelBot: How many days?: ")
    days = input(Fore.YELLOW + "You: ")

    print(Fore.GREEN + f"TravelBot: Packing tips for {days} days in {location} (forest):")
    print(Fore.GREEN + "- Bring insect repellant.")
    print(Fore.GREEN + "- Bring and wear sturdy hiking boots.")
    print(Fore.GREEN + "- Bring backpack with essential items.")
    print(Fore.GREEN + "- Pack a rain jacket.")

def packing_tips_beaches():
    print(Fore.CYAN + "TravelBot: Where to? (beaches): ")
    location = normalize_input(input(Fore.YELLOW + "You: "))
    print(Fore.CYAN + f"TravelBot: How many days?: ")
    days = input(Fore.YELLOW + "You: ")

    print(Fore.GREEN + f"TravelBot: Packing tips for {days} days in {location} (beach):")
    print(Fore.GREEN + "- Bring Sunscreen.")
    print(Fore.GREEN + "- Bring swimwear.")
    print(Fore.GREEN + "- Bring backpack with essential items.")
    print(Fore.GREEN + "- Pack sandals.")


def tell_joke():
    print(Fore.YELLOW + f"TravelBot: {random.choice(jokes)}")

def show_help():
    print(Fore.MAGENTA + "\nI can:")
    print(Fore.GREEN + "- Suggest travel spots (say 'recommendation')")
    print(Fore.GREEN + "- Offer packing tips for cities (say 'urban packing')")
    print(Fore.GREEN + "- Offer packing tips for forests (say 'nature packing')")
    print(Fore.GREEN + "- Offer packing tips for beaches (say 'beach packing')")
    print(Fore.GREEN + "- Tell a joke (say 'joke')")
    print(Fore.CYAN + "Type 'exit' or 'bye' to end. \n")

def chat():
    print(Fore.CYAN + "Hello! I'm TravelBot.")
    name = input(Fore.YELLOW + "Your name?: ")
    print(Fore.GREEN + f"Nice to meet you, {name}!")

    show_help()

    while True:
        user_input = input(Fore.YELLOW + f"{name}:")
        user_input = normalize_input(user_input)

        if "recommend" in user_input or "suggest" in user_input:
            recommend()
        elif "city packing" in user_input or "urban packing" in user_input:
            packing_tips_cities()
        elif "nature packing" in user_input or "forest packing" in user_input:
            packing_tips_forests()
        elif "beach packing" in user_input or "seashore packing" in user_input or "shore packing" in user_input:
            packing_tips_beaches()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "help" in user_input:
            show_help()
        elif "exit" in user_input or "bye" in user_input:
            print(Fore.CYAN + "TravelBot: Safe travels! Goodbye!")
            break
        else:
            print(Fore.RED + "TravelBot: Could you rephrase?")

chat()