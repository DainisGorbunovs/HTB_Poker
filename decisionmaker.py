from treys import Evaluator
from treys import Card
import random

evaluator = Evaluator()

# Probabilities for Case 1 (fold / call)
case1 = [[0.7, 1],
         [0.65, 1],
         [0.25, 0.9],
         [0.1, 0.85],
         [0.1, 0.7],
         [0.1, 0.5],
         [0.1, 0.7],
         [0.05, 0.35],
         [0.05, 0.25]
         ]
# Probabilities for Case 2 (fold / check)
case2 = [[0, 0.8],
         [0, 0.75],
         [0, 0.7],
         [0, 0.6],
         [0, 0.5],
         [0, 0.4],
         [0, 0.6],
         [0, 0.2],
         [0, 0.1]
         ]

raisePercentage = [0.03,
                   0.05,
                   0.08,
                   0.09,
                   0.1,
                   0.12,
                   0.15,
                   0.2,
                   0.3]

# Returns 0 for fold, 1 for check/call, 2 for raise
def valueCompare(val, a):
    if val<a[0]:
        return 0
    elif val<a[1]:
        return 1
    else:
        return 2

def raiseAmount(currentMoney, callAmount, i):
    return round(min(currentMoney, callAmount + currentMoney * raisePercentage[i]))

def callAmount(currentMoney, callAmount):
    return round(min(currentMoney, callAmount))

# method makes a decision (check/raise/call/fold) based on:
#   @community, the cards on the board
#   @hand, the cards in the hand
#   @case, 1 if we have to respond to a bet, 2 if there are no bets
#   @bidAmount, the amount of money that we have to call, or 0 if there are no bets
#   And returns the following:
#   ["fold", 0] if we should fold
#   ["check", 0] if we should check
#   ["call", value] if we should call (to the value specified)
#   ["raise", value] if we should raise (to the value specified)
def decision(community, hand, case, bidAmount, currentMoney):
    score = evaluator.evaluate(community, hand)
    randomVal = random.uniform(0, 1)
    if score>5000:
        i = 0
    elif score>4000:
        i = 1
    elif score>2500:
        i = 2
    elif score>2100:
        i = 3
    elif score>1800:
        i = 4
    elif score>1300:
        i = 5
    elif score>400:
        i = 6
    elif score>200:
        i = 7
    else:
        i = 8

    if case == 1:
        result = valueCompare(randomVal, case1[i])
        if result == 0:
            return ["fold", 0]
        elif result == 1:
            callVal = callAmount(currentMoney, bidAmount)
            if callVal == currentMoney:
                return ["all-in", callVal]
            else:
                return ["call", callVal]
        else:
            raiseVal = raiseAmount(currentMoney, bidAmount, i)
            if raiseVal == currentMoney:
                return ["all-in", raiseVal]
            else:
                return ["raise", raiseVal]
    else:
        result = valueCompare(randomVal, case2[i])
        if result == 0:
            return ["fold", 0]
        elif result == 1:
            return ["check", 0]
        else:
            raiseVal = raiseAmount(currentMoney, bidAmount, i)
            if raiseVal == currentMoney:
                return ["all-in", raiseVal]
            else:
                return ["raise", raiseVal]

if __name__ == "__main__":
    board = [Card.new('Ah'), Card.new('9d'), Card.new('7c')]
    hand = [Card.new('9s'), Card.new('Ad')]

    dec = decision(board, hand, 1, 10, 100)
    print(dec[0], dec[1])