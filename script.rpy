#Main game script. All card-related python is in cardistry.rpy

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define narrator = Character(None, kind = nvl, what_color="#000000", size = 10)

# Test screen definitions

init python:
    menu = nvl_menu
    # Initialising global conflict variables so they exist when we call init_conflict()
    stack = []
    opponent_deck = []
    ret = ''


# The game starts here.
label start:
    $ player_deck = deck(u'0С1С4Д0С1С4Д0С1С4Д0С1С4Д')
    $ player_deck.append(Card(u'З', 7, spendable = True, tooltip = u'Эта карта не перманентна; в отличие от прочих она серая'))
    image bg solid_bg = Solid('#EEE')
    show bg solid_bg
    "Посмотреть на все эти прелести ты можешь в следующем конфликте."
    "Как и в прошлый раз, ты можешь проиграть, начав с семёрки знаний."
    menu:
        "Сыграть":
            #nvl clear
            jump gamble
        "Перечитать текст":
            nvl clear
            jump start
    #nvl clear

label gamble:

    $ init_conflict(u'0З1С')
    show screen conf
    "Launching conflict"
    #$ _return = renpy.show_screen('conf')
    if ret == 'Defeat':
        jump failure
    elif ret == u'Знания':
        jump success_knowledge
    elif ret == u'Сила':
        jump success_force

label success_knowledge:
    "Ты умный"
    jump success

label success_force:
    "Ты пизды дал"
    jump success

label failure:
    nvl clear
    $ player_deck.append(Card(u'З', 11, spendable = True, tooltip = u'Эта карта была выдана после поражения'))
    "Тебе выдаётся новая карта - одиннадцать знаний, тоже одноразовая"
    "Обрати внимание: истраченной семёрки у тебя больше нет"
    jump gamble

label success:
    "Всё, ты подебил"
    return
