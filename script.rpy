#Main game script. All card-related python is in cardistry.rpy

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define narrator = Character(None, kind = nvl, what_color="#000000", size = 10)

init python:
    menu = nvl_menu
    # Initialising global conflict variables so they exist when we call init_conflict()
    stack = []
    opponent_deck = []
    ret = ''
    # Initialising starting position
    current_port = monet


#  This is the beginning, from the very start to the first trip from Monet
label start:
    $ player_deck = deck(u'0С1С4Д0С1С4Д0С1С4Д0С1С4Д')
    $ player_deck.append(Card(u'З', 7, spendable = True, tooltip = u'Эта карта не перманентна; в отличие от прочих она серая'))
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
    #nvl clear

label gamble:

    $ init_conflict(u'0З1С')
    show screen conf
    "Вы вступили в конфликт. Ни его цель, ни награда за победу вам не ясны."
    #$ _return = renpy.show_screen('conf')
    if ret == 'Defeat':
        jump failure
    elif ret == u'Знания':
        jump success_knowledge
    elif ret == u'Сила':
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
    call screen map_screen
    "Showing map"
