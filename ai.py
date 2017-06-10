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

    def __init__(self,game,position,**kwargs):
        super(AI,self).__init__(**kwargs)
        self.game = game
        self.role = 'peasant'
        self.position = position
        if self.position == 'left':
            self.interface = LeftInterface()
        elif self.position == 'right':
            self.interface = RightInterface()
        self.bid_stake = -1

    def get_card(self, card, *args):
        card.parent.remove_widget(card)
        self.interface.add_widget(card)
        self.interface.lay_cards()

    def bid(self):
        a = next(A)
        if a > self.game.stake:
            self.game.bid_interface.animation(self.game.turn,a)
        else:
            self.game.bid_interface.animation(self.game.turn,0)

