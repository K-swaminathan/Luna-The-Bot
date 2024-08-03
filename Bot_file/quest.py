import random


def wordgame():
    print(
        "Welcome to the 20 Questions game!\nThink of an object, and I will try to guess what it is.\nYou can also try to guess my object!")

    # Player's object
    player_object = input("Enter your object (e.g., 'banana'): ").lower()

    print("Let's begin!")

    computer_guess = None
    guessed_objects = []  # To keep track of guessed objects

    while computer_guess != player_object:
        computer_guess = generate_guess(guessed_objects)
        if computer_guess is None:
            print("I have run out of guesses. Let's try again!")
            break
        guessed_objects.append(computer_guess)  # Add the guessed object to the list
        print(f"My guess: Is it a {computer_guess}?")

        response = input("Your response (yes, no, I don't know): ").lower()

        if response in ["yes", "yeah", "yea", "yep"]:
            print("I guessed it! I win!")
            break
        elif response in ["no", "nope", "nah"]:
            print("Oh no! I need more clues.")
        else:
            print("I don't understand that response. Please enter 'yes,' 'no,' or 'I don't know'.")

    if computer_guess == player_object:
        print("Congratulations! You guessed it correctly. You win!")


def generate_guess(guessed_objects):
    objects = ["apple", "banana", "car", "dog", "house", "computer", "book", "pen", "cat", "phone", "fruit"]

    # Remove objects that have already been guessed
    available_objects = [obj for obj in objects if obj not in guessed_objects]

    if not available_objects:
        return None

    return random.choice(available_objects)


if __name__ == "__main__":
    wordgame()
