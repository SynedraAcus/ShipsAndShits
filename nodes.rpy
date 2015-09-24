#  Script(s) for node events. Each node starts with label node[\d][\d]?\:

label node1:
    label node1_event1:
        nvl clear
        "Вы наблюдаете событие №1, имеющее вероятность 10\%"
        jump node1_quit
    label node1_event2:
        nvl clear
        "Вы наблюдаете событие №2, имеющее вероятность 20\%"
        jump node1_quit
    label node1_event3:
        nvl clear
        "Вы наблюдаете событие №3, имеющее вероятность 20\%"
    label node1_quit:
        show screen map_screen

label node2:
    nvl clear
    label node2_quit:
        show screen map_screen

label node3:
    nvl clear
    label node3_quit:
        show screen map_screen

label node4:
    nvl clear
    label node4_quit:
        show screen map_screen

label node5:
    nvl clear
    label node5_quit:
        show screen map_screen

label node6:
    nvl clear
    label node6_quit:
        show screen map_screen

label node7:
    nvl clear
    label node7_quit:
        show screen map_screen

label node8:
    nvl clear
    label node8_quit:
        show screen map_screen

label node9:
    label node9_quit:
        show screen map_screen

label node10:
    nvl clear
    label node10_quit:
        show screen map_screen

label node11:
    nvl clear
    label node11_quit:
        show screen map_screen

label node12:
    nvl clear
    label node12_quit:
        show screen map_screen

label node13:
    nvl clear
    label node13_quit:
        show screen map_screen

label node14:
    nvl clear
    label node14_quit:
        show screen map_screen

label node15:
    nvl clear
    label node15_quit:
        show screen map_screen

label node16:
    nvl clear
    label node16_quit:
        show screen map_screen

label node17:
    nvl clear
    label node17_quit:
        show screen map_screen

label node18:
    nvl clear
    label node18_quit:
        show screen map_screen

label node19:
    nvl clear
    label node19_quit:
        show screen map_screen

label node20:
    nvl clear
    label node20_quit:
        show screen map_screen
    "NOTHING"