from functools import  partial
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.lang import Builder


Builder.load_file('interface.kv')

class Board(FloatLayout):
    pass

class GamerInterface(FloatLayout):
    def on_touch_down(self, touch):
        if self.parent.state == 'play':
            l = self.children[::-1]
            for child in l:
                if child.collide_point(*touch.pos):
                    if child.state == 'in_hand':
                        child.state = 'selected'
                    elif child.state == 'selected':
                        child.state = 'in_hand'
                    return
        return super(GamerInterface, self).on_touch_down(touch)

    def check_card_state(self, card):
        d = card.pos_hint.copy()
        if card.state == 'selected':
            d['y'] = 0.05
            card.pos_hint = d
        elif card.state == 'in_hand':
            d['y'] = 0.01
            card.pos_hint = d

    def lay_cards(self):
        self.children.sort()
        children = self.children[:]
        self.clear_widgets()
        num = len(children)
        center = 0.52 - num * 0.02
        for child in children:
            child.pos_hint = {'center_x': center + 0.04 * children.index(child), 'y': 0.01}
            self.add_widget(child)

    def get_last3cards(self):
        self.parent.deck[0].show_back = False
        self.parent.deck[1].show_back = False
        self.parent.deck[2].show_back = False
        ani0 = Animation(duration=1)
        ani1 = ani0 + Animation(pos_hint={'center_x': 0.5, 'center_y': 0.124}, duration=0.2, t='in_sine')
        ani1.bind(on_complete=partial(self.parent.player_a.get_card, self.parent.deck[0]))
        ani2 = ani0 + Animation(pos_hint={'center_x': 0.5, 'center_y': 0.124}, duration=0.2, t='in_sine')
        ani2.bind(on_complete=partial(self.parent.player_a.get_card, self.parent.deck[1]))
        ani3 = ani0 + Animation(pos_hint={'center_x': 0.5, 'center_y': 0.124}, duration=0.2, t='in_sine')
        ani3.bind(on_complete=partial(self.parent.player_a.get_card, self.parent.deck[2]))
        ani3.bind(on_complete = partial(lambda x,y:setattr(self.parent,'state','play')))
        ani1.start(self.parent.deck[0])
        ani2.start(self.parent.deck[1])
        ani3.start(self.parent.deck[2])
        self.parent.deck = []



class LeftInterface(FloatLayout):
    def lay_cards(self):
        self.children.sort()
        children = self.children[:]
        self.clear_widgets()
        for child in children:
            child.show_back = True
            child.pos_hint = {'center_x': 0.1, 'center_y': 0.7 - 0.01 * children.index(child)}
            self.add_widget(child)

    def get_last3cards(self):
        self.parent.deck[0].show_back = False
        self.parent.deck[1].show_back = False
        self.parent.deck[2].show_back = False

        ani0 = Animation(duration=1)
        ani1 = ani0 + Animation(pos_hint={'center_x': 0.1, 'center_y': 0.7}, duration=0.2, t='in_sine')
        ani1.bind(on_complete=partial(self.parent.player_c.get_card, self.parent.deck[0]))
        ani2 = ani0 + Animation(pos_hint={'center_x': 0.1, 'center_y': 0.7}, duration=0.2, t='in_sine')
        ani2.bind(on_complete=partial(self.parent.player_c.get_card, self.parent.deck[1]))
        ani3 = ani0 + Animation(pos_hint={'center_x': 0.1, 'center_y': 0.7}, duration=0.2, t='in_sine')
        ani3.bind(on_complete=partial(self.parent.player_c.get_card, self.parent.deck[2]))
        ani3.bind(on_complete=partial(lambda x, y: setattr(self.parent, 'state', 'play')))

        ani1.start(self.parent.deck[0])
        ani2.start(self.parent.deck[1])
        ani3.start(self.parent.deck[2])
        self.parent.deck = []

class RightInterface(FloatLayout):
    def lay_cards(self):
        self.children.sort()
        children = self.children[:]
        self.clear_widgets()
        for child in children:
            child.show_back = True
            child.pos_hint = {'center_x': 0.9, 'center_y': 0.7 - 0.01 * children.index(child)}
            self.add_widget(child)

    def get_last3cards(self):
        self.parent.deck[0].show_back = False
        self.parent.deck[1].show_back = False
        self.parent.deck[2].show_back = False

        ani0 = Animation(duration=1)
        ani1 = ani0 + Animation(pos_hint={'center_x': 0.9, 'center_y': 0.7}, duration=0.2, t='in_sine')
        ani1.bind(on_complete=partial(self.parent.player_b.get_card, self.parent.deck[0]))
        ani2 = ani0 + Animation(pos_hint={'center_x': 0.9, 'center_y': 0.7}, duration=0.2, t='in_sine')
        ani2.bind(on_complete=partial(self.parent.player_b.get_card, self.parent.deck[1]))
        ani3 = ani0 + Animation(pos_hint={'center_x': 0.9, 'center_y': 0.7}, duration=0.2, t='in_sine')
        ani3.bind(on_complete=partial(self.parent.player_b.get_card, self.parent.deck[2]))
        ani3.bind(on_complete=partial(lambda x, y: setattr(self.parent, 'state', 'play')))

        ani1.start(self.parent.deck[0])
        ani2.start(self.parent.deck[1])
        ani3.start(self.parent.deck[2])
        self.parent.deck = []


class BidInterface(FloatLayout):

    def __init__(self,game,**kwargs):
        super(BidInterface,self).__init__(**kwargs)
        self.game = game

    def on_touch_down(self, touch):
        if self.game.turn == 'player_a':
            if self.ids._pass.collide_point(*touch.pos):
                self.game.bid_message = self.game.player_a.bid(0)
            elif self.ids.stake_1.collide_point(*touch.pos):
                if self.game.stake < 1:
                    self.game.bid_message = self.game.player_a.bid(1)
            elif self.ids.stake_2.collide_point(*touch.pos):
                if self.game.stake < 2:
                    self.game.bid_message = self.game.player_a.bid(2)
            elif self.ids.stake_3.collide_point(*touch.pos):
                if self.game.stake < 3:
                    self.game.bid_message = self.game.player_a.bid(3)

    def animation(self,player,stake):
        if player == 'player_a':
            self.game.bid_result[0] = stake
            if stake == 0:
                ani = Animation(pos_hint={'center_x': 0.49, 'center_y': 0.5}, t='in_bounce', duration=0.1)
                ani += Animation(pos_hint={'center_x': 0.51, 'center_y': 0.5}, t='in_bounce', duration=0.1)
                ani += Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, t='in_bounce', duration=0.1)
                ani.bind(on_complete = self.game.check_bid_result)
                ani.start(self.ids.player_a)
            elif stake in (1,2,3):
                ani = Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5},duration=0.5)
                ani &= Animation(size_hint=(0.05,0.05),duration=0.5)
                ani &= Animation(opacity=1, duration=0.5)
                ani.bind(on_complete=self.game.check_bid_result)
                if stake ==1:
                    ani.start(self.ids.bid_1stake)
                elif stake ==2:
                    ani.start(self.ids.bid_2stake)
                elif stake == 3:
                    ani.start(self.ids.bid_3stake)
        elif player == 'player_b':
            self.game.bid_result[1] = stake
            if stake == 0:
                ani = Animation(pos_hint={'center_x': 0.54, 'center_y': 0.58}, t='in_bounce', duration=0.1)
                ani += Animation(pos_hint={'center_x': 0.56, 'center_y': 0.58}, t='in_bounce', duration=0.1)
                ani += Animation(pos_hint={'center_x': 0.55, 'center_y': 0.58}, t='in_bounce', duration=0.1)
                ani.bind(on_complete=self.game.check_bid_result)
                ani.start(self.ids.player_b)
            elif stake in (1,2,3):
                ani = Animation(pos_hint={'center_x': 0.55, 'center_y': 0.58},duration=0.5)
                ani &= Animation(size_hint=(0.05,0.05),duration=0.5)
                ani &= Animation(opacity=1, duration=0.5)
                ani.bind(on_complete=self.game.check_bid_result)
                if stake ==1:
                    ani.start(self.ids.bid_1stake)
                elif stake ==2:
                    ani.start(self.ids.bid_2stake)
                elif stake == 3:
                    ani.start(self.ids.bid_3stake)
        elif player == 'player_c':
            self.game.bid_result[2] = stake
            if stake == 0:
                ani = Animation(pos_hint={'center_x': 0.44, 'center_y': 0.58}, t='in_bounce', duration=0.1)
                ani += Animation(pos_hint={'center_x': 0.46, 'center_y': 0.58}, t='in_bounce', duration=0.1)
                ani += Animation(pos_hint={'center_x': 0.45, 'center_y': 0.58}, t='in_bounce', duration=0.1)
                ani.bind(on_complete=self.game.check_bid_result)
                ani.start(self.ids.player_c)
            elif stake in (1,2,3):
                ani = Animation(pos_hint={'center_x': 0.45, 'center_y': 0.58},duration=0.5)
                ani &= Animation(size_hint=(0.05,0.05),duration=0.5)
                ani &= Animation(opacity=1, duration=0.5)
                ani.bind(on_complete=self.game.check_bid_result)
                if stake ==1:
                    ani.start(self.ids.bid_1stake)
                elif stake ==2:
                    ani.start(self.ids.bid_2stake)
                elif stake == 3:
                    ani.start(self.ids.bid_3stake)




