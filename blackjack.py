import random
import json
import os
from blackjack_art import logo
from cards_visual import print_cards

STATS_FILE = "blackjack_stats.json"


def draw_card():
    card = random.randint(1, 13)

    if card == 1:
        return 11
    if card > 10:
        return 10

    return card


def calculate_sum(cards):
    total = sum(cards)

    while total > 21 and 11 in cards:
        ace_index = cards.index(11)
        cards[ace_index] = 1
        total = sum(cards)

    return total


def ask_user():
    while True:
        answer = input("Would you like to buy another card? (y/n): ").lower()

        if answer in ["y", "n"]:
            return answer

        print("Invalid input. Please enter y or n.")


def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"wins": 0, "losses": 0, "ties": 0, "games": 0}

    with open(STATS_FILE, "r") as file:
        return json.load(file)


def save_stats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)


def update_stats(result):
    stats = load_stats()

    stats["games"] += 1

    if result == "win":
        stats["wins"] += 1
    elif result == "loss":
        stats["losses"] += 1
    elif result == "tie":
        stats["ties"] += 1

    save_stats(stats)


def show_stats():
    stats = load_stats()

    print("\n--- Game Statistics ---")
    print(f"Games played: {stats['games']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Ties: {stats['ties']}")


def computer_should_draw(cpu_sum, user_sum):
    if cpu_sum < 17:
        return True

    if cpu_sum < user_sum:
        return True

    return False


def play_one_round():
    print("\nWelcome to the Blackjack Game!")

    user_cards = [draw_card(), draw_card()]
    user_sum = calculate_sum(user_cards)

    print_cards(user_cards, "Your cards:")
    print(f"Sum is: {user_sum}")

    while user_sum <= 21:
        answer = ask_user()

        if answer == "n":
            break

        user_cards.append(draw_card())
        user_sum = calculate_sum(user_cards)

        print_cards(user_cards, "Your cards:")
        print(f"Sum is: {user_sum}")

    if user_sum > 21:
        print("You Lost!")
        update_stats("loss")
        return

    cpu_cards = [draw_card(), draw_card()]
    cpu_sum = calculate_sum(cpu_cards)

    print_cards([cpu_cards[0]], "Computer visible card:")
    print("Second card is hidden.")

    while computer_should_draw(cpu_sum, user_sum):
        cpu_cards.append(draw_card())
        cpu_sum = calculate_sum(cpu_cards)
        print_cards(cpu_cards, "Computer cards:")
        print(f"Sum is: {cpu_sum}")

    print("\n--- Final Result ---")
    print_cards(user_cards, "Your cards:")
    print(f"Sum is: {user_sum}")
    print_cards(cpu_cards, "Computer cards:")
    print(f"Sum is: {cpu_sum}")

    if cpu_sum > 21:
        print("You Win!")
        update_stats("win")
    elif cpu_sum == user_sum:
        print("It's a tie!")
        update_stats("tie")
    elif user_sum > cpu_sum:
        print("You Win!")
        update_stats("win")
    else:
        print("CPU won!")
        update_stats("loss")


def play_blackjack():
    print(logo)

    while True:
        play_one_round()
        show_stats()

        again = input("\nWould you like to play again? (y/n): ").lower()

        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__": 
    play_blackjack()