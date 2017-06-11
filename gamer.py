from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

from interface import GamerInterface

class Gamer(EventDispatcher):
    game = ObjectProperty()
    interface = ObjectProperty()

    def __init__(self,game,name,**kwargs):
        super(Gamer,self).__init__(**kwargs)
        self.game = game
        self.name = name
        self.interface = GamerInterface()
        self.bid_stake = -1
        self.role = 'peasant'

    def get_card(self, card, *args):
        card.parent.remove_widget(card)
        card.show_back = False
        self.interface.add_widget(card)
        self.interface.lay_cards()

    def bid(self,value):
        return [self.name,value]

