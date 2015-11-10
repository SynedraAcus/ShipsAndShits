# Everything related to the card conflict mechanics

init -3 python:
    import random
    import math
    SUITS={u'С':u'Сила',
        u'Д':u'Деньги',
        u'З':u'Знания',
        u'И':u'Интриги'}

    DEFAULT_HISTORY = u'Вам не известна история этой карты'
    SPENDABLE_COLOR = '#AAA'
    PERMANENT_COLOR = '#DEC666'
    COST_QOTIENT = 1.5 #  Cost-to-nominal ratio for trading system
    # Card-related classes: card itself and an action

    class Card(renpy.Displayable):
        def __init__(self, suit, number, spendable = False, tooltip = DEFAULT_HISTORY, cost=None, **kwargs):
            super(Card, self).__init__(xysize=(200, 120), xfill=False, yfill=False, **kwargs)
            self.suit = SUITS[suit]
            if number == 0:
                number = 10
            self.number = number
            self.spendable = spendable
            self.tooltip = tooltip
            self.text = Text(u'{0} {1}'.format(number, self.suit), color = '#6A3819', font='Hangyaboly.ttf')
            self.t_text = Text(tooltip, size = 14, color = '#6A3819', font='Hangyaboly.ttf')
            self.bg = (self.spendable == True and Solid(SPENDABLE_COLOR) or Solid(PERMANENT_COLOR))
            if cost is None:
                self.cost = self.number
            else:
                self.cost = cost
            #  Stuff for new conflict; not referenced outside it
            self.xpos = 0
            self.ypos = 0
            self.xsize = 200
            self.ysize = 120
            self.x_offset = 0
            self.y_offset = 0
            self.stack = 0
            self.transform = Transform(child=self) #, xpos=self.xpos, ypos=self.ypos)

        def __str__(self):
            return(u'{0} {1}'.format(self.suit, self.number))

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
        ui.text(u'Продаём {0} {1} за {2}'.format(str(sell_card.number), sell_card.suit, str(price)),\
                xalign=0.85, yalign=0.3, color = '#6A3819', font='Hangyaboly.ttf')
        ui.text(u'Уплочено {0}'.format(str(sum((x.number for x in trade_stack)))),
                xalign=0.85, yalign = 0.35, color = '#6A3819', font='Hangyaboly.ttf')
        ui.textbutton(u'Купить', action=Sell(price, sell_card), xalign=0.8, yalign=0.4)
        ui.textbutton(u'Отмена', action=DontSell(), xalign=0.8, yalign=0.5)

    # Screen definitions
    # Predict disabled because otherwise block_rollback shoots any time it likes
    renpy.define_screen('conf', conflict, modal='True', zorder='10', predict=False)
    renpy.define_screen('collection', card_collection, modal = 'True', zorder='10')
    renpy.define_screen('trade', trade, modal='True', zorder='10', predict=False)

    ##########################################################
    #New card screen displayable and other event-capable shit#
    ##########################################################
    import pygame

    #  Various utility functions

    def inside(click, box):
        """
        Check whether a point is within a box
        :param click: 2-element tuple (x,y)
        :param box: 4-element tuple: (x,y,xsize,ysize)
        :return:
        """
        if not(click[0]<box[0] or click[0]>box[0]+box[2]):
            if not (click[1]<box[1] or click[1]>box[1]+box[3]):
                return True
        return False

    #  Cardbox and its children


    class Cardbox(object):
        def __init__(self, card_list=[], stack_id='NO ID', accept_from = None, x=0, y=0, xsize=300, ysize=300):
            # Position on screen
            self.x = x
            self.y = y
            self.id = stack_id
            self.xsize = xsize
            self.ysize = ysize
            if accept_from is not None:
                self.accept_from = accept_from
            # Rest of it
            self.card_list = card_list
            for card in self.card_list:
                card.stack = stack_id
            if len(self.card_list) > 0:
                self._position_cards()

        def position_next_card(self):
            """
            Return position of the next card to be added
            Takes current card positions into account
            """
            #max_y = max((c.y for c in self.card_list))
            #return(int(self.x+self.xsize/2), max_y+50)
            # If there is no card list, add card to the top
            if len(self.card_list) == 0:
                return int(self.x+self.xsize/2-100), self.y + 10
            else:
                # Get coordinates, sorted by y
                coords = max(((c.transform.xpos, c.transform.ypos) for c in self.card_list), key=lambda c: c[1])
                #  Add the next card 50 px under the lowest one
                return coords[0], coords[1]+50

        def _position_cards(self):
            """
            Position all the cards in stack. This is to be called only when
            initialising Cardbox for display
            """
            self.card_list[0].transform.xpos = int(self.x+self.xsize/2-100)
            self.card_list[0].transform.ypos = self.y + 10
            for card in self.card_list[1:]:
                (card.transform.xpos, card.transform.ypos) = self.position_next_card()
                card.transform.update()
                # mid = int(self.x + self.xsize/2) - 100
                # step = int(self.ysize/len(self.card_list))
                # y = self.y
                # for card in self.card_list:
                #     card.transform.xpos = mid
                #     card.transform.ypos = y
                #     card.transform.update()
                #     y += step

        def give(self, card):
            '''
            Return True if this stack is willing to give card away, False otherwise
            Should be defined by child classes
            '''
            raise NotImplementedError('Give function should be overridden')

        def accept(self, card, origin=None):
            '''
            Return True if this stack accepts this card, False otherwise
            Should be defined by child classes
            '''
            raise NotImplementedError('Accept function should be overridden')

        #  Defining those here creates less messy code than
        #  inheriting from list ABC. Maybe even quicker
        def append(self, card):
            self.card_list.append(card)

        def remove(self, card):
            self.card_list.remove(card)

        def pop(self, index):
            return self.card_list.pop(index)

        def index(self, card):
            return self.card_list.index(card)

        def replace_cards(self, l):
            """
            Set this stack's card_list as l
            """
            self.card_list = l


    class PlayerShoppingStack(Cardbox):
        """
        The player hand stack for trading. Contains actual trade logic
        """
        def __init__(self, **kwargs):
            super(PlayerShoppingStack, self).__init__(**kwargs)


        def accept(self, card, origin=None):
            if origin not in self.accept_from:
                #  Wrong source? No accept
                return False
            global paid
            global withheld
            if origin == 'T_OFFER' and card.cost <= paid-withheld:
                #  Accept bought card, if it was paid for
                return True
            elif origin == 'P_OFFER' and card.number <= paid-withheld:
                return True
            else:
                return False

        def give(self, card):
            return True

    class PlayerOfferStack(Cardbox):
        '''
        Stack for player-sold cards during trade
        Overloaded .append and .remove change global paid
        '''
        def __init__(self, **kwargs):
            super(PlayerOfferStack, self).__init__(**kwargs)

        def accept(self, card, origin):
            if origin in self.accept_from:
                return True
            return False

        def give(self, card):
            return True

        def append(self, card):
            global paid
            paid += card.number
            super(PlayerOfferStack, self).append(card)

        def remove(self, card):
            global paid
            paid -= card.number
            super(PlayerOfferStack, self).remove(card)

        def position_next_card(self):
            """
            Return position of the next card to be added
            Takes current card positions into account
            """
            #max_y = max((c.y for c in self.card_list))
            #return(int(self.x+self.xsize/2), max_y+50)
            # If there is no card list, add card to the top
            if self.card_list == []:
                return int(self.x+self.xsize/2-100), self.y + 50
            # Get coordinates, sorted by y
            coords = sorted(((c.transform.xpos, c.transform.ypos) for c in self.card_list), key=lambda c: c[1])
            #  Add the next card 50 px under the lowest one
            return coords[-1][0], coords[-1][1]+50

    class TraderOfferStack(Cardbox):
        """
        Stack for trader-sold cards during trade
        Overloaded .append and .remove change global withheld
        """
        def __init__(self, **kwargs):
            super(TraderOfferStack, self).__init__(**kwargs)

        def accept(self, card, origin=None):
            if origin in self.accept_from:
                return True
            return False

        def give(self, card):
            return True

        def append(self, card):
            global withheld
            withheld += card.cost
            super(TraderOfferStack, self).append(card)

    class TraderHandStack(Cardbox):
        """
        Stack for trader hand.
        Overloaded .remove decreases withheld if card moved back from T_OFFER
        """
        def __init__(self, **kwargs):
            super(TraderHandStack, self).__init__(**kwargs)

        def append(self, card):
            global withheld
            withheld -= card.cost
            super(TraderHandStack, self).append(card)

        def give(self, card):
            return True

        def accept(self, card, origin=None):
            if origin in self.accept_from:
                return True
            else:
                return False


    class BasicStack(Cardbox):
        """
        Stack that accepts and gives all cards, but contains no more logic.
        Useful every once in a while
        """
        def __init__(self, **kwargs):
            super(BasicStack, self).__init__(**kwargs)

        def accept(self, card, origin=None):
            if origin in self.accept_from:
                return True
            else:
                return False

        def give(self, card):
            return True


    class Table(renpy.Displayable):

        def __init__(self, stacks = [], automove = {}, **kwargs):
            if gl_no_rollback:
                renpy.block_rollback()
            super(renpy.Displayable, self).__init__(xfill=True, yfill=True, **kwargs)
            #self.bg = Solid('#DDD')
            self.player_deck = player_deck
            self.stacks = stacks
            self.automove = automove  #  Dict of stacks that will be used automatically upon click
            #  ADD KEY CORRECTNESS ASSERT FOR AUTOMOVE
            self.stack_dict = {x.id: x for x in self.stacks}
            self.cards = []
            for x in self.stacks:
                self.cards.extend(x.card_list)
            self.drag_text = Text('None dragged')
            self.dragged = None
            self.drag_start = (0, 0)
            self.initial_card_position = (0,0)
            #  Debug Cardbox highlighters
            self.cardboxes = []
            for x in self.stacks:
                self.cardboxes.append(Solid('#FF0000'))
            #  Debug paid/withheld
            self.paid_text = Text('Paid {0}/Withheld {1}'.format(str(paid), str(withheld)))

        def render(self, width, height, st, at):
            self.render_object = renpy.Render(width, height, st, at)
            # bg_render = renpy.render(self.bg, width, height, st, at)
            # self.render_object.blit(bg_render, (0,0))
            #  DEBUG DRAG TEXT
            if self.dragged is not None:
                self.drag_text = Text('{0}'.format(self.dragged.stack))
            else:
                self.drag_text = Text('None dragged')
            drag_render = renpy.render(self.drag_text, width, height, st, at)
            self.render_object.blit(drag_render, (500, 600))
            self.paid_text = Text('Paid {0}/Withheld {1}'.format(str(paid), str(withheld)))
            paid_render = renpy.render(self.paid_text, width, height, st, at)
            self.render_object.blit(paid_render, (450, 630))

            #  DEBUG STACK BOXES
            box_renders = []
            for x in range(len(self.stacks)):
                tmp_render = self.cardboxes[x].render(self.stacks[x].xsize, self.stacks[x].ysize, st, at)
                box_renders.append(tmp_render)
                self.render_object.blit(tmp_render, (self.stacks[x].x, self.stacks[x].y))
            #  PLACEHOLDER PAID/WITHHELD VALUES
            #  CARDS
            #card_renders = []
            for card in self.cards:
                # tmp_render = card.render(200, 120, st, at)
                # card_renders.append(tmp_render)
                # self.render_object.blit(tmp_render, (card.xpos, card.ypos))
                self.render_object.place(card.transform)
            return self.render_object



        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                #  Checking if we have clicked any cards:
                for card in reversed(self.cards):
                    if inside((x,y), (card.transform.xpos, card.transform.ypos, card.xsize, card.ysize)) and self.get_stack_by_id(card.stack).give(card):
                        self.drag_start = (x, y)
                        self.initial_card_position = (card.transform.xpos, card.transform.ypos)
                        self.dragged = card
                        self.dragged.x_offset = self.dragged.transform.xpos - x
                        self.dragged.y_offset = self.dragged.transform.ypos - y
                        #  Show dragged on the top of other cards
                        self.cards.append(self.cards.pop(self.cards.index(self.dragged)))
                        break  #  No need to move two cards at the same time

            if ev.type == pygame.MOUSEMOTION and self.dragged is not None:
                #  Just redrawing card in hand
                self.dragged.transform.xpos = x + self.dragged.x_offset
                self.dragged.transform.ypos = y + self.dragged.y_offset
                self.dragged.transform.update()

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if abs(x - self.drag_start[0]) > 7 or abs(y - self.drag_start[1]) > 7:
                    #  If it was a long enough drag
                    if self.dragged is not None:
                        # If the card was dragged:
                        #  Check if there is accepting stack and transfer is possible
                        is_accepted = False
                        for accepting_stack in self.stacks:
                            if inside((x,y), (accepting_stack.x, accepting_stack.y, accepting_stack.xsize, accepting_stack.ysize)):
                                if not self.dragged.stack == accepting_stack.id:
                                    #  If a card is moved to the other stack
                                    if accepting_stack.accept(self.dragged, origin=self.dragged.stack):
                                        is_accepted = True
                                        self.get_stack_by_id(self.dragged.stack).remove(self.dragged)
                                        accepting_stack.append(self.dragged)
                                        self.dragged.stack = accepting_stack.id
                                else:
                                    #  Why not rearrange cards within stack
                                    is_accepted = True
                        if not is_accepted:
                            #  If card was not accepted, it should be returned where it belongs
                            self.dragged.transform.xpos = self.initial_card_position[0]
                            self.dragged.transform.ypos = self.initial_card_position[1]
                            self.dragged.transform.update()
                        #  Dragging has ended somehow anyway
                        self.dragged = None

                else:
                    #  Things to do upon click
                    if self.dragged is not None and self.dragged.stack in self.automove.keys():
                        #  First of all check whether transfer is possible
                        old_stack = self.get_stack_by_id(self.dragged.stack)
                        new_stack = self.get_stack_by_id(self.automove[old_stack.id])
                        if old_stack.give(self.dragged) and new_stack.accept(self.dragged, origin=old_stack.id):
                            #  Positioning card should happen before appending
                            #  Because it uses the accepting stack's card_list to define card position
                            new_coords = new_stack.position_next_card()
                            (self.dragged.transform.xpos, self.dragged.transform.ypos) = new_coords
                            self.dragged.transform.update()
                            #  Remove dragged card from its initial stack and move it to acceptor
                            old_stack.remove(self.dragged)
                            new_stack.append(self.dragged)
                            self.dragged.stack = new_stack.id
                    #  Release dragged card anyway
                    self.dragged = None

        def visit(self):
            l = []
            l+=(x.transform for x in self.cards)
            #l.append(self.bg)
            l.append(self.drag_text)
            l.append(self.paid_text)
            l+=self.cardboxes
            return l

        def per_interact(self):
            renpy.redraw(self, 0)

        def get_stack_by_id(self, stack_id):
            return self.stack_dict[stack_id]

init -1 python:

    def init_new_conflict():
        global player_deck
        p_stack.replace_cards(player_deck)
        p_stack._position_cards()

    def init_trade_table(stock):
        global player_deck
        #global acc_stack
        global test_table
        global paid
        global withheld
        paid = 0
        withheld = 0
        t_offer_stack = TraderOfferStack(card_list=[], stack_id='T_OFFER', accept_from=['T_HAND'],
                                   x=400, y=100, xsize=300, ysize=200)
        p_offer_stack = PlayerOfferStack(card_list=[], stack_id='P_OFFER', accept_from=['P_HAND'],
                                   x=400, y=400, xsize=300, ysize=200)
        p_hand_stack = PlayerShoppingStack(card_list=player_deck, stack_id='P_HAND', accept_from=['T_OFFER', 'P_OFFER'],
                                    x=10, y=100, xsize=300, ysize=500)
        t_hand_stack = TraderHandStack(card_list=stock, stack_id='T_HAND', accept_from=['T_OFFER'],
                                  x=800, y=100, xsize=300, ysize=500)
        #n_stack = NullStack(stack_id='NULL', accept_from=['HAND'], x=750, xsize=300, y=100, ysize=500)
        a = {'P_HAND': 'P_OFFER', 'T_HAND': 'T_OFFER', 'T_OFFER': 'P_HAND', 'P_OFFER': 'P_HAND'}
        #acc_stack._position_cards()
        #p_stack._position_cards()
        test_table = Table(stacks=[p_hand_stack, t_hand_stack, p_offer_stack, t_offer_stack], automove=a)


init:
    screen test_screen():
        modal True
        zorder 10
        add test_table