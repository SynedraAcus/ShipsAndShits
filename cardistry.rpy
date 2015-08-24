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
            super(Card, self).__init__(xysize=(200, 100), xfill=False, yfill=False, **kwargs)
            self.suit = SUITS[suit]
            if number == 0:
                number = 10
            self.number = number
            self.spendable = spendable
            self.tooltip = tooltip
            self.text = Text(u'{0} {1}'.format(self.suit, number), color = '#6A3819', font='Hangyaboly.ttf')
            spendability = (self.spendable == True and u'Тратится' or u'Перманент')
            self.t_text = Text(tooltip, size = 12, color = '#6A3819', font='Hangyaboly.ttf')
            self.bg = (self.spendable == True and Solid(SPENDABLE_COLOR) or Solid(PERMANENT_COLOR))

        def __str__(self):
            return(u' '.join([unicode(self.number), self.suit]))

        def render(self, width, height, st, at):
            bg_render = renpy.render(self.bg, width, height, st, at)
            text_render = renpy.render(self.text, width, height, st, at)
            t_text_render = renpy.render(self.t_text, width, height, st, at)
            render = renpy.Render(width, height, st, at)
            render.blit(bg_render, (0,0))
            render.blit(text_render, (10,10))
            render.blit(t_text_render,(10,40))
            return render

        def per_interact(self):
            renpy.redraw(self,0)

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
        Screen for card game. All buttons here use style.card_button
        '''
        # Defining UI elements
        global player_deck
        global stack
        global opponent_deck
        global ret
        #ui.frame(id='conflict_window', background=Solid('0000'), area = (0.0, 0.00, 1.0, 0.85))
        #ui.add(Solid('0000'))
        ui.fixed(id='conflict_fixed', xpos=0.0, ypos=0.0)
        ui.viewport(id = 'hand_view', xmaximum = 220, mousewheel=True, \
        draggable = True, yadjustment=ui.adjustment(), ymaximum = 0.9)
        ui.vbox(id = 'p_hand', spacing = 10, xalign=0.05, ysize = 220*len(player_deck))
        # Player's deck
        for card in (x for x in player_deck if x not in stack if x.suit in {y.suit for y in opponent_deck}):
            ui.button(action = CardMove(card), style=style.card_button)
            ui.add(card, align = (0.5, 0.5))
        ui.close()
        # Played cards
        ui.vbox(id = 'stack', spacing = 10, xalign = 0.4, ymaximum = 0.9)
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
                action=[Hide('conf'), SetVariable('ret', 'Defeat')], style=style.card_button)
            try:
                opponent_deck.remove(stack[-1])
            except ValueError: # No clue where this exception comes from, but all works well if we just catch it
                pass
        if len(stack)%2==1:
            # This is cute: stack has an odd amount of cards iff oppponent didn't play during button actions
            # Even better: 0%2==1 so no worries about empty stack
            ui.textbutton('You win', xalign=0.5, xanchor=0.5, yalign=0.95, \
            action=[SetVariable('ret', stack[-1].suit), Hide('conf')], style=style.card_button)
        ui.vbox(id = 'o_hand', spacing = 10, xalign = 0.85)
        for card in opponent_deck:
            ui.add(card)
        ui.close()
        ui.close()

    def card_collection(**kwargs):
        '''
        Screen that shows card collection
        '''
        global player_deck
        ui.window(id='collection_window', background=Frame('images/Tmp_frame.png', 5, 5), area = (0.05, 0.05, 0.9, 0.85))
        ui.fixed(id='collection_fixed', xpos=0.0, ypos=0.0)
        ui.text(u"Колода", color='#000000', xalign=0.5, ypos=0)
        rows = int(math.ceil(len(player_deck)/3.0))
        ui.viewport (id='collection_viewport', scrollbars='vertical', mousewheel = True, ypos=0.1, yanchor=0, ysize=0.9, xfill=True)
        ui.grid(3, rows, id='collection_grid', transpose = False, spacing = 5)
        for card in player_deck:
            ui.add(card)
        for j in range(rows*3 - len(player_deck)):
            ui.add(Null())
        ui.close()  # For grid
        ui.close()  # For fixed
        # The following is outside the window!
        ui.textbutton(u"Продолжить", action = Hide('collection'), xalign = 0.5, yalign = 0.95)

    renpy.define_screen('conf', conflict, modal='True', zorder=10)
    renpy.define_screen('collection', card_collection, modal = 'True', zorder=10)
