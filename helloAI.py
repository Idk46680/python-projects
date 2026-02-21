print("Hello there! What is the name of yours?")

name = input()

print(f"Hi {name}! How are you feeling today?")

mood = input().lower()

if mood == 'good':
    print('I see! A good mood is healthy for your mind.')