import requests

def get_user_info(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    response = requests.get(url)

    if response.status_code == 200:

        # Convert JSON response into Python dictionary
        user_data = response.json()

        print("\nExtracted User Information:")
        print("ID:", user_data["id"])
        print("Name:", user_data["name"])
        print("Username:", user_data["username"])
        print("Email:", user_data["email"])

    else:
        print("Failed to retrieve user information.")


def main():
    print("Welcome to the User Data Extractor!")

    while True:

        user_input = input(
            "\nEnter a user ID (1-10) or type 'q'/'exit' to quit: "
        )

        if user_input.lower() in ("q", "exit"):
            print("Goodbye!")
            break

        if user_input.isdigit():

            user_id = int(user_input)

            if 1 <= user_id <= 10:
                get_user_info(user_id)

            else:
                print("Please enter a number between 1 and 10.")

        else:
            print("Invalid input. Please enter a valid number.")


main()