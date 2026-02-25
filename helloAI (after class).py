print("Hello there! What is the name of yours?")

name = input()

print(f"Hi {name}! How are you feeling today?")

mood = input().lower()

if mood == 'good':
    print('I see! A good mood is healthy for your mental well-being.')
elif mood == 'bad':
    print("I'm sorry to hear that!")
elif mood == 'sad':
    print("Don't be sad!")
elif mood == 'happy':
    print("Nice! Always try to be happy!")
elif mood == 'calm':
    print("Good! Being calm brings peace to the mind.")
elif mood == 'angry':
    print("I'm sorry to hear that! Try to calm down and cool your mind!")
else:
    print("I see, it's sometimes hard to put feelings into words.")

print("Well, it was nice talking to you. Bye!")