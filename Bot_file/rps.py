import random


def sample():
    print('Welcome to Rock Paper Scissors Game!\n')
    while True:
        outcome = ["rock", "paper", "scissor"]
        pc = random.choice(outcome)
        user = input("Your turn:")
        print("My turn:", pc)
        if any(keyword in user.lower() for keyword in ["stop", "enough"]):
            print("okay..let's stop the game.")
            break
        elif user.lower() == pc:
            print("Chat-bot: out")
        elif user.lower() == "rock" and pc == "paper":
            print("Chat-bot: I win!")
        elif user.lower() == "rock" and pc == "scissor":
            print("Chat-bot: You win!")
        elif user.lower() == "paper" and pc == "rock":
            print("Chat-bot: You win")
        elif user.lower() == "paper" and pc == "scissor":
            print("Chat-bot: I win")
        elif user.lower() == "scissor" and pc == "rock":
            print("Chat-bot: I win")
        elif user.lower() == "scissor" and pc == "paper":
            print("Chat-bot: You win")
        else:
            print("uhh..I don't understand what you're saying.")
            continue


if __name__ == "__main__":
    sample()
