import re

CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}

SCORES = {
    "11111": 1, # high card
    "1112": 2,  # one pair
    "122": 3,   # two pair
    "113": 4,   # 3 of a kind
    "23": 5,    # full house
    "14": 6,    # 4 of a kind
    "5": 7,     # 5 of a kind

    # joker hands
    "1111": 2,  # one pair (1 + 1J)
    "112": 4,   # 3 of a kind (2 + 1J)
    "111": 4,   # 3 of a kind (1 + 2J)
    "22": 5,    # full house (2 + 2 + 1J)
    "13": 6,    # 4 of a kind (3 + 1J)
    "12": 6,    # 4 of a kind (2 + 2J)
    "11": 6,    # 4 of a kind (1 + 3J)
    "4": 7,     # 5 of a kind (4 + 1J)
    "3": 7,     # 5 of a kind (3 + 2J)
    "2": 7,     # 5 of a kind (2 + 3J)
    "1": 7,     # 5 of a kind (1 + 4J)
    "": 7,      # 5 of a kind (5J)
}

def score_hand(hand, jokers_wild=False):
    score = [0]
    cards = {}
    for card in hand:
        if jokers_wild and card == "J":
            score.append(1)
            continue
        if card in CARD_VALUES:
            card = CARD_VALUES[card]
        else:
            card = int(card)
        score.append(card)
        if card in cards:
            cards[card] += 1
        else:
            cards[card] = 1
    score[0] = SCORES[''.join([str(x) for x in sorted(cards.values())])]
    return score

def get_total(jokers_wild=False):   
    scores_and_bets = []
    for line in open("day07_input.txt"):
        m = re.search("(?P<hand>(A|K|Q|J|T|\d)+) (?P<bet>\d+)", line)
        score = score_hand(m.group("hand"), jokers_wild)
        bet = int(m.group("bet"))
        scores_and_bets.append((score, bet))
    scores_and_bets.sort()

    total = 0
    for i in range(len(scores_and_bets)):
        rank = i+1
        bet = scores_and_bets[i][1]
        total += rank * bet
    return total

print("Part 1:", get_total())
print("Part 2:", get_total(jokers_wild=True))