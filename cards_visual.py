import random

SUITS = ["♠", "♥", "♦", "♣"]

def card_to_display(card):
    suit = random.choice(SUITS)

    if card == 11:
        value = "A"
    else:
        value = str(card)

    return [
        "┌─────┐",
        f"│{value:^5}│",
        "│     │",
        f"│{suit:^5}│",
        "└─────┘"
    ]


def print_cards(cards, title):
    print(f"\n{title}")

    card_lines = [card_to_display(card) for card in cards]

    for i in range(5):
        print(" ".join(card[i] for card in card_lines))