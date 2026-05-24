import requests
import random 
import html
import time

CATAGORY_ID = 9
AMOUNT = 10


def get_questions(difficulty):
    API_URL = (f"https://opentdb.com/api.php?"
               f"amount={AMOUNT}&category={CATAGORY_ID}"f"&difficulty={difficulty}&type=multiple")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()

        data = response.json()
        
        if data["response_code"] == 0:
            return data["results"]
    except requests.excpetions.RequestException:
        print("\nError: Could not fetch question.")

        
    return None

def calculate_grade(percentage):
   if percentage >= 90:
    return "A+"
   elif percentage >= 80:
    return "A"
   elif percentage >= 70:
    return "B"
   elif percentage >= 60:
    return "C"
   else:
    return "F"
   
def ask_question(number, q):
    question = html.unescape(q["question"])
    
    correct = html.unescape(q["correct_answer"])
    
    incorrects = [html.unescape(ans) for ans in q["incorrect_answers"]]

    options = incorrects + [correct]
    random.shuffle(options)

    print(f"\nQuestion {number}")
    print("-" * 20)
    print(question)

    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")

    start_time = time.time()

    while True:
        try:
          choice = int(input("\nYour answer (1-4): "))

          if 1 <= choice <= 4:
             break
          
          print("Please enter a number from 1 to 4.")

        except ValueError:
          print("Invalid input! Enter a number between 1 & 4.")

    end_time = time.time()
    time_taken = end_time - start_time

    if options[choice - 1] == correct:
       print("Correct!")
       print(f"Answered in {time_taken:.1f} seconds")
       return 1
    
    else:
       print("Wrong!")
       print(f"Correct Answer: {correct}")
       return 0
    
def run_quiz():
    print("~" * 20)
    print("Welcome To The Trivia Game!")
    print("~" * 20)

    difficulties = ["easy", "medium", "hard"]

    while True:
       difficulty = input("\nChoose difficulty (easy/medium/hard): ".lower())

       if difficulty in difficulties:
          break
       
       print("Invalid difficulty!")

    questions = get_questions(difficulty)

    if not questions:
       print("Failed to fetch questions.")
       return
    
    score = 0

    for i, q in enumerate(questions, start = 1):
       score += ask_question(i, q)

    percentage = (score / len(questions)) * 100
    grade = calculate_grade(percentage)

    print("\n" + "=" * 50)
    print("QUIZ COMPLETE")
    print("=" * 50)

    print(f"Score: {score}/{len(questions)}")
    print(f"Percentage: {percentage:.1f}%")
    print(f"Grade: {grade}")

    if percentage == 100:
       print("Perfect score!")
    elif percentage >= 70:
       print("Great job!")
    else:
       print("Keep Going!")

while True:
    run_quiz()

    play_again = input("\nPlay again? (yes/no): ").lower()

    if play_again != "yes":
       print("\nThanks for playing!")
       break