# Everything related to the card conflict mechanics

init -2 python:
    import random
    import math
    SUITS={u'С':u'Сила',
        u'Д':u'Деньги',
        u'З':u'Знания',
        u'И':u'Интриги'}

    DEFAULT_HISTORY = u'Тебе не известна история этой карты'
    SPENDABLE_COLOR = '#AAA'
    PERMANENT_COLOR = '#DEC666'
    # Card-related classes: card itself and an action

    class Card(renpy.Displayable):
        def __init__(self, suit, number, spendable = False, tooltip = DEFAULT_HISTORY, **kwargs):
            super(Card, self).__init__(xysize=(200, 120), xfill=False, yfill=False, **kwargs)
            self.suit = SUITS[suit]
            if number == 0:
                number = 10
            self.number = number
            self.spendable = spendable
            self.tooltip = tooltip
            self.text = Text(u'{0} {1}'.format(self.suit, number), color = '#6A3819', font='Hangyaboly.ttf')
            self.t_text = Text(tooltip, size = 12, color = '#6A3819', font='Hangyaboly.ttf')
            self.bg = (self.spendable == True and Solid(SPENDABLE_COLOR) or Solid(PERMANENT_COLOR))
            #  Coordinates for new conflict; not referenced outside it
            #self.x = 0
            #self.y = 0
            #self.x_offset = 0
            #self.y_offset = 0

        def __str__(self):
            return(u' '.join([unicode(self.number), self.suit]).encode('utf-8'))

        def render(self, width, height, st, at):
            bg_render = renpy.render(self.bg, width, height, st, at)
            text_render = renpy.render(self.text, width, height, st, at)
            t_text_render = renpy.render(self.t_text, width, height, st, at)
            render = renpy.Render(width, height, st, at)
            render.blit(bg_render, (0,0))
            render.blit(text_render, (10,10))
            render.blit(t_text_render,(10,40))
            return render

        def visit(self):
            return [self.text, self.t_text, self.bg]

        def __eq__(self, other):
            if not type(other) is Card:
                return False
            elif other.suit==self.suit and other.number==self.number \
                and other.tooltip==self.tooltip and other.spendable==self.spendable:
                return True
            else:
                return False

    class CardMove(Action):
        '''
        Class for card button action in a conflict screen
        '''
        def __init__(self, card, **kwargs):
            self.card = card
            super(Action, self).__init__(**kwargs)

        def __call__(self):
            global stack
            stack.append(self.card) # No need to check if it's a correct suit: get_sensitive did that already
            global player_deck
            if self.card.spendable == True:
                player_deck.remove(self.card)
            a = filter(lambda x: x.suit == stack[-1].suit and x.number>=stack[-1].number, opponent_deck)
            if len(a) > 0:
                move_card = random.choice(a)
                stack.append(move_card)
                # The enemy made his move, if he could. If he could not, it's screen function's job to detect that
            renpy.restart_interaction()

        def get_sensitive(self):
            if (stack == [] or self.card.suit == stack[-1].suit and self.card.number>=stack[-1].number)\
            and len(stack)%2==0:  #  Blocks cards when it's opp's turn but you won
                # You can play a card when either there were no cards played or it beats the last played card
                return True
            else:
                return False

        def __eq__(self, other):
            if not(type(other) is CardMove):
                return False
            if self.card==other.card:
                return True
            else:
                return False

    # Various necessary functions

    def deck(deckline):
        #'''
        #Given a deck-describing line, return a list of cards.\
        #Line syntax is like 0С2Д2Д, etc. etc. Number, then suit, repeat for all cards\
        #'0' means '10' because fuck you, that's why\
        #'''
        if not (type(deckline) == unicode):
            raise TypeError('Only unicode line accepted by deck constructor')
        d = []
        l=list(deckline)
        while len(l)>0:
            num = int(l.pop(0))
            suit = l.pop(0)
            d.append(Card(suit, num))
        return d

    def init_conflict(deckline):
        # Initialises global variables for a conflict screen
        global ret
        global stack
        global opponent_deck
        ret = ''
        stack = []
        opponent_deck = deck(deckline)


    # Screens

    def conflict(**kwargs):
        '''
        Screen for card game. style.card_button imports only inactive_background = None
        '''
        # Defining UI elements
        global player_deck
        global stack
        global opponent_deck
        global ret
        if gl_no_rollback:
            renpy.block_rollback()
        ui.fixed(id='conflict_fixed', xpos=0.0, ypos=0.0)
        # Player hand
        p_adjustment = ui.adjustment()
        ui.vbox(spacing=10, ypos=0.05, xpos=0.1,  ymaximum = 0.75)
        ui.imagebutton(idle='images/STRELKAH_VVERKH.png',
                       hover='images/STRELKAH_VVERKH.png',
                       action=Function(p_adjustment.change, p_adjustment.value-0.1))
        ui.viewport(id = 'hand_view', xmaximum = 220, mousewheel=True, \
        draggable = True, yadjustment=p_adjustment, xalign=0.1)
        ui.vbox(id = 'p_hand', spacing = 10, ysize = 220*len(player_deck))
        for card in (x for x in player_deck if x not in stack if x.suit in {y.suit for y in opponent_deck}):
            ui.button(action = CardMove(card), style=style.card_button)
            ui.add(card, align = (0.5, 0.5))
        ui.close()
        ui.imagebutton(idle='images/STRELKAH_VNEESE.png',
                       hover='images/STRELKAH_VNEESE.png',
                       yminimum=50,
                       action=Function(p_adjustment.change, p_adjustment.range))
        ui.close()
        # Played cards
        ui.vbox(id = 'stack', spacing = 10, xalign = 0.5, ypos =0.05, ymaximum = 0.85)
        for card in stack:
            ui.add(card)
        ui.close()
        # Checking end conditions
        # Important note: variable names in SetVariable (actions on Defeat/Victory buttons)
        # actually should be strings, not Python variables themselves. This is weird, but this is how
        # renPy works
        if len(stack) >= 10:
            ui.textbutton('This has dragged for too long', xalign = 0.3, yalign = 0.95, action = Return ('TooLong'))
        if len(stack)>0 and len(stack)%2==0:
            if len(filter(lambda x: x.suit==stack[-1].suit and x.number>=stack[-1].number, player_deck))==0:
                ui.textbutton('You lose', xalign=0.5, xanchor=0.5, yalign=0.95,\
                action=[Hide('conf'), SetVariable('ret', u'F{0}'.format(stack[-1].suit))])
            try:
                opponent_deck.remove(stack[-1])
            except ValueError: # No clue where this exception comes from, but all works well if we just catch it
                pass
        if len(stack)%2==1:
            # This is cute: stack has an odd amount of cards iff oppponent didn't play during button actions
            # Even better: 0%2==1 so no worries about empty stack
            ui.textbutton('You win', xalign=0.5, xanchor=0.5, yalign=0.95, \
            action=[SetVariable('ret', u'S{0}'.format(stack[-1].suit)), Hide('conf')])
        # Opponent hand
        o_adjustment=ui.adjustment()
        ui.vbox(ypos=0.05, xalign=0.85, ymaximum=0.75)
        ui.imagebutton(idle='images/STRELKAH_VVERKH.png',
                       hover='images/STRELKAH_VVERKH.png',
                       action=Function(o_adjustment.change, 0))
        ui.viewport(id = 'o_view', xmaximum = 220, mousewheel=True, \
                    draggable = True, yadjustment=o_adjustment)
        ui.vbox(id = 'o_hand', spacing = 10)
        for card in opponent_deck:
            ui.button(action=None, style=style.card_button)
            ui.add('images/ROOBASTSHKA.png')
        ui.close()
        ui.imagebutton(idle='images/STRELKAH_VNEESE.png',
            hover='images/STRELKAH_VNEESE.png',
            yminimum=50,
            action=Function(o_adjustment.change, p_adjustment.range))
        ui.close()

    def card_collection(**kwargs):
        '''
        Screen that shows card collection
        '''
        global player_deck
        ui.window(id='collection_window', background=Frame('images/Tmp_frame.png', 5, 5), area = (0.05, 0.05, 0.9, 0.85))
        ui.fixed(id='collection_fixed', area = (0.05, 0.05, 0.9, 0.85))
        ui.text(u"Колода", color='#000000', xalign=0.5, ypos=0)
        rows = int(math.ceil(len(player_deck)/3.0))
        ui.viewport (id='collection_viewport', mousewheel = True, ypos=0.1,\
            yanchor=0, xalign=0.5, xsize=630)
        ui.grid(3, rows, id='collection_grid', transpose = False, spacing = 10)
        for card in player_deck:
            ui.add(card)
        for j in range(rows*3 - len(player_deck)):
            ui.add(Null())
        ui.close()  # For grid
        ui.close()  # For fixed
        # The following is outside the window!
        ui.textbutton(u"Продолжить", action = Hide('collection'), xalign = 0.5, yalign = 0.95)


    ###############################################################
    #Trade system
    ###############################################################

    class CardSell(Action):
        '''
        Analogue of CardMove, except for trading screen
        '''
        def __init__(self, card, **kwargs):
            self.card = card
            super(Action, self).__init__(**kwargs)

        def __call__(self):
            player_deck.remove(self.card)
            trade_stack.append(self.card)
            renpy.restart_interaction()

        def __eq__(self, other):
            if not(type(other) is CardMove):
                return False
            if self.card==other.card:
                return True
            else:
                return False


    class CardUnsell(Action):
        '''
        The same as CardSell, except it moves card the other way around
        '''
        def __init__(self, card, **kwargs):
            self.card = card
            super(Action, self).__init__(**kwargs)

        def __call__(self):
            trade_stack.remove(self.card)
            player_deck.append(self.card)
            renpy.restart_interaction()

        def __eq__(self, other):
            if not(type(other) is CardMove):
                return False
            if self.card==other.card:
                return True
            else:
                return False


    class Sell(Action):
        '''
        Buy the sold item if there are enough money in the trade_stack and close screen
        '''
        def __init__(self, price, to_sell, **kwargs):
            if not(type(to_sell) is Card):
                raise ValueError('Only cards can be sold')
            if not (type(price) is int):
                raise ValueError('Only integer prices are allowed')
            self.to_sell = to_sell
            self.price = price
            super(Action, self).__init__(**kwargs)

        def __call__(self):
            player_deck.append(self.to_sell)
            global ret
            ret = 'Sold'
            renpy.hide_screen('trade')
            renpy.restart_interaction()

        def get_sensitive(self):
            if sum((x.number for x in trade_stack))>=self.price:
                return True
            else:
                return False

    class DontSell(Action):
        '''
        Do not sell shit, return trade_stack to the deck and close screen
        '''
        def __init__(self, **kwargs):
            super(Action, self).__init__(**kwargs)

        def __call__(self):
            player_deck.extend(trade_stack)
            global ret
            ret = 'NotSold'
            renpy.hide_screen('trade')
            renpy.restart_interaction()

    def init_trade(i, o):
        # Initialises global variables for a trader screen
        global price
        global sell_card
        global trade_stack
        ret = ''
        if not (type(o) is Card):
            raise ValueError('Only cards can be used for initialising trade screen')
        price = i
        sell_card = o
        trade_stack = []

    def trade(**kwargs):
        '''
        Screen for buying shit for gold
        For gold only for now!
        One item of shit per screen only for now!
        '''
        if gl_no_rollback:
            renpy.block_rollback()
        global player_deck
        global trade_stack
        #Player hand, copypasted from conflict screen
        p_adjustment = ui.adjustment()
        ui.vbox(spacing=10, ypos=0.05, xpos=0.1,  ymaximum = 0.75)
        ui.imagebutton(idle='images/STRELKAH_VVERKH.png',
                       hover='images/STRELKAH_VVERKH.png',
                       action=Function(p_adjustment.change, 0))
        ui.viewport(id = 'hand_view', xmaximum = 220, mousewheel=True, \
        draggable = True, yadjustment=p_adjustment, xalign=0.1)
        ui.vbox(id = 'p_hand', spacing = 10, ysize = 220*len(player_deck))
        for card in (x for x in player_deck if x.suit==u'Деньги'):
            ui.button(action = CardSell(card), style=style.card_button)
            ui.add(card, align = (0.5, 0.5))
        ui.close()
        ui.imagebutton(idle='images/STRELKAH_VNEESE.png',
                       hover='images/STRELKAH_VNEESE.png',
                       yminimum=50,
                       action=Function(p_adjustment.change, p_adjustment.range))
        ui.close()
        # Cards player wants to trade
        stack_adjustment = ui.adjustment()
        ui.vbox(spacing=10, ypos=0.05, xalign=0.5, ymaximum=0.75)
        ui.imagebutton(idle='images/STRELKAH_VVERKH.png',
                       hover='images/STRELKAH_VVERKH.png',
                       action=Function(stack_adjustment.change, 0))
        ui.viewport(id = 'hand_view', xmaximum = 220, mousewheel=True, \
        draggable = True, yadjustment=stack_adjustment, xalign=0.1)
        ui.vbox(id = 'p_hand', spacing = 10, ysize = 220*len(player_deck))
        for card in trade_stack:
            ui.button(action = CardUnsell(card), style=style.card_button)
            ui.add(card, align = (0.5, 0.5))
        ui.close()
        ui.imagebutton(idle='images/STRELKAH_VNEESE.png',
                       hover='images/STRELKAH_VNEESE.png',
                       yminimum=50,
                       action=Function(p_adjustment.change, p_adjustment.range))
        ui.close()
        ui.text(u'Продаём {0} за {1}'.format(str(sell_card), str(price)), xalign=0.85, yalign=0.3)
        ui.textbutton('Купить', action=Sell(price, sell_card), xalign=0.8, yalign=0.4)
        ui.textbutton('Отмена', action=DontSell(), xalign=0.8, yalign=0.5)

    # Screen definitions
    # Predict disabled because otherwise block_rollback shoots any time it likes
    renpy.define_screen('conf', conflict, modal='True', zorder='10', predict=False)
    renpy.define_screen('collection', card_collection, modal = 'True', zorder='10')
    renpy.define_screen('trade', trade, modal='True', zorder='10', predict=False)

    ##########################################################
    #New card screen displayable and other event-capable shit#
    ##########################################################
    import pygame
    class Stack(renpy.Displayable):
        def __init__(self, card_list, **kwargs):
            super(renpy.Displayable, self).__init__(**kwargs)
            self.render_object=None
            self.card_list = card_list
            p_adjustment = ui.adjustment()
            self.viewport = Viewport(id = 'hand_view', xfill = False, yfill=False, xmaximum = 220, mousewheel=True, \
                            draggable = True, yadjustment = p_adjustment, scrollbars='vertical',\
                            xysize=(220, 600),\
                            child = LiveTile('images/Tmp_frame.png', xysize=(200, 10000)))




        def render(self, width, height, st, at):
            self.render_object = renpy.Render(width, height, st, at)
            vp_render = renpy.render(self.viewport, 220, 600, st, at)
            self.render_object.blit(vp_render, (0,0))
            return self.render_object

        def visit(self):
            return [self.viewport]
            pass
        def event(self, ev, x, y, st):
            return self.viewport.event(ev,x,y,st)
        def per_interact(self):
            renpy.redraw(self, 0)
            pass

        def append(self, card):
            pass

        def remove(self, card):
            pass
    class Jumpback():
        def __init__ (self):
            pass

    class Table(renpy.Displayable):
        def __init__(self, player_deck, **kwargs):
            if gl_no_rollback:
                renpy.block_rollback()
            super(renpy.Displayable, self).__init__(xfill=True, yfill=True, **kwargs)
            self.bg = Solid('#DDD')
            self.player_deck = player_deck
            self.text = [Text('Start of the log')]
            self.drag_text = Text('None dragged')
            self.dragging = False
            self.dragged = None
            card_y = 0
            for card in self.player_deck:
                card.x = 50
                card.y = card_y
                card_y += 130
            #  Test hand stack
            self.stack = Stack(player_deck)

        def render(self, width, height, st, at):
            self.render_object = renpy.Render(width, height, st, at)
            bg_render = renpy.render(self.bg, width, height, st, at)
            self.render_object.blit(bg_render, (0,0))
            card_renders = []
            card_ypos = 0
            for card in self.player_deck:
                tmp_render = card.render(200, 120, st, at)
                card_renders.append(tmp_render)
                self.render_object.blit(tmp_render, (card.x, card.y))
            #  Stack render
            stack_render = self.stack.render(width, height, st, at)
            self.render_object.blit(stack_render, (800,0))
            #  Debug text
            text_ypos = 10
            if self.dragged is not None:
                self.drag_text = Text('{0}'.format(self.dragged.number))
            else:
                self.drag_text = Text('None dragged')
            for x in self.text:
                text_render = renpy.render(x, width, height, st, at)
                self.render_object.blit(text_render, (500, text_ypos))
                text_ypos += 25
            drag_render = renpy.render(self.drag_text, width, height, st, at)
            self.render_object.blit(drag_render, (500, 600))
            return self.render_object
            pass

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                #self.text.append(Text('Click at {0};{1}'.format(x,y)))
                self.drag_state = True
                self.drag_start = (x,y)
                #  Checking if we have clicked any cards:
                for card in self.player_deck:
                    if x>card.x and y >card.y and x - card.x < 200 and y - card.y < 120:
                        self.dragged = card
                        self.dragged.x_offset = self.dragged.x - x
                        self.dragged.y_offset = self.dragged.y - y
                        break
                renpy.redraw(self,0)
            if ev.type == pygame.MOUSEMOTION and self.dragged is not None:
                self.dragged.x = x + self.dragged.x_offset
                self.dragged.y = y + self.dragged.y_offset
                renpy.redraw(self, 0)
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if (abs(x-self.drag_start[0]>10) or abs(y-self.drag_start[1]>10)):
                    #  If it was a long enough drag
                    self.text.append(Text('Drag from {0};{1} to {2};{3}'.format(self.drag_start[0], self.drag_start[1], x, y)))
                    if not self.dragged == None:
                        self.dragged.x = x + self.dragged.x_offset
                        self.dragged.y = y + self.dragged.y_offset
                else:
                    self.text.append(Text('Click at {0};{1}'.format(x,y)))
                self.dragged = None
                self.drag_state == False
                renpy.redraw(self,0)
            self.stack.event(ev, x, y, st)

        def visit(self):
            l = self.player_deck[:3]
            l.extend(self.text)
            l.append(self.bg)
            l.append(self.drag_text)
            l.append(self.stack)
            return l

        def per_interact(self):
            renpy.redraw(self, 0)
