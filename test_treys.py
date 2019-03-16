from treys import Card
from treys import Evaluator

card = Card.new('Qh')

board = [
    Card.new('Ah'),
    Card.new('Kd'),
    Card.new('Jc')
]
hand = [
    Card.new('Qs'),
    Card.new('Th')
]

Card.print_pretty_cards(board + hand)


evaluator = Evaluator()
print(evaluator.evaluate(board, hand))
