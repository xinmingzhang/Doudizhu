from itertools import cycle
from functools import partial
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import ListProperty, ObjectProperty, NumericProperty, BooleanProperty, OptionProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from card import Card, deck

from gamer import Gamer
from ai import AI
from interface import BidInterface

DEALSOUND = SoundLoader.load('deal.ogg')





class PlayerHud2(FloatLayout):
    def on_touch_down(self, touch):
        if self.parent.state == 'play':
            if self.ids.pass_.collide_point(*touch.pos):
                pass
            elif self.ids.play_.collide_point(*touch.pos):
                l = []
                for child in self.parent.player_cards.children:
                    if child.state == 'selected':
                        l.append(child)
                print(l)
                for child in l:
                    self.parent.player_cards.remove_widget(child)
                    self.parent.player_table_cards.add_widget(child)
            return
        return super(PlayerHud2, self).on_touch_down(touch)


class LandlordIcon(FloatLayout):
    pass


class Game(FloatLayout):

    player_a = ObjectProperty()
    player_b = ObjectProperty()
    player_c = ObjectProperty()

    player_table_cards = ObjectProperty()

    state = OptionProperty('start', options=('start','deal', 'bid', 'play', 'over'))
    turn = OptionProperty('player_a',options=('player_a','player_b','player_c'))
    bid_result = ListProperty([-1,-1,-1])


    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.player_a = Gamer(self)
        self.player_b = AI(self,'right')
        self.player_c = AI(self,'left')

        self.orders = cycle(['player_a','player_b','player_c'])
        self.turn = next(self.orders)

        self.add_widget(self.player_a.interface)
        self.add_widget(self.player_b.interface)
        self.add_widget(self.player_c.interface)

        self.state = 'deal'





    def on_state(self, *args):
        if self.state == 'deal':
            self.deck = deck()
            for card in self.deck:
                card.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
                card.show_back = True
                self.add_widget(card)
            self.deal_num = 0
            self.deal()

        elif self.state == 'bid':
            self.landlord = None
            self.stake = max(self.bid_result)
            self.bid_interface = BidInterface(self)
            self.add_widget(self.bid_interface)
            if self.turn == 'player_a':
                pass
            elif self.turn == 'player_b':
                self.player_b.bid()
            elif self.turn == 'player_c':
                self.player_c.bid()

        elif self.state == 'play':
            pass


    def on_bid_result(self,*args):
        self.stake = max(self.bid_result)
        if self.bid_result == [0,0,0]:
            self.remove_widget(self.bid_interface)
            self.state = 'deal'
        elif (self.bid_result[0] > 0 and self.bid_result[1] == self.bid_result[2]== 0) or self.bid_result[0]==3:
            self.player_a.role = 'landlord'
            self.remove_widget(self.bid_interface)
            self.player_a.interface.get_last3cards()
        elif (self.bid_result[1] > 0 and self.bid_result[0] == self.bid_result[2] == 0) or self.bid_result[1]==3:
            self.player_b.role = 'landlord'
            self.remove_widget(self.bid_interface)
            self.player_b.interface.get_last3cards()
        elif (self.bid_result[2] > 0 and self.bid_result[0] == self.bid_result[1] == 0) or self.bid_result[2]==3:
            self.player_c.role = 'landlord'
            self.remove_widget(self.bid_interface)
            self.player_c.interface.get_last3cards()




    def deal(self, *args):
        DEALSOUND.play()
        if self.deal_num < 51:
            card = self.deck[-1]
            if self.deal_num % 3 == 0:
                ani = Animation(pos_hint={'center_x': 0.5, 'center_y': 0.124}, duration=0.1)
                ani.bind(on_complete=partial(self.player_a.get_card, card))
                ani.bind(on_complete = self.deal)
            elif self.deal_num % 3 == 1:
                ani = Animation(pos_hint={'center_x': 0.9, 'center_y': 0.7}, duration=0.1)
                ani.bind(on_complete=partial(self.player_b.get_card, card))
                ani.bind(on_complete=self.deal)
            elif self.deal_num % 3 == 2:
                ani = Animation(pos_hint={'center_x': 0.1, 'center_y': 0.7}, duration=0.1)
                ani.bind(on_complete=partial(self.player_c.get_card, card))
                ani.bind(on_complete=self.deal)
            ani.start(card)
            self.deck.pop()
            self.deal_num += 1

        elif self.deal_num >= 51:
            ani1 = Animation(pos_hint={'center_x': 0.3, 'center_y': 0.8}, duration=0.1)
            ani2 = Animation(pos_hint={'center_x': 0.5, 'center_y': 0.8}, duration=0.1)
            ani3 = Animation(pos_hint={'center_x': 0.7, 'center_y': 0.8}, duration=0.1)
            ani3.bind(on_complete = lambda x,y:setattr(self,'state','bid'))
            ani1.start(self.deck[2])
            ani2.start(self.deck[1])
            ani3.start(self.deck[0])
            self.deal_num = 0
            self.turn = 'player_a'

        else:
            pass








    def on_turn(self, *args):
        if self.state == 'bid':
            if self.turn == 'player_a':
                pass
            elif self.turn == 'player_b':
                self.player_b.bid()
            elif self.turn == 'player_c':
                self.player_c.bid()


class PlayerTableCards(FloatLayout):
    pass


class DoudizhuApp(App):
    def build(self):
        return Game()


if __name__ == '__main__':
    DoudizhuApp().run()
