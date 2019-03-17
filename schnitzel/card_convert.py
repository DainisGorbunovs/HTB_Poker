from treys import Card


class CardConvert:
    @staticmethod
    def convert_cards(cards: list, use_card_name: bool = True):
        converted_cards = []
        for card in cards:
            card_name = card['rank'].upper()[0] + card['suit'][0]
            if card_name[0] == '1':
                card_name = 'T' + card_name[1]

            card_value = card_name if use_card_name else Card.new(card_name)
            converted_cards.append(card_value)
        return converted_cards
