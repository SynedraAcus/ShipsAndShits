label plains:
    nvl clear
    hide screen nvl
    scene bg plains_yurts_image
    $ renpy.pause(None)
    "Вы прибыли в тартарские степи."
    "К сожалению, делать тут практически нечего. Можно разве что сходить посмотреть на коней."
    menu:
        "Сходить":
            jump plains_horses
        "Не ходить":
            jump plains_quit

label plains_horses:
    nvl clear
    hide screen nvl
    scene bg plains_horses_image
    $ renpy.pause(None)
    "Вы посмотрели на лошадей. А теперь отправляйтесь-ка куда-нибудь, где есть текст."
    jump plains_quit

label plains_quit:
    show screen map_screen
    "NOTHING"