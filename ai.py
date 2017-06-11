from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty,ListProperty
from interface import LeftInterface,RightInterface
import random
from itertools import cycle

A = cycle([1,2,3])

class AI(EventDispatcher):
    game = ObjectProperty()
    interface = ObjectProperty()
    cards = ListProperty([])

    def __init__(self,game,name,**kwargs):
        super(AI,self).__init__(**kwargs)
        self.game = game
        self.role = 'peasant'
        self.name = name
        if self.name == 'player_c':
            self.interface = LeftInterface()
        elif self.name == 'player_b':
            self.interface = RightInterface()
        self.bid_stake = -1

    def get_card(self, card, *args):
        card.parent.remove_widget(card)
        self.interface.add_widget(card)
        self.interface.lay_cards()

    def bid(self):
        a = 0
        if a > self.game.stake:
            return [self.name,a]
        else:
            return [self.name,0]

