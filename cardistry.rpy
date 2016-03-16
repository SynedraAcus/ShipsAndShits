# Everything related to the card conflict mechanics

init -3 python:
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
    class Card(object):
        """
        Card for the game. This class contains value, suit and handles showing the correct displayable.
        Small displayable is returned if card is not maximized, large is returned otherwise
        """
        def __init__(self, suit, number, spendable=False, tooltip=DEFAULT_HISTORY, cost=None):
            self.suit = SUITS[suit]
            if number == 0:
                number = 10
            self.number = number
            self.spendable = spendable
            self.tooltip = tooltip
            self.maximized = True  #  Set to True when card is expanded
            self.visible = True  #  Set to True if player can see the card
            self.stack = None
            if cost:
                self.cost = cost
            else:
                self.cost = number
            self.init_displayables()

        #  Displayables-related methods
        def init_displayables(self):
            """
            Initialize card displayables
            """
            self.large_displayable = CardLargeDisplayable(self)
            self.small_displayable = CardSmallDisplayable(self)
            self.hidden_displayable = CardHiddenDisplayable()

        def remove_displayables(self):
            """
            Remove card displayables, as those can't be saved
            """
            self.large_displayable = None
            self.small_displayable = None
            self.hidden_displayable = None

        def get_displayable(self):
            if not self.visible:
                return self.hidden_displayable
            elif self.maximized:
                return self.large_displayable
            else:
                return self.small_displayable

        #  Useful 4 debug

        def __str__(self):
            return(u'{0} {1}'.format(self.suit, self.number))

        #  Two methods that switch displayables

        def maximize(self):
            self.maximized = True
            self.large_displayable.xpos = self.small_displayable.xpos
            self.large_displayable.ypos = self.small_displayable.ypos
            self.large_displayable.transform.xpos = self.small_displayable.transform.xpos
            self.large_displayable.transform.ypos = self.small_displayable.transform.ypos
            self.large_displayable.transform.update()

        def minimize(self):
            self.maximized = False
            self.small_displayable.xpos = self.large_displayable.xpos
            self.small_displayable.ypos = self.large_displayable.ypos
            self.small_displayable.transform.xpos = self.large_displayable.transform.xpos
            self.small_displayable.transform.ypos = self.large_displayable.transform.ypos
            self.small_displayable.transform.update()

    class CardHiddenDisplayable(renpy.Displayable):
        """
        Displayable for card player can't see
        """
        def __init__(self, **kwargs):
            super(CardHiddenDisplayable, self).__init__(xysize=(100, 140), xfill=False, yfill=False, **kwargs)
            self.bg = LiveTile( 'images/ROOBASTSHKA.png')
            self.frame = Solid('#6A3819')
            self.xpos = 0
            self.ypos = 0
            self.xsize = 100
            self.ysize = 140
            self.x_offset = 0
            self.y_offset = 0
            self.transform = Transform(child=self)


        def render(self, width, height, st, at):
            frame_render = renpy.render(self.frame, self.xsize, self.ysize, st, at)
            bg_render = renpy.render(self.bg, self.xsize-4, self.ysize-4, st, at)
            render = renpy.Render(width, height, st, at)
            render.blit(frame_render, (0,0))
            render.blit(bg_render, (2, 2))
            return render

        def visit(self):
            return[self.frame, self.bg]

        def per_interact(self):
            renpy.redraw(self, 0)

        def reinit_transform(self):
            #  Card size
            self.transform.xsize = 100
            self.transform.ysize = 140
            #  Card position
            self.transform.xpos = 0
            self.transform.ypos = 0
            self.x_offset = 0
            self.y_offset = 0
            self.transform.update()

    class CardSmallDisplayable(renpy.Displayable):
        """
        Regular card displayable
        """
        def __init__(self, card, **kwargs):
            super(CardSmallDisplayable, self).__init__(xysize=(100, 140), xfill=False, yfill=False, **kwargs)
            self.bg = (card.spendable == True and Solid(SPENDABLE_COLOR) or Solid(PERMANENT_COLOR))
            self.frame = Solid('#6A3819')
            self.text = Text(u'{0}{1}'.format(card.number, card.suit[0]), color = '#6A3819')
            self.xpos = 0
            self.ypos = 0
            self.xsize = 100
            self.ysize = 140
            self.x_offset = 0
            self.y_offset = 0
            self.transform = Transform(child=self)

        def render(self, width, height, st, at):
            """
            Return 100*140 render for a card
            """
            frame_render = renpy.render(self.frame, self.xsize, self.ysize, st, at)
            bg_render = renpy.render(self.bg, self.xsize-4, self.ysize-4, st, at)
            text_render = renpy.render(self.text, width, height, st, at)
            render = renpy.Render(width, height, st, at)
            render.blit(frame_render, (0, 0))
            render.blit(bg_render, (2, 2))
            render.blit(text_render, (10, 10))
            return render

        def visit(self):
            return[self.frame,
                   self.bg,
                   self.text]

        def reinit_transform(self):
            #  Card size
            self.transform.xsize = 100
            self.transform.ysize = 140
            #  Card position
            self.transform.xpos = 0
            self.transform.ypos = 0
            self.x_offset = 0
            self.y_offset = 0
            self.transform.update()


    class CardLargeDisplayable(renpy.Displayable):
        """
        Expanded card displayable
        """
        def __init__(self, card, **kwargs):
            super(CardLargeDisplayable, self).__init__(xysize=(200, 280), xfill=False, yfill=False, **kwargs)
            self.text = Text(u'{0}{1}'.format(card.number, card.suit[0]), color = '#6A3819', font='Hangyaboly.ttf')
            self.t_text = Text(card.tooltip, size = 14, color = '#6A3819', font='Hangyaboly.ttf')
            self.bg = (card.spendable == True and Solid(SPENDABLE_COLOR) or Solid(PERMANENT_COLOR))
            self.frame = Solid('#6A3819')
            self.xpos = 0
            self.ypos = 0
            self.xsize = 200
            self.ysize = 280
            self.x_offset = 0
            self.y_offset = 0
            self.transform = Transform(child=self)

        def reinit_transform(self):
            """
            Renitialise card Transform that contains its position and stack it belongs to.
            Should be called any time screen is initialized, currently called from Cardbox.__init__()
            """
            #  Card size
            self.transform.xsize = 200
            self.transform.ysize = 280
            #  Card position
            self.transform.xpos = 0
            self.transform.ypos = 0
            self.x_offset = 0
            self.y_offset = 0
            self.transform.update()

        def render(self, width, height, st, at):
            """
            Return 200*280 render for a card
            """
            frame_render = renpy.render(self.frame, width, height, st, at)
            bg_render = renpy.render(self.bg, 196, 276, st, at)
            text_render = renpy.render(self.text, width, height, st, at)
            t_text_render = renpy.render(self.t_text, width, height, st, at)
            render = renpy.Render(width, height, st, at)
            render.blit(frame_render, (0, 0))
            render.blit(bg_render, (2, 2))
            render.blit(text_render, (10, 10))
            render.blit(text_render, (160, 250))
            render.blit(t_text_render, (5, 120))
            return render

        def visit(self):
            return [self.text, self.t_text, self.bg]

        def __eq__(self, other):
            return False

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
            ui.add(card.get_displayable())
        for j in range(rows*3 - len(player_deck)):
            ui.add(Null())
        ui.close()  # For grid
        ui.close()  # For fixed
        # The following is outside the window!
        ui.textbutton(u"Продолжить", action = Hide('collection'), xalign = 0.5, yalign = 0.95)

    renpy.define_screen('collection', card_collection, modal = 'True', zorder='10')

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
        def __init__(self, card_list=[], stack_id='NO ID', accept_from = None, allow_positioning = False,
                     x=0, y=0, xsize=300, ysize=300):
            # Position on screen
            self.x = x
            self.y = y
            self.id = stack_id
            self.xsize = xsize
            self.ysize = ysize
            self.allow_positioning = allow_positioning
            if accept_from is not None:
                self.accept_from = accept_from
            # Adding cards
            self.card_list = []
            if len(card_list)>0:
                for card in sorted(card_list, key=lambda x: x.number):
                    card.minimize()
                    (card.get_displayable().transform.xpos, card.get_displayable().transform.ypos) = self.position_next_card(card)
                    self.append(card)
            # if self.card_list:
            #     for card in self.card_list:
            #         card.minimize()
            #         card.stack = self.id
            #     self.position_cards()

        # Card positioning methods

        def position_next_card(self, card):
            """
            Return position of the next card to be added
            Places the next card 50 px under the lowest one, no matter what. Children should provide more reasonable
            positioning algorithms.
            """
            if len(self.card_list) == 0:
                return int(self.x+self.xsize/2-100), self.y + 10
            else:
                # Get coordinates, sorted by y
                coords = max(((c.get_displayable().transform.xpos, c.get_displayable().transform.ypos) for c in self.card_list), key=lambda c: c[1])
                #  Add the next card 50 px under the lowest one
                return coords[0], coords[1]+50

        # def position_cards(self):
        #     """
        #     Initially position cards for cardbox.
        #     As with previous method, doesn't particularly care about design and shit
        #     """
        #     # x = self.x + self.xsize/2 - 100
        #     # y = self.y + 10
        #     # self.card_list[0].get_displayable().transform.xpos = x
        #     # self.card_list[0].get_displayable().transform.ypos = y
        #     # self.card_list[0].get_displayable().transform.update()
        #     # for card in self.card_list[1:]:
        #     #     y += 40
        #     #     card.get_displayable().transform.xpos = x
        #     #     card.get_displayable().transform.ypos = y
        #     #     card.get_displayable().transform.update()


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

    class TraderShoppingStack(Cardbox):
        """
        Stack for trader hand.
        Overloaded .remove decreases withheld if card moved back from T_OFFER
        """
        def __init__(self, **kwargs):
            super(TraderShoppingStack, self).__init__(**kwargs)

        def append(self, card):
            global withheld
            withheld -= card.cost
            super(TraderShoppingStack, self).append(card)

        def give(self, card):
            return True

        def accept(self, card, origin=None):
            if origin in self.accept_from:
                return True
            else:
                return False


    class DeckStack(Cardbox):
        """
        Stack that gives all cards and accepts none, but contains no more logic.
        Used in Deck screen. Giving is necessary to allow dragging cards
        """
        def __init__(self, **kwargs):
            super(DeckStack, self).__init__(**kwargs)

        def accept(self, card, origin=None):
            return False

        def give(self, card):
            return True

        def position_next_card(self, card):
            super(DeckStack, self).position_next_card(card)

    class PlayerConflictStack(Cardbox):
        """
        Player hand for conflict screen. Does not accept cards and positioning may break if this rule is violated!
        """
        def __init__(self, **kwargs):
            #  Setting starting points for card placement. This should be done before super.__init__
            #  (and, thus, self.position_next_card) is called
            suits = set(x.suit for x in kwargs['card_list'])
            lengths = {}
            for suit in suits:
                l = len([x for x in kwargs['card_list'] if x.suit == suit])
                if l>0:
                    lengths[suit] = (l-1)*40 + 100 #  Length in pixels
            self.next_pos = {}
            x = kwargs['x']
            y = kwargs['y'] + 10
            if sum(lengths.values()) < kwargs['xsize']:
                #  All lines fit in a single row
                spacer_len = (kwargs['xsize'] - sum(lengths.values()))/(len(lengths)+1)
                for suit in sorted(lengths.keys()):
                    x += spacer_len
                    self.next_pos[suit] = [x, y]
                    x += lengths[suit]
            else:
                #  TO DO: add multiline positioning
                raise NotImplementedError('Cannot use more than one line of cards')
            super(PlayerConflictStack, self).__init__(**kwargs)

        def accept(self, card, origin=None):
            return False

        def give(self, card):
            return True

        def position_next_card(self, card):
            self.next_pos[card.suit][0] += 40
            return self.next_pos[card.suit]

    class OpponentConflictStack(Cardbox):
        """
        Opponent hand for conflict
        """
        def __init__(self, **kwargs):
            super(OpponentConflictStack, self).__init__(**kwargs)

        def accept(self, card, origin=None):
            return False

        def give(self, card):
            return False

        def position_cards(self):
            """
            Position cards for an opponent conflict stack. Much like Cardbox.position_cards(), but places
            cards horizontally rather than vertically
            """
            x = self.x + self.xsize/2 - (40*(len(self.card_list)-1)+100)/2
            y = self.y + 10
            self.card_list[0].get_displayable().transform.xpos = x
            self.card_list[0].get_displayable().transform.ypos = y
            self.card_list[0].get_displayable().transform.update()
            for card in self.card_list[1:]:
                #y += renpy.random.randint(-7, 7)
                x += 40
                card.get_displayable().transform.xpos = x
                card.get_displayable().transform.ypos = y
                card.get_displayable().transform.update()


    class MidStack(Cardbox):
        """
        Central stack for the conflict
        """
        def __init__(self, **kwargs):
            super(MidStack, self).__init__(**kwargs)
            #  Position of the last card added
            self.last_x = int(self.x+self.xsize/2-100)
            self.last_y = self.y

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

        def position_next_card(self, card):
            if len(self.card_list) == 0:
               return int(self.x+self.xsize/2-100), self.y
            if self.ysize + self.y - self.last_y <= 140:
                #  if one more card will not fit in the desk
                self.last_x += 110
                self.last_y = self.y-40 # It will be added back right in the next line
            return(self.last_x, self.last_y+40)

        def append(self, card):
            """
            Remember where the player placed his last card, so that it will be covered
            """
            self.last_x = card.get_displayable().transform.xpos
            self.last_y = card.get_displayable().transform.ypos
            self.card_list.append(card)


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
            self.old_position = len(self.cards) - 1
            self.drag_text = Text('None dragged')
            self.dragged = None
            self.drag_start = (0, 0)
            #  Debug Cardbox highlighters
            self.cardboxes = []
            for x in self.stacks:
                self.cardboxes.append(Solid('#10101020'))

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
                self.render_object.place(card.get_displayable().transform)
            return self.render_object

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                #  Checking if we have clicked any cards:
                card_clicked = False
                for card in reversed(self.cards):
                    if inside((x,y), (card.get_displayable().transform.xpos, card.get_displayable().transform.ypos, card.get_displayable().xsize, card.get_displayable().ysize)):
                        self.drag_start = (x, y)
                        # card.maximize()
                        self.initial_card_position = (card.get_displayable().transform.xpos, card.get_displayable().transform.ypos)
                        self.dragged = card
                        self.dragged.get_displayable().x_offset = self.dragged.get_displayable().transform.xpos - x
                        self.dragged.get_displayable().y_offset = self.dragged.get_displayable().transform.ypos - y
                        #  Show dragged on the top of other cards
                        #  But remember where it was just in case
                        if self.cards.index(self.dragged) < len(self.cards)-1:
                            #  If the card is already in the latest position, this piece is unnecessary.
                            #  Even worse, it risks overwriting the valuable self.old_position, which harms DeckScreen
                            self.old_position = self.cards.index(self.dragged)
                            self.cards.append(self.cards.pop(self.old_position))
                        card_clicked = True
                        break  #  No need to move two cards at the same time
                if not card_clicked:
                    #  If no card was clicked on, look for any maximized cards and minimize them
                    for card in self.cards:
                        if card.maximized:
                            self.cards.insert(self.old_position, card)
                            self.cards.pop()
                            card.minimize()
                renpy.restart_interaction()

            elif ev.type == pygame.MOUSEMOTION and self.dragged is not None:
                #  Just redrawing card in hand
                self.dragged.maximize()
                self.dragged.get_displayable().transform.xpos = x + self.dragged.get_displayable().x_offset
                self.dragged.get_displayable().transform.ypos = y + self.dragged.get_displayable().y_offset
                self.dragged.get_displayable().transform.update()
                renpy.restart_interaction()

            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
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
                                    if accepting_stack.accept(self.dragged, origin=self.dragged.stack) and self.get_stack_by_id(self.dragged.stack).give(self.dragged):
                                        is_accepted = True
                                        self.get_stack_by_id(self.dragged.stack).remove(self.dragged)
                                        #  If a stack does not allow positioning in any place, ask it for card coord
                                        if not accepting_stack.allow_positioning:
                                            #  This could've been a single line, but properties chains would be so long
                                            #  one could think it was Java
                                            coords = accepting_stack.position_next_card(self.dragged)
                                            self.dragged.get_displayable().transform.xpos = coords[0]
                                            self.dragged.get_displayable().transform.ypos = coords[1]
                                        accepting_stack.append(self.dragged)
                                else:
                                    #  Set this to True to enable card rearrangement within stack
                                    is_accepted = False

                        if not is_accepted:
                            #  If card was not accepted, it should be returned where it belongs
                            self.dragged.get_displayable().transform.xpos = self.initial_card_position[0]
                            self.dragged.get_displayable().transform.ypos = self.initial_card_position[1]
                            self.cards.pop()
                            self.cards.insert(self.old_position, self.dragged)

                        #  Dragging has ended somehow anyway

                        self.dragged.minimize()
                        self.dragged.get_displayable().transform.update()
                        self.dragged = None
                        # renpy.restart_interaction()


                else:
                    #  Things to do upon click
                    #  Yeah, probably some card was clicked. For some reason this part is not entered when clicking
                    #  outside the card.
                    if self.dragged is not None:# and self.dragged.stack in self.automove.keys():
                        if not self.dragged.maximized:
                            #  On first click we only expand a card, but don't play it
                            self.dragged.maximize()
                        elif self.dragged.stack in self.automove.keys():
                            # On second click card actually is played (and minimized)
                            #  First of all check whether transfer is possible
                            old_stack = self.get_stack_by_id(self.dragged.stack)
                            new_stack = self.get_stack_by_id(self.automove[old_stack.id])
                            if old_stack.give(self.dragged) and new_stack.accept(self.dragged, origin=old_stack.id):
                                #  Positioning card should happen before appending
                                #  Because it uses the accepting stack's card_list to define card position
                                #  The small displayable should be available for positioning as well
                                self.dragged.minimize()
                                new_coords = new_stack.position_next_card(self.dragged)
                                (self.dragged.get_displayable().transform.xpos, self.dragged.get_displayable().transform.ypos) = new_coords
                                self.dragged.get_displayable().transform.update()
                                #  Remove dragged card from its initial stack and move it to acceptor
                                old_stack.remove(self.dragged)
                                new_stack.append(self.dragged)
                                self.dragged.stack = new_stack.id
                        else:
                            #  If the card was expanded, but it cannot be played
                            self.cards.insert(self.old_position, self.dragged)
                            self.cards.pop()
                            self.dragged.minimize()
                        #  Release dragged card anyway
                        self.dragged = None
                        renpy.restart_interaction()

                #  Restart interaction to check for success, flip exit button state, etc.
                renpy.restart_interaction()

        def visit(self):
            l = []
            l+=(x.get_displayable().transform for x in self.cards)
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
                    card.visible = True
                    self.get_stack_by_id('O_HAND').remove(card)
                    (card.get_displayable().transform.xpos, card.get_displayable().transform.ypos) = self.get_stack_by_id('M_STACK').position_next_card(card)
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
                # if there were no playable cards to start with
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

    class DeckTable(Table):
        """
        The Table for a deck view. Is expected to contain 4 non-active Cardboxes (one for each suit).
        Also has a small display space for value sums and such
        """
        def __init__(self, **kwargs):
            super(DeckTable, self).__init__(**kwargs)
            # Initializing stack description lines
            self.money_line = Text(u'Деньги: {0} ({1})'.format(sum((x.number for x in self.get_stack_by_id('MONEY').card_list)),
                                                                  len(self.get_stack_by_id('MONEY').card_list)),
                                   color='#6A3819', size=30)
            self.force_line = Text(u'Сила: {0} ({1})'.format(sum((x.number for x in self.get_stack_by_id('FORCE').card_list)),
                                                                  len(self.get_stack_by_id('FORCE').card_list)),
                                   color='#6A3819', size=30)
            self.intrigue_line = Text(u'Интриги: {0} ({1})'.format(sum((x.number for x in self.get_stack_by_id('INTRIGUE').card_list)),
                                                                  len(self.get_stack_by_id('INTRIGUE').card_list)),
                                   color='#6A3819', size=30)
            self.knowledge_line = Text(u'Знания: {0} ({1})'.format(sum((x.number for x in self.get_stack_by_id('KNOWLEDGE').card_list)),
                                                                  len(self.get_stack_by_id('KNOWLEDGE').card_list)),
                                   color='#6A3819', size=30)

        def render(self, width, height, st, at):
            render = super(DeckTable, self).render(width, height, st, at)
            money_line_render = renpy.render(self.money_line, width, height, st, at)
            force_line_render = renpy.render(self.force_line, width, height, st, at)
            intrigue_line_render = renpy.render(self.intrigue_line, width, height, st, at)
            knowledge_line_render = renpy.render(self.knowledge_line, width, height, st, at)
            render.blit(money_line_render, (100, 620))
            render.blit(force_line_render, (350, 620))
            render.blit(intrigue_line_render, (600, 620))
            render.blit(knowledge_line_render, (850, 620))
            return render

        def per_interact(self):
            """
            This table requires no activity
            :return:
            """
            renpy.redraw(self, 0)

        def visit(self):
            """
            Return all the children of this Table
            :return:
            """
            ret = super(DeckTable, self).visit()
            return ret
            ret.extend((self.money_line, self.force_line. self.intrigue_line, self.knowledge_line))

        def finalize_success(self):
            pass


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
            trade_table = None
            renpy.hide_screen('trade_buttons_screen')
            renpy.restart_interaction()

        def get_sensitive(self):
            global paid
            global withheld
            return paid >= withheld


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
        xalign 0.5
        yalign 0.5

screen conflict_failure_screen():
    modal True
    zorder 10
    textbutton u"Вы проиграли":
        action [Hide('conflict_table_screen'), Hide('conflict_failure_screen')]
        xalign 0.5
        yalign 0.5

screen deck_hide_screen:
    zorder 10
    textbutton u"Колода":
        action [Hide('deck_screen'), Hide('deck_hide_screen')]
        xalign 0.5
        xanchor 0.5
        yalign 0.95

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
        global gl_no_rollback
        if gl_no_rollback:
            renpy.block_rollback()
        #  Opponent deck may be either a list of cards or a deckline
        assert (type(opponent_deck) is list and all(type(x) is Card for x in opponent_deck)) or type(opponent_deck) is str
        if type(opponent_deck) is unicode:
            opponent_deck = deck(opponent_deck)
        #  Hide opponent's cards
        for card in opponent_deck:
            card.visible = False
        # List of acceptable suits
        suits=set(x.suit for x in opponent_deck)
        # Player stack takes the entire bottom of the screen
        p_hand_stack = PlayerConflictStack(card_list=[x for x in player_deck if x.suit in suits],
                                           stack_id='P_HAND',
                                           accept_from=[],
                                           x=50, y=500, xsize=920, ysize=268)
        mid_stack = MidStack(card_list=[], stack_id='M_STACK', accept_from=['P_HAND', 'O_HAND'],
                             x=50, y=175, xsize=920, ysize=300)
        # Opponent stack takes bottom and doesn't need more than one line of cards, so it's narrow
        o_hand_stack = OpponentConflictStack(card_list=opponent_deck, stack_id='O_HAND',
                                             x=50, y=0, xsize=920, ysize=150)
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
        global trade_table
        global paid
        global withheld
        global gl_no_rollback
        if gl_no_rollback:
            renpy.block_rollback()
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
        t_hand_stack = TraderShoppingStack(card_list=stock, stack_id='T_HAND', accept_from=['T_OFFER'],
                                           x=800, y=100, xsize=300, ysize=500)
        a = {'P_HAND': 'P_OFFER', 'T_HAND': 'T_OFFER', 'T_OFFER': 'P_HAND', 'P_OFFER': 'P_HAND'}
        trade_table = TradeTable(stacks=[p_hand_stack, t_hand_stack, p_offer_stack, t_offer_stack], automove=a)
        renpy.show_screen('trade_screen')
        renpy.show_screen('trade_buttons_screen')

    def init_deck_table():
        """
        Initialize a deck view screen and show it
        :return:
        """
        global player_deck
        global deck_table
        #  Defining 4 separate stacks, one for each suit
        money_stack = DeckStack(card_list=[x for x in player_deck if x.suit == u'Деньги'],
                                stack_id='MONEY', #accept_from=None,
                                x=100, xsize=220,
                                y=100, ysize=500)
        force_stack = DeckStack(card_list=[x for x in player_deck if x.suit == u'Сила'],
                                stack_id='FORCE', accept_from=None,
                                x=350, xsize=220,
                                y=100, ysize=500)
        intrigue_stack = DeckStack(card_list=[x for x in player_deck if x.suit == u'Интриги'],
                                   stack_id='INTRIGUE', accept_from=None,
                                   x=600, xsize=220,
                                   y=100, ysize=500)
        knowledge_stack=DeckStack(card_list=[x for x in player_deck if x.suit == u'Знания'],
                                  stack_id='KNOWLEDGE', accept_from=None,
                                  x=850, xsize=220,
                                  y=100, ysize=500)
        deck_table = DeckTable(stacks=[money_stack, force_stack, intrigue_stack, knowledge_stack], automove={})
        renpy.show_screen('deck_screen')
        renpy.show_screen('deck_hide_screen')



init:
    screen trade_screen():
        modal True
        zorder 9
        add trade_table

    screen conflict_table_screen():
        modal True
        zorder 9
        add conflict_table

    screen deck_screen():
        modal True
        zorder 9
        add deck_table