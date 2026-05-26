import requests

FACT_CATEGORIES = FACT_CATEGORIES = {
    "1": {
        "name": "General",
        "url": "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    },

    "2": {
        "name": "Technology",
        "url": "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    },

    "3": {
        "name": "History",
        "url": "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    },

    "4": {
        "name": "Science",
        "url": "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    }
}

def get_fact(url):
    try:
        response = requests.get(url)
        fact_data = response.json()
        response.raise_for_status()

        print("\nDid you know?")
        print(fact_data["text"])
        print()

    except requests.exceptions.RequestException as e:
        print(f"\nError fetching fact: {e}\n")

def display_categories():
    print("\n----Fact Categories----")

    for key, value in FACT_CATEGORIES.items():
        print(f"{key}. {value['name']}")

    print("Q. Quit")

def main():
    print("Welcome to the Random Useless Fact Fetcher!")

    while True:
        display_categories()

        user_choice = input("\nChoose a Category: ").strip().lower()

        if user_choice == 'q':
            print("\nGoodbye!")
            break

        if user_choice not in FACT_CATEGORIES:
            print("\nInvalid choice. Please try again.\n")
            continue

        selected_category = FACT_CATEGORIES[user_choice]

        print(f"\nFetching a {selected_category['name']} fact...")

        get_fact(selected_category["url"])

main()