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


# The game starts here.
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



################################################
# Everything below is just a placeholder!!!!!!!#
################################################

label monet:
    nvl clear
    "Вы вернулись в Порт Моне"
    menu:
        "Посмотреть, что тут можно делать":
            jump start
        "Посетить другие порты":
            show screen map_screen

label tartari:
    nvl clear
    "Вы прибыли в крепость Тартари"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label plains:
    nvl clear
    "Вы прибыли в тартарские степи"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label vein:
    nvl clear
    "Вы прибыли в Порт Вейн"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label poop:
    nvl clear
    "Вы прибыли на остров Пуп"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label office:
    nvl clear
    "Вы прибыли в Конторск"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label yankee:
    nvl clear
    "Вы прибыли в Порт Янки"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label monastery:
    nvl clear
    "Вы прибыли в Монастырь"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen


#  Node placeholders
label node1:
    nvl clear
    "Вы прибыли в node1."
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node2:
    nvl clear
    "Вы прибыли в node2."
    "К сожалению, делать тут совершенно нечего"
    call screen map_screen

label node3:
    nvl clear
    "Вы прибыли в node3."
    "К сожалению, делать тут совершенно нечего"
    call screen map_screen

label node4:
    nvl clear
    "Вы прибыли в node4"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node5:
    nvl clear
    "Вы прибыли в node5"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node6:
    nvl clear
    "Вы прибыли в node6"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node7:
    nvl clear
    "Вы прибыли в node7"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node8:
    nvl clear
    "Вы прибыли в node8"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node9:
    nvl clear
    "Вы прибыли в node9"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node10:
    nvl clear
    "Вы прибыли в node10"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node11:
    nvl clear
    "Вы прибыли в node11"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node12:
    nvl clear
    "Вы прибыли в node12"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node13:
    nvl clear
    "Вы прибыли в node13"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node14:
    nvl clear
    "Вы прибыли в node14"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node15:
    nvl clear
    "Вы прибыли в крепость Тартари"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node16:
    nvl clear
    "Вы прибыли в node16"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node17:
    nvl clear
    "Вы прибыли в node17"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node18:
    nvl clear
    "Вы прибыли в node18"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node19:
    nvl clear
    "Вы прибыли в node19"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen

label node20:
    nvl clear
    "Вы прибыли в node20"
    "К сожалению, делать тут совершенно нечего"
    show screen map_screen
