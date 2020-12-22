import sys
import numpy as np
import copy
from collections import deque

decks = []
player_deck = []
for line in sys.stdin:
    line = line.strip()
    if line.startswith("Player "):
        if player_deck:
            decks.append(player_deck)
        player_deck = []
    elif line:
        player_deck.append(int(line))
if player_deck:
    decks.append(player_deck)

decks = [deque(deck) for deck in decks]


def score_decks(decks):
    deck = next(deck for deck in decks if len(deck) > 0)
    score = sum((len(deck) - i) * card for i, card in enumerate(deck))
    return score


def play_part1(decks):
    decks = copy.deepcopy(decks)
    while all(len(deck) > 0 for deck in decks):
        cards = [deck.popleft() for deck in decks]
        winner = np.argmax(cards)
        decks[winner].extend(sorted(cards, reverse=True))
    return decks


def play_part2(decks):
    seen = set()
    while all(len(deck) > 0 for deck in decks):
        state = tuple(tuple(deck) for deck in decks)
        if state in seen:
            return 0, decks
        seen.add(state)
        cards = [deck.popleft() for deck in decks]
        if all(c <= len(decks[i]) for i, c in enumerate(cards)):
            # Play recursive combat
            new_decks = [deque(list(decks[i])[:card]) for i, card in enumerate(cards)]
            winner, _ = play_part2(new_decks)
        else:
            winner = np.argmax(cards)
        decks[winner].extend(cards if winner == 0 else cards[::-1])
    winner = next(i for i, deck in enumerate(decks) if len(deck) > 0)
    return winner, decks


print("Part 1:", score_decks(play_part1(decks)))
_, decks = play_part2(decks)
print("Part 2:", score_decks(decks))
