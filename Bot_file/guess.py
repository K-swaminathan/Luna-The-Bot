import random


def guessing_game():
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    print("Welcome to the Guessing Game!\nI'm thinking of a number between 1 and 100. Can you guess it?")

    while attempts < max_attempts:
        try:
            guess = input("Enter your guess: ")

            if guess.lower() == 'enough':
                print("Chatbot: Okay, let's stop the game.")
                break

            guess = int(guess)

        except ValueError:
            print("Chatbot: Please enter a valid number.")
            continue

        attempts += 1

        if guess < secret_number:
            print("Chatbot: Too low! Try again.")
        elif guess > secret_number:
            print("Chatbot: Too high! Try again.")
        else:
            print(f"Chatbot: Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
            continue
    if attempts >= max_attempts:
        print(f"Chatbot: Sorry, you've used all {max_attempts} attempts. The secret number was {secret_number}.")


if __name__ == "__main__":
    guessing_game()
