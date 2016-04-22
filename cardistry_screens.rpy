#  Screen definitions for cardistry.
#  Everything that is related to that system and is not Python belongs here

#  TRADE

screen trade_screen():
    modal True
    zorder 9
    add trade_table

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

#  CONFLICT

screen conflict_success_screen():
    modal True
    zorder 100
    imagebutton:
        idle 'images/win_button.png'
        action [Hide('conflict_table_screen'), Hide('conflict_success_screen')]
        xalign 0.5
        yalign 0.5
    text u'НИШТЯК':
        size 150
        xalign 0.5
        yalign 0.7
        font 'Hangyaboly.ttf'
        outlines [(5, '#000000', 0, 0)]

screen conflict_failure_screen():
    modal True
    zorder 100
    imagebutton:
        idle 'images/fail_button.png'
        hover 'images/fail_button.png'
        action [Hide('conflict_table_screen'), Hide('conflict_failure_screen')]
        xalign 0.5
        yalign 0.5
    text u'ОБЛОМ':
        size 150
        xalign 0.5
        yalign 0.7
        font 'Hangyaboly.ttf'
        color '#000000'
        outlines [(5, '#FFFFFF', 0, 0)]

screen conflict_table_screen():
    modal True
    zorder 9
    add conflict_table

#  DECK

screen deck_hide_screen:
    zorder 10
    textbutton u"Колода":
        action [Hide('deck_screen'), Hide('deck_hide_screen')]
        xalign 0.5
        xanchor 0.5
        yalign 0.95

screen deck_screen():
    modal True
    zorder 9
    add deck_table
