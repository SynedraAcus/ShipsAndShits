#Main game script. All card-related python is in cardistry.rpy

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define narrator = Character(None, kind = nvl, what_color="#000000", size = 10)

init python:
    menu = nvl_menu
    gl_no_rollback = True
    # Initialising global conflict variables so they exist when we call init_conflict()
    stack = []
    opponent_deck = []
    ret = ''
    price = '0'
    # Initialising starting position
    current_port = monet
    player_deck = deck(u'0С1С4Д0С1С4Д0С1С4Д0С1С4Д')
    player_deck.append(Card(u'З', 7, spendable = True, tooltip = u'Эта карта не перманентна; в отличие от прочих она серая'))


#  This is the beginning, from the very start to the first trip from Monet
label start:
    $ vortex_firsttime = 0
    $ gl_cargo = []
    $ gl_knowhow = []
    $ gl_cargo_jerry = 0
    $ gl_you_are_terrible = 0
    $ useless_variable = 0
    $ useless_variable_2 = 0
    image bg solid_bg = Solid('#EEE')
    show bg solid_bg
    "Вы видите перед собой Порт Моне. Короли-развратники, торговцы, политики, вот это всё."
    "Поскольку тексты не написаны, насладиться обаянием этого города вы не можете."
    "Тем не менее, кое-что тут сделать всё-таки можно:"
    menu:
        "Вступить в беспричинный конфликт":
            #nvl clear
            jump gamble
        "Перечитать предыдущие три строчки":
            nvl clear
            jump start
        "Куда-нибудь поплыть":
            nvl clear
            jump map_label
        "Включить торговый экран":
            nvl clear
            jump trade_test
        "Включить новый экран конфликта":
            nvl clear
            jump new_conflict

label new_conflict:
    "Включаем"
    $ test_table = Table(stacks=[Cardbox(player_deck, x = 0, y = 0, xsize = 300, ysize = 1000, give_function = lambda a: False, accept_function = lambda a: True), Cardbox([], x=400, y=0, xsize=300, ysize=1000, give_function=lambda a: False, accept_function = lambda a: True)])
    screen test_screen:
        add test_table
        modal True
        zorder 10
    show screen test_screen
    jump start

label trade_test:
    $ test_card = Card(u'Д', 10, spendable=True, tooltip='Эта карта была куплена при тестировании магазина')
    $ init_trade(10, test_card)
    "Здесь вы можете купить десятку денег за десятку денег. Я подозреваю, что в реальности бизнес работает как-то иначе, но для дебага сойдёт"
    show screen trade
    "Включаем магазин"
    if ret == 'Sold':
        "Сделка завершена. Убедитесь в этом на экране колоды."
        jump start
    if ret == 'NotSold':
        "Сделка отменена."
        jump start

label gamble:
    $ init_conflict(u'0З1С')
    show screen conf
    "Вы вступили в конфликт. Ни его цель, ни награда за победу вам не ясны."
    #$ _return = renpy.show_screen('conf')
    if ret[0] == 'F':
        jump failure
    elif ret == u'SЗнания':
        jump success_knowledge
    elif ret == u'SСила':
        jump success_force

label success_knowledge:
    "Вы победили, применив свой безмерный интеллект"
    jump success

label success_force:
    "Вы победили, применив свою безмерную силу"
    jump success

label failure:
    nvl clear
    $ player_deck.append(Card(u'З', 11, spendable = True, tooltip = u'Эта карта была выдана после поражения'))
    "Раз уж вы потерпели поражение, ваша колода была усилена"
    "Теперь поражение невозможно в принципе"
    jump gamble

label success:
    "Вы победили в нашей игре"
    return

label map_label:
    show screen map_screen
    "Showing map"

#  The rest is in port files, even Monet's events