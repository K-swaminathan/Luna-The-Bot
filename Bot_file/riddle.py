import random


def riddlegame():
    # Function to create a riddle
    def create_riddle():
        riddle = input("Enter your riddle: ")
        answer = input("Enter the answer to your riddle: ")
        with open("../venv/riddles.txt", "a") as file:
            file.write(f"Riddle: {riddle}\nAnswer: {answer}\n\n")
        print("Riddle added!")

    # Function to solve a random riddle
    def solve_riddle():
        riddles = []
        with open("../venv/riddles.txt", "r") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith("Riddle:"):
                    riddle = lines[i][8:].strip()
                    answer = lines[i + 1][7:].strip()
                    riddles.append((riddle, answer))
                    i += 2
                else:
                    i += 1

        if not riddles:
            print("There are no riddles to solve. You can create one!")
            return

        riddle, answer = random.choice(riddles)
        print("Here's a riddle for you:")
        print(riddle)
        user_guess = input("Your answer: ").strip().lower()

        if user_guess == answer.lower():
            print("Correct! You solved the riddle.")
        else:
            print(f"Sorry, the correct answer is '{answer}'.")

    # Main menu
    print("Welcome to the Riddle Game!")
    while True:

        print("\nChoose an option:")
        print("(a). Create a riddle")
        print("(b). Solve a riddle")
        print("(c). Exit")

        choice = input("Enter your choice (a/b/c): ")

        if choice == "a":
            create_riddle()
        elif choice == "b":
            solve_riddle()
        elif choice == "c":
            print("Goodbye, have a nice day!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    riddlegame()
