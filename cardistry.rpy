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
            self.t_text = Text(self.tooltip, size = 14, color = '#6A3819', font='Hangyaboly.ttf')
            self.bg = (self.spendable == True and Solid(SPENDABLE_COLOR) or Solid(PERMANENT_COLOR))
            self.frame = Solid('#6A3819')
            if cost is None:
                self.cost = self.number
            else:
                self.cost = cost
            self.xpos = 0
            self.ypos = 0
            self.xsize = 200
            self.ysize = 120
            self.x_offset = 0
            self.y_offset = 0
            self.stack = None
            self.transform = Transform(child=self) #, xpos=self.xpos, ypos=self.ypos)

        def reinit_transform(self):
            """
            Renitialise card Transform that contains its position and stack it belongs to.
            Should be called any time screen is initialized, currently called from Cardbox.__init__()
            """
            self.transform.xpos = 0
            self.transform.ypos = 0
            self.transform.xsize = 200
            self.transform.ysize = 120
            self.x_offset = 0
            self.y_offset = 0
            self.stack = None
            # self.transform = Transform(child=self) #, xpos=self.xpos, ypos=self.ypos)

        def __str__(self):
            return(u'{0} {1}'.format(self.suit, self.number))

        def render(self, width, height, st, at):
            frame_render = renpy.render(self.frame, width, height, st, at)
            bg_render = renpy.render(self.bg, 196, 116, st, at)
            text_render = renpy.render(self.text, width, height, st, at)
            t_text_render = renpy.render(self.t_text, width, height, st, at)
            render = renpy.Render(width, height, st, at)
            render.blit(frame_render, (0, 0))
            render.blit(bg_render, (2, 2))
            render.blit(text_render, (10, 10))
            render.blit(t_text_render, (10, 40))
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
                card.reinit_transform()
                card.stack = stack_id
            if len(self.card_list) > 0:
                self._position_cards()

        # Card positioning methods

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

        # Card transfer methods

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

        def __len__(self):
            return (len(self.card_list))

        def append(self, card):
            card.stack = self.id
            self.card_list.append(card)

        def remove(self, card):
            card.stack = None
            self.card_list.remove(card)

        def pop(self, index):
            card = self.card_list[index]
            self.remove(card)
            return card

        def index(self, card):
            return self.card_list.index(card)

        def replace_cards(self, l):
            """
            Set this stack's card_list as l
            Release all cards from this stack
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
            if origin == 'T_OFFER' and paid-withheld >= 0:
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

    class PlayerConflictStack(Cardbox):
        #  Player hand for conflict screen
        def __init__(self, **kwargs):
            super(PlayerConflictStack, self).__init__(**kwargs)

        def accept(self, card, origin=None):
            return False

        def give(self, card):
            return True

    class OpponentConflictStack(Cardbox):
        """
        Opponent hand for conflict
        """
        def __init__(self, **kwargs):
            super(OpponentConflictStack, self).__init__(**kwargs)

        def accept(self, card, origin=None):
            return False

        def give(self, card):
            return True

    class MidStack(Cardbox):
        """
        Central stack for the conflict
        """
        def __init__(self, **kwargs):
            super(MidStack, self).__init__(**kwargs)

        def accept(self, card, origin=None):
            if origin not in self.accept_from:
                #  Not that I mean to actually limit its accept_from
                return False
            if self.card_list==[] or (card.suit == self.card_list[-1].suit and card.number >= self.card_list[-1].number):
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
            self.stacks = stacks
            self.automove = automove  #  Dict of stacks that will be used automatically upon click
            assert all(x in (s.id for s in stacks) for x in automove.keys())
            self.stack_dict = {x.id: x for x in self.stacks}
            self.cards = []
            for x in self.stacks:
                self.cards.extend(x.card_list)
            self.drag_text = Text('None dragged')
            self.dragged = None
            self.drag_start = (0, 0)
            #  Debug Cardbox highlighters
            self.cardboxes = []
            for x in self.stacks:
                self.cardboxes.append(Solid('#FF0000'))

        def render(self, width, height, st, at):
            self.render_object = renpy.Render(width, height, st, at)
            #  DEBUG DRAG TEXT
            if self.dragged is not None:
                self.drag_text = Text('{0}'.format(self.dragged.stack))
            else:
                self.drag_text = Text('None dragged')
            drag_render = renpy.render(self.drag_text, width, height, st, at)
            self.render_object.blit(drag_render, (500, 600))
            #  DEBUG STACK BOXES
            box_renders = []
            for x in range(len(self.stacks)):
                tmp_render = self.cardboxes[x].render(self.stacks[x].xsize, self.stacks[x].ysize, st, at)
                box_renders.append(tmp_render)
                self.render_object.blit(tmp_render, (self.stacks[x].x, self.stacks[x].y))
            for card in self.cards:
                self.render_object.place(card.transform)
            return self.render_object

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                #  Checking if we have clicked any cards:
                for card in reversed(self.cards):
                    if inside((x,y), (card.transform.xpos, card.transform.ypos, card.xsize, card.ysize))\
                            and self.get_stack_by_id(card.stack).give(card):
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
                                else:
                                    #  Why not rearrange cards within stack
                                    is_accepted = True
                        if not is_accepted:
                            #  If card was not accepted, it should be returned where it belongs
                            self.dragged.transform.xpos = self.initial_card_position[0]
                            self.dragged.transform.ypos = self.initial_card_position[1]
                        #  Dragging has ended somehow anyway
                        self.dragged.transform.update()
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
                #  Restart interaction to check for success, flip exit button state, etc.
                renpy.restart_interaction()

        def visit(self):
            l = []
            l+=(x.transform for x in self.cards)
            #l.append(self.bg)
            l.append(self.drag_text)
            l+=self.cardboxes
            return l

        def per_interact(self):
            #  In children this method also checks for exit conditions,
            #  Makes opponent moves and so on, so it's disabled here
            raise NotImplementedError

        def get_stack_by_id(self, stack_id):
            return self.stack_dict[stack_id]

        def finalize_success(self):
            """
            Interact with globals upon success
            """
            raise NotImplementedError('Finalization methods must be overloaded')

        def finalize_failure(self):
            """
            Interact with globals upon failure
            """
            raise NotImplementedError('Finalization methods must be overridden')

    #  Specific table classes. Overload per_interact to check for exit conditions or enemy moves, if any.
    class TradeTable(Table):
        """
        Table that facilitates trade
        """
        def __init__(self, **kwargs):
            super(TradeTable, self).__init__(**kwargs)
            self.paid_text = Text('{0}'.format(paid), color='#6A3819', size=30)
            self.withheld_text = Text('{0}'.format(withheld), color='#6A3819', size=30)
        #
        def render(self, width, height, st, at):
            r = super(TradeTable, self).render(width, height, st, at)
            paid_render = renpy.render(self.paid_text, width, height, st, at)
            r.blit(paid_render, (720, 500))
            withheld_render = renpy.render(self.withheld_text, width, height, st, at)
            r.blit(withheld_render, (720, 200))
            return self.render_object

        def visit(self):
            r = super(TradeTable, self).visit()
            r += [self.paid_text, self.withheld_text]
            return r

        def per_interact(self):
            # Update text fields
            self.paid_text = Text('{0}'.format(paid), color='#6A3819', size=30)
            self.withheld_text = Text('{0}'.format(withheld), color='#6A3819', size=30)
            renpy.redraw(self, 0)

        def finalize_success(self):
            """
            Success in this case is "Buy/sell stuff"
            """
            global player_deck
            # Move cards from T_OFFER to global deck and remove cards in P_OFFER from there
            for card in self.get_stack_by_id('T_OFFER').card_list:
                player_deck.append(card)
            for card in self.get_stack_by_id('P_OFFER').card_list:
                if card in player_deck:
                    player_deck.remove(card)
            # Check that all cards from P_HAND are already in deck, add otherwise
            for card in self.get_stack_by_id('P_HAND').card_list:
                if card not in player_deck:
                    player_deck.append(card)
            # Clean stacks to clarify possible multiple pointer issues and enable garbage collection
            # Stacks will be re-initialized by trade initialization, if any, later
            for stack in self.stacks:
                stack.replace_cards([])

        def finalize_failure(self):
            """
            Failure in this case is "Do not sell stuff"
            """
            global player_deck
            # Return cards that are in P_OFFER back home
            for card in self.get_stack_by_id('P_OFFER').card_list:
                if card not in player_deck:
                    player_deck.append(card)

    class ConflictTable(Table):
        def __init__(self, **kwargs):
            super(ConflictTable, self).__init__(**kwargs)
            self.finalizing = False # Set to True when calling finalize_*

        def per_interact(self):
            # Check if the conflict has been won or lost
            stack_len = len(self.get_stack_by_id('M_STACK'))
            if stack_len > 0 and stack_len % 2 == 1:
                # It's opponent turn
                if not any(self.get_stack_by_id('M_STACK').accept(x, origin='O_HAND')
                           for x in self.get_stack_by_id('O_HAND').card_list):
                    # Opponent cannot play, so player wins
                    if not self.finalizing:
                        self.finalize_success()
                else:
                    # Make opponent move
                    moves = [x for x in self.get_stack_by_id('O_HAND').card_list
                             if self.get_stack_by_id('M_STACK').accept(x, origin='O_HAND')]
                    card = renpy.random.choice(moves)
                    self.get_stack_by_id('O_HAND').remove(card)
                    (card.transform.xpos, card.transform.ypos) = self.get_stack_by_id('M_STACK').position_next_card()
                    self.get_stack_by_id('M_STACK').append(card)
                    # Move newly played card to top
                    self.cards.append(self.cards.pop(self.cards.index(card)))

            elif stack_len % 2 == 0:
                # It's player turn
                if not any(self.get_stack_by_id('M_STACK').accept(x, origin='P_HAND')
                           for x in self.get_stack_by_id('P_HAND').card_list):
                    # Player cannot play, so opponent wins
                    if not self.finalizing:
                        self.finalize_failure()
            renpy.redraw(self,0)

        def finalize_failure(self):
            global ret
            try:
                ret = u'F{0}'.format(self.get_stack_by_id('M_STACK').card_list[-1].suit)
            except IndexError:
                # Consider the conflict lost with one of the suits in opponent hand
                ret = u'F{0}'.format(self.get_stack_by_id('O_HAND').card_list[0].suit)
            global player_deck
            #  Remove spent cards unless they are permanent
            for card in self.get_stack_by_id('M_STACK').card_list:
                if card in player_deck and card.spendable:
                    player_deck.remove(card)
            renpy.show_screen('conflict_failure_screen')

        def finalize_success(self):
            global ret
            ret = u'S{0}'.format(self.get_stack_by_id('M_STACK').card_list[-1].suit)
            for card in self.get_stack_by_id('M_STACK').card_list:
                if card in player_deck and card.spendable:
                    player_deck.remove(card)
            renpy.show_screen('conflict_success_screen')


    #  Action classes for button screens

    class DoSell(Action):
        """
        Move user's offer to trader hand and vice versa. Hide screens
        """
        def __init__(self, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            #  Transfer cards
            #  Remove sold cards from player deck and add bought ones,
            #  If that was not done already manually
            global trade_table
            trade_table.finalize_success()
            renpy.hide_screen('trade_screen')
            renpy.hide_screen('trade_buttons_screen')
            renpy.restart_interaction()
            return

        def get_sensitive(self):
            global paid
            global withheld
            return paid >= withheld

    class DoNotSell(Action):
        """
        Return all cards where they belonged originally and hide screens
        """
        def __init__(self, **kwargs):
           pass

        def __call__(self):
            global trade_table
            trade_table.finalize_failure()
            renpy.hide_screen('trade_screen')
            renpy.hide_screen('trade_buttons_screen')
            renpy.restart_interaction()

        def get_sensitive(self):
            global paid
            global withheld
            return paid >= withheld

    # class HideConflictSuccess(Action):
    #     def __init__(self):
    #         pass
    #
    #     def get_sensitive(self):
    #         return True
    #
    #     def __call__(self):
    #         renpy.hide_screen('coflict_table_screen')
    #         renpy.hide_screen('conflict_success_screen')

#  Table button screens. Separate because buttons inside CDD are a godawful mess

screen trade_buttons_screen():
    zorder 10
    textbutton u"Торговать":
        action DoSell()
        xpos 350
        ypos 350
    textbutton u"Не торговать":
        action DoNotSell()
        xpos 550
        ypos 350

screen conflict_success_screen():
    modal True
    zorder 100
    textbutton u"Вы победили":
        action [Hide('conflict_table_screen'), Hide('conflict_success_screen')]
        xpos 480
        ypos 350

screen conflict_failure_screen():
    modal True
    zorder 10
    textbutton u"Вы проиграли":
        action [Hide('conflict_table_screen'), Hide('conflict_failure_screen')]
        xpos 480
        ypos 350

## Table init procedures

init -1 python:
    def init_conflict_table(opponent_deck):
        """
        Initialize conflict table and show the corresponding screen
        :param opponent_deck: A list of cards
        :return:
        """
        global player_deck
        global conflict_table
        assert type(opponent_deck) is list and all(type(x) is Card for x in opponent_deck)
        # List of acceptable suits
        suits=set(x.suit for x in opponent_deck)
        p_hand_stack = PlayerConflictStack(card_list=[x for x in player_deck if x.suit in suits],
                                           stack_id='P_HAND',
                                           accept_from=[],
                                           x=100, y=100, xsize=250, ysize=500)
        mid_stack = MidStack(card_list=[], stack_id='M_STACK', accept_from=['P_HAND', 'O_HAND'],
                             x=450, y=100, xsize=250, ysize=500)
        o_hand_stack = OpponentConflictStack(card_list=opponent_deck, stack_id='O_HAND',
                                             x=780, y=100, xsize=250, ysize=500)
        a = {'P_HAND': 'M_STACK'}
        conflict_table = ConflictTable(stacks=[p_hand_stack, mid_stack, o_hand_stack],
                                       automove=a)
        renpy.show_screen('conflict_table_screen')

    def init_trade_table(stock, accepted_suits=[u'Сила', u'Деньги', u'Знания', u'Интриги']):
        """
        Initialize trade table and show it on screen.
        :param stock: List of cards that are sold here
        :param accepted_suits: List of suits that are accepted here
        :return:
        """
        global player_deck
        #global acc_stack
        global trade_table
        global paid
        global withheld
        paid = 0
        withheld = 0
        assert type(stock) is list and len(stock)>0 and all(lambda x: type(x) is Card for x in stock)
        assert type (accepted_suits) is list and all(x in accepted_suits in [u'Сила', u'Деньги', u'Знания', u'Интриги'])
        t_offer_stack = TraderOfferStack(card_list=[], stack_id='T_OFFER', accept_from=['T_HAND'],
                                         x=400, y=100, xsize=300, ysize=200)
        p_offer_stack = PlayerOfferStack(card_list=[], stack_id='P_OFFER', accept_from=['P_HAND'],
                                         x=400, y=400, xsize=300, ysize=200)
        p_hand_stack = PlayerShoppingStack(card_list=[x for x in player_deck if x.suit in accepted_suits],
                                           stack_id='P_HAND', accept_from=['T_OFFER', 'P_OFFER'],
                                           x=10, y=100, xsize=300, ysize=500)
        t_hand_stack = TraderHandStack(card_list=stock, stack_id='T_HAND', accept_from=['T_OFFER'],
                                       x=800, y=100, xsize=300, ysize=500)
        #n_stack = NullStack(stack_id='NULL', accept_from=['HAND'], x=750, xsize=300, y=100, ysize=500)
        a = {'P_HAND': 'P_OFFER', 'T_HAND': 'T_OFFER', 'T_OFFER': 'P_HAND', 'P_OFFER': 'P_HAND'}
        #acc_stack._position_cards()
        #p_stack._position_cards()
        trade_table = TradeTable(stacks=[p_hand_stack, t_hand_stack, p_offer_stack, t_offer_stack], automove=a)
        renpy.show_screen('trade_screen')
        renpy.show_screen('trade_buttons_screen')


init:
    screen trade_screen():
        modal True
        zorder 9
        add trade_table

    screen conflict_table_screen():
        modal True
        zorder 9
        add conflict_table