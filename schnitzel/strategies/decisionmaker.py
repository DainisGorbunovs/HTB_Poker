from treys import Evaluator
from treys import Card
import random
from random import randint

evaluator = Evaluator()

MAXSCORE = 7462

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

allCards = [ "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "Ts", "Js", "Qs", "Ks", "As",
                "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "Th", "Jh", "Qh", "Kh", "Ah",
                "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "Td", "Jd", "Qd", "Kd", "Ad",
                "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "Tc", "Jc", "Qc", "Kc", "Ac"]

# Returns 0 for fold, 1 for check/call, 2 for raide
def valueCompare(val, a):
    if val<a[0]:
        return 0
    elif val<a[1]:
        return 1
    else:
        return 2

def raiseAmount(currentMoney, callAmount, raisePercent):
    return round(min(currentMoney, callAmount + currentMoney * raisePercent))

def callAmount(currentMoney, callAmount):
    return round(min(currentMoney, callAmount))

def playerScore(community, hand):
    return (evaluator.evaluate(community, hand) / MAXSCORE)

def randCommunity(community):
    if len(community) == 3:
        hand = [Card.new(allCards[randint(0, 51)]), Card.new(allCards[randint(0, 51)])]
    elif len(community) == 4:
        hand = [Card.new(allCards[randint(0, 51)])]
    else:
        hand = []
    return evaluator.evaluate(community, hand) / MAXSCORE

def communityScore(community):
    averageScore = 0
    for i in range(10):
        averageScore += 0.1 * randCommunity(community)
    return averageScore

def overallScore(community, hand, stakePercent):
    if stakePercent < 0.03:
        risk = 1.2
    elif stakePercent < 0.1:
        risk = 1
    elif stakePercent < 0.3:
        risk = 0.8
    else:
        risk = 0.6
    print("player score: %8f community score: %8f risk: %8f" % (playerScore(community, hand), communityScore(community), risk))
    return playerScore(community, hand) / communityScore(community) * risk



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
def decision(community, hand, bidAmount, currentMoney):

    if len(community) == 0:
        return ["raise", int(max(round(bidAmount*1.1), 10))]

    stakePercent = bidAmount / currentMoney
    score = overallScore(community, hand, stakePercent)
    print("The score for this hand is: %8f" % score)
    if score < 0.6:
        betValue = 0.2 * currentMoney
        if betValue > bidAmount:
            return ["raise", int(betValue - bidAmount)]
        else:
            if bidAmount == 0:
                return ["check", 0]
            else:
                return ["call", 0]
    elif score < 1:
        betValue = 0.1 * currentMoney
        if betValue > bidAmount:
            return ["raise", int(betValue - bidAmount)]
        else:
            if bidAmount == 0:
                return ["check", 0]
            else:
                return ["call", 0]
    else:
        betValue = 0.05 * currentMoney
        if betValue >= bidAmount:
            if bidAmount == 0:
                return ["check", 0]
            else:
                return ["call", 0]
        else:
            return ["fold", 0]



if __name__ == "__main__":
    board = [Card.new('Jh'), Card.new('Ad'), Card.new('3s')]
    hand = [Card.new('4s'), Card.new('Jc')]

    #print(evaluator.evaluate(board, hand))

    #stakePercent = 0.1
    #ovScore = overallScore(board, hand, stakePercent)
    #print("Your overall score is: %10f" % ovScore)
    dec = decision(board, hand, 5, 1000)
    print(dec[0], dec[1])