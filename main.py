from functools import partial
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import ListProperty,ObjectProperty,NumericProperty,BooleanProperty,OptionProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from card import Card,deck

DEALSOUND = SoundLoader.load('deal.ogg')

class EntryCards(FloatLayout):
    pass


class LeftAICards(EntryCards):
    pass

class RightAICards(EntryCards):
    pass



class PlayerCards(EntryCards):
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
        return super(PlayerCards,self).on_touch_down(touch)

    def check_card_state(self,card):
        d = card.pos_hint.copy()
        if card.state == 'selected':
            d['y'] = 0.05
            card.pos_hint = d
        elif card.state == 'in_hand':
            d['y'] = 0.01
            card.pos_hint = d

class PlayerHud1(FloatLayout):
    def on_touch_down(self, touch):
        if self.parent.state == 'bid':
            if self.ids._pass.collide_point(*touch.pos):
                print('hello')
            elif self.ids.stake_1.collide_point(*touch.pos):
                self.parent.stake = 1
            elif self.ids.stake_2.collide_point(*touch.pos):
                self.parent.stake = 2
            elif self.ids.stake_3.collide_point(*touch.pos):
                self.parent.stake = 3
                self.parent.landlord = 'player'
                self.parent.show_leftover_cards()
            return
        return super(PlayerHud1,self).on_touch_down(touch)

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
        return super(PlayerHud2,self).on_touch_down(touch)

class LandlordIcon(FloatLayout):
    pass

class Game(FloatLayout):
    player_cards= ObjectProperty()
    left_ai_cards= ObjectProperty()
    right_ai_cards= ObjectProperty()
    player_table_cards = ObjectProperty()
    state = OptionProperty('deal',options = ('deal','bid','play','over'))
    turn = OptionProperty('player',options =('player','right_ai','left_ai'))

    def __init__(self,**kwargs):
        super(Game,self).__init__(**kwargs)
        self.landlord = None
        self.peasants = None
        self.multiple = 1
        self.stake = 1

        self.deck = deck()
        for card in self.deck:
            card.pos_hint = {'center_x':0.5,'center_y':0.5}
            card.show_back = True
            self.add_widget(card)
        self.deal_num = 0
        self.deal()




    def deal(self,*args):
        DEALSOUND.play()
        if self.deal_num < 51:
            card = self.deck[-1]
            if self.deal_num % 3 == 0:
                ani = Animation(pos_hint = {'center_x': 0.5,'center_y':0.124},duration=0.1)
                ani.bind(on_complete = partial(self.player_get_card,card))
            elif self.deal_num % 3 == 1:
                ani = Animation(pos_hint={'center_x': 0.9, 'center_y': 0.7},duration=0.1)
                ani.bind(on_complete = partial(self.right_ai_get_card,card))
            elif self.deal_num % 3 == 2:
                ani = Animation(pos_hint={'center_x': 0.1, 'center_y': 0.7},duration=0.1)
                ani.bind(on_complete = partial(self.left_ai_get_card,card))
            ani.start(card)
            self.deck.pop()
            self.deal_num += 1
        elif self.deal_num >= 51:
            ani1 = Animation(pos_hint = {'center_x': 0.3,'center_y':0.75},duration=0.1)
            ani2 = Animation(pos_hint={'center_x': 0.5, 'center_y': 0.75}, duration=0.1)
            ani3 = Animation(pos_hint={'center_x': 0.7, 'center_y': 0.75}, duration=0.1)
            ani1.start(self.deck[2])
            ani2.start(self.deck[1])
            ani3.start(self.deck[0])
            self.deal_num = 0
            self.state = 'bid'
            self.turn = 'player'

    def left_ai_get_card(self,card,*args):
        card.parent.remove_widget(card)
        self.left_ai_cards.add_widget(card)
        if self.landlord!='left_ai':
            self.deal(*args)

    def right_ai_get_card(self,card,*args):
        card.parent.remove_widget(card)
        self.right_ai_cards.add_widget(card)
        if self.landlord!='right_ai':
            self.deal(*args)

    def player_get_card(self,card,*args):
        card.parent.remove_widget(card)
        card.show_back = False
        self.player_cards.add_widget(card)
        if self.landlord!='player':
            self.deal(*args)

    def on_state(self,*args):
        if self.state == 'bid':
            self.p_hud1 = PlayerHud1()
            self.add_widget(self.p_hud1)
        if self.state == 'play':
            self.p_hud2 = PlayerHud2()
            self.remove_widget(self.p_hud1)
            lordicon = LandlordIcon()
            self.add_widget(lordicon)
            self.add_widget(self.p_hud2)

    def on_turn(self,*args):
        pass

    def show_leftover_cards(self):
        self.deck[0].show_back = False
        self.deck[1].show_back = False
        self.deck[2].show_back = False
        if self.landlord == 'player':
            ani0 = Animation(duration = 0.8)
            ani1 =  ani0+ Animation(pos_hint={'center_x': 0.5, 'center_y': 0.124}, duration=0.2,t='in_sine')
            ani1.bind(on_complete=partial(self.player_get_card, self.deck[0]))
            ani2 = ani0+Animation(pos_hint={'center_x': 0.5, 'center_y': 0.124}, duration=0.2,t='in_sine')
            ani2.bind(on_complete=partial(self.player_get_card, self.deck[1]))
            ani3 = ani0+Animation(pos_hint={'center_x': 0.5, 'center_y': 0.124}, duration=0.2,t='in_sine')
            ani3.bind(on_complete=partial(self.player_get_card, self.deck[2]))
            ani3.bind(on_complete = lambda x,y:setattr(self,'state','play'))
        ani1.start(self.deck[0])
        ani2.start(self.deck[1])
        ani3.start(self.deck[2])
        self.deck =[]



class PlayerTableCards(FloatLayout):
    pass


class DoudizhuApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    Window.size = (800,480)
    DoudizhuApp().run()
