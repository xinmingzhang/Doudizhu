from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import OptionProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_file('card.kv')


class Card(Image):
    '''Suits are irrelevant in game, I just use it to sort the card'''
    suits_value = {'Joker': 0.9,
                   'Spades': 0.8,
                   'Hearts': 0.6,
                   'Clubs': 0.4,
                   'Diamonds': 0.2}

    rank_value = {'color': 20,
                  'black': 18,
                  '2': 16,
                  'A': 14,
                  'K': 13,
                  'Q': 12,
                  'J': 11,
                  '10': 10,
                  '9': 9,
                  '8': 8,
                  '7': 7,
                  '6': 6,
                  '5': 5,
                  '4': 4,
                  '3': 3}

    state = OptionProperty('in_hand', options=('in_hand', 'selected', 'on_table'))
    show_back = BooleanProperty(False)

    def __init__(self, suit, rank, **kwargs):
        self.suit = suit
        self.rank = rank
        super(Card, self).__init__(**kwargs)
        self.value = Card.rank_value[self.rank]
        self.v = self.value
        self.img = './img/card{}{}.png'.format(self.suit, self.rank)
        self.source = self.img

    def __lt__(self, cls):
        return self.value + Card.suits_value[self.suit] > cls.value + Card.suits_value[self.suit]

    def __repr__(self):
        return '{}{}'.format(self.suit, self.rank)

    def on_state(self, *args):
        self.parent.check_card_state(self)

    def on_show_back(self, *args):
        if self.show_back:
            self.source = './img/cardBack_blue4.png'
        else:
            self.source = self.img


def deck():
    deck = []
    for suit in Card.suits_value:
        for rank in Card.rank_value:
            if suit != 'Joker' and rank not in ('color', 'black'):
                deck.append(Card(suit, rank))
    deck.append(Card('Joker', 'color'))
    deck.append(Card('Joker', 'black'))
    import random
    random.shuffle(deck)
    return deck


def check_hands(card_list):
    card_list.sort()
    n = len(card_list)

    if n == 1:
        return {'solo': card_list[0].value}

    elif n == 2:
        if card_list[0].rank == 'color' and card_list[1].rank == 'black':
            return {'rocket': 100}
        elif card_list[0].v == card_list[1].v:
            return {'pair': card_list[0].v}
        else:
            return {'invalid': None}

    elif n == 3:
        if card_list[0].v == card_list[1].v == card_list[2].v:
            return {'trio': card_list[0].v}
        else:
            return {'invalid': None}

    elif n == 4:
        if card_list[0].v == card_list[1].v == card_list[2].v == card_list[3].v:
            return {'bomb': card_list[0].v}
        elif card_list[0].v == card_list[1].v == card_list[2].v:
            return {'trio+solo': card_list[0].v}
        elif card_list[1].v == card_list[2].v == card_list[3].v:
            return {'trio+solo': card_list[1].v}
        else:
            return {'invalid': None}

    elif n == 5:
        if card_list[0].v == card_list[1].v == card_list[2].v and card_list[3].v == card_list[4].v:
            return {'trio+pair': card_list[0].v}
        elif card_list[0].v == card_list[1].v and card_list[2].v == card_list[3].v == card_list[4].v:
            return {'trio+pair': card_list[2].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(5)]:
            return {'5chain': card_list[4].v}
        else:
            return {'invalid': None}

    elif n == 6:
        if card_list[0].v == card_list[1].v == card_list[2].v == card_list[3].v:
            return {'four+2solo': card_list[0].v}
        elif card_list[1].v == card_list[4].v == card_list[2].v == card_list[3].v:
            return {'four+2solo': card_list[1].v}
        elif card_list[5].v == card_list[4].v == card_list[2].v == card_list[3].v:
            return {'four+2solo': card_list[2].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(6)]:
            return {'6chain': card_list[5].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(3) for i in range(2)]:
            return {'3pair_chain': card_list[5].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(2) for i in range(3)]:
            return {'airplane': card_list[3].v}
        else:
            return {'invalid': None}

    elif n == 7:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(7)]:
            return {'7chain': card_list[6].v}
        else:
            return {'invalid': None}

    elif n == 8:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(8)]:
            return {'8chain': card_list[7].v}
        elif check_hands(card_list[0:6]).has_key('airplane'):
            return {'airplane+2solo': card_list[5].v}
        elif check_hands(card_list[1:7]).has_key('airplane'):
            return {'airplane+2solo': card_list[6].v}
        elif check_hands(card_list[2:8]).has_key('airplane'):
            return {'airplane+2solo': card_list[7].v}
        elif check_hands(card_list[0:4]).has_key('bomb') and check_hands(card_list[4:6]).has_key(
                'pair') and check_hands(card_list[6:8]).has_key('pair'):
            return {'four+2pair': card_list[0].v}
        elif check_hands(card_list[2:6]).has_key('bomb') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[6:8]).has_key('pair'):
            return {'four+2pair': card_list[2].v}
        elif check_hands(card_list[4:8]).has_key('bomb') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[2:4]).has_key('pair'):
            return {'four+2pair': card_list[4].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(4) for i in range(2)]:
            return {'4pair_chain': card_list[7].v}
        else:
            return {'invalid': None}

    elif n == 9:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(9)]:
            return {'9chain': card_list[8].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(3) for i in range(3)]:
            return {'3airplane': card_list[8].v}
        else:
            return {'invalid': None}

    elif n == 10:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(10)]:
            return {'10chain': card_list[9].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(5) for i in range(2)]:
            return {'5pair_chain': card_list[9].v}
        elif check_hands(card_list[0:6]).has_key('airplane') and check_hands(card_list[6:8]).has_key(
                'pair') and check_hands(card_list[8:10]).has_key('pair'):
            return {'airplane+2pair': card_list[5].v}
        elif check_hands(card_list[2:8]).has_key('airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[8:10]).has_key('pair'):
            return {'airplane+2pair': card_list[7].v}
        elif check_hands(card_list[4:10]).has_key('airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[2:4]).has_key('pair'):
            return {'airplane+2pair': card_list[9].v}
        else:
            return {'invalid': None}

    elif n == 11:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(11)]:
            return {'11chain': card_list[10].v}
        else:
            return {'invalid': None}

    elif n == 12:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(12)]:
            return {'12chain': card_list[11].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(6) for i in range(2)]:
            return {'6pair_chain': card_list[11].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(4) for i in range(3)]:
            return {'4airplane': card_list[11].v}
        elif check_hands(card_list[0:9]).has_key('3airplane'):
            return {'3airplane+3solo': card_list[8].v}
        elif check_hands(card_list[1:10]).has_key('3airplane'):
            return {'3airplane+3solo': card_list[9].v}
        elif check_hands(card_list[2:11]).has_key('3airplane'):
            return {'3airplane+3solo': card_list[10].v}
        elif check_hands(card_list[3:12]).has_key('3airplane'):
            return {'3airplane+3solo': card_list[11].v}
        else:
            return {'invalid': None}

    elif n == 14:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(7) for i in range(2)]:
            return {'7pair_chain': card_list[13].v}
        else:
            return {'invalid': None}

    elif n == 15:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(5) for i in range(3)]:
            return {'5airplane': card_list[14].v}
        elif check_hands(card_list[0:9]).has_key('3airplane') and check_hands(card_list[9:11]).has_key(
                'pair') and check_hands(card_list[11:13]).has_key('pair') and check_hands(card_list[13:15]).has_key(
            'pair'):
            return {'3airplane+3pair': card_list[8].v}
        elif check_hands(card_list[2:11]).has_key('3airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[11:13]).has_key('pair') and check_hands(card_list[13:15]).has_key(
            'pair'):
            return {'3airplane+3pair': card_list[10].v}
        elif check_hands(card_list[4:13]).has_key('3airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[2:4]).has_key('pair') and check_hands(card_list[13:15]).has_key(
            'pair'):
            return {'3airplane+3pair': card_list[12].v}
        elif check_hands(card_list[6:15]).has_key('3airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[2:4]).has_key('pair') and check_hands(card_list[4:6]).has_key('pair'):
            return {'3airplane+3pair': card_list[14].v}
        else:
            return {'invalid': None}

    elif n == 16:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(8) for i in range(2)]:
            return {'8pair_chain': card_list[15].v}
        elif check_hands(card_list[0:12]).has_key('4airplane'):
            return {'4airplane+4solo': card_list[11].v}
        elif check_hands(card_list[1:13]).has_key('4airplane'):
            return {'4airplane+4solo': card_list[12].v}
        elif check_hands(card_list[2:14]).has_key('4airplane'):
            return {'4airplane+4solo': card_list[13].v}
        elif check_hands(card_list[3:15]).has_key('4airplane'):
            return {'4airplane+4solo': card_list[14].v}
        elif check_hands(card_list[4:16]).has_key('4airplane'):
            return {'4airplane+4solo': card_list[15].v}
        else:
            return {'invalid': None}


    elif n == 18:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(9) for i in range(2)]:
            return {'9pair_chain': card_list[17].v}
        elif [x.v for x in card_list] == [card_list[0].v - x for x in range(6) for i in range(3)]:
            return {'6airplane': card_list[17].v}
        else:
            return {'invalid': None}

    elif n == 20:
        if [x.v for x in card_list] == [card_list[0].v - x for x in range(10) for i in range(2)]:
            return {'10pair_chain': card_list[19].v}
        elif check_hands(card_list[0:15]).has_key('5airplane'):
            return {'5airplane+5solo': card_list[14].v}
        elif check_hands(card_list[1:16]).has_key('5airplane'):
            return {'5airplane+5solo': card_list[15].v}
        elif check_hands(card_list[2:17]).has_key('5airplane'):
            return {'5airplane+5solo': card_list[16].v}
        elif check_hands(card_list[3:18]).has_key('5airplane'):
            return {'5airplane+5solo': card_list[17].v}
        elif check_hands(card_list[4:19]).has_key('5airplane'):
            return {'5airplane+5solo': card_list[18].v}
        elif check_hands(card_list[5:20]).has_key('5airplane'):
            return {'5airplane+5solo': card_list[19].v}
        elif check_hands(card_list[0:12]).has_key('4airplane') and check_hands(card_list[12:14]).has_key(
                'pair') and check_hands(card_list[14:16]).has_key('pair') and check_hands(card_list[16:18]).has_key(
            'pair') and check_hands(card_list[18:20]).has_key('pair'):
            return {'4airplane+4pair': card_list[11].v}
        elif check_hands(card_list[2:14]).has_key('4airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[14:16]).has_key('pair') and check_hands(card_list[16:18]).has_key(
            'pair') and check_hands(card_list[18:20]).has_key('pair'):
            return {'4airplane+4pair': card_list[13].v}
        elif check_hands(card_list[4:16]).has_key('4airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[2:4]).has_key('pair') and check_hands(card_list[16:18]).has_key(
            'pair') and check_hands(card_list[18:20]).has_key('pair'):
            return {'4airplane+4pair': card_list[15].v}
        elif check_hands(card_list[6:18]).has_key('4airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[2:4]).has_key('pair') and check_hands(card_list[4:6]).has_key(
            'pair') and check_hands(card_list[18:20]).has_key('pair'):
            return {'4airplane+4pair': card_list[17].v}
        elif check_hands(card_list[8:20]).has_key('4airplane') and check_hands(card_list[0:2]).has_key(
                'pair') and check_hands(card_list[2:4]).has_key('pair') and check_hands(card_list[4:6]).has_key(
            'pair') and check_hands(card_list[6:8]).has_key('pair'):
            return {'4airplane+4pair': card_list[19].v}
        else:
            return {'invalid': None}

if __name__ == '__main__':
    a = [Card('Spades', '4'),
         Card('Spades', '4'),
         Card('Spades', '5'),
         Card('Spades', '5'),
         Card('Spades', '9'),
         Card('Spades', '9'),
         Card('Spades', '6'),
         Card('Spades', '6'),
         Card('Spades', '7'),
         Card('Spades', '7'),
         Card('Spades', '8'),
         Card('Spades', '8'), ]
    p = check_hands(a)
    print(p)
