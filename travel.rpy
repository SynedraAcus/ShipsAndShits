# Everything related to travels

screen map_screen:
    tag map
    modal True
    zorder 10
    imagemap:
        auto 'images/1024map_%s.png'
        #  Main cities
        hotspot (132, 610, 37, 37) action Travel(monet)
        hotspot (246, 90, 27, 27) action Travel(tartari)
        hotspot (570, 95, 27, 27) action Travel(plains)
        hotspot (639, 320, 27, 27) action Travel(poop)
        hotspot (896, 364, 27, 27) action Travel(office)
        hotspot (352, 418, 27, 27) action Travel(yankee)
        hotspot (632, 495, 27, 27) action Travel(vortex)
        hotspot (581, 661, 27, 27) action Travel(monastery)
        #  Nodes (in no particular order)
        hotspot (203, 550, 14, 14) action Travel(node3)
        hotspot (130, 706, 14, 14) action Travel(node1)
        hotspot (289, 693, 14, 14) action Travel(node2)
        hotspot (140, 142, 14, 14) action Travel(node16)
        hotspot (321, 190, 14, 14) action Travel(node17)
        hotspot (451, 164, 14, 14) action Travel(node18)
        hotspot (647, 198, 14, 14) action Travel(node19)
        hotspot (802, 202, 14, 14) action Travel(node20)
        hotspot (383, 309, 14, 14) action Travel(node13)
        hotspot (485, 337, 14, 14) action Travel(node14)
        hotspot (857, 312, 14, 14) action Travel(node15)
        hotspot (98, 359, 14, 14) action Travel(node12)
        hotspot (262, 415, 14, 14) action Travel(node9)
        hotspot (551, 423, 14, 14) action Travel(node10)
        hotspot (720, 385, 14, 14) action Travel(node11)
        hotspot (387, 565, 14, 14) action Travel(node4)
        hotspot (520, 534, 14, 14) action Travel(node7)
        hotspot (812, 469, 14, 14) action Travel(node8)
        hotspot (625, 605, 14, 14) action Travel(node5)
        hotspot (812, 657, 14, 14) action Travel(node6)

init -2 python:
    class Travel(Action):
        def __init__(self, map_point, **kwargs):
            super(Action, self).__init__(**kwargs)
            self.map_point = map_point

        def __call__(self):
            global current_port
            current_port = self.map_point
            renpy.hide_screen('map')
            renpy.jump(self.map_point.label)
            #renpy.Return()

        def get_sensitive(self):
            global current_port
            if self.map_point.check_connected(current_port):
                return True
            else:
                return False

    class Map_point():
        def __init__(self, name, label = ''):
            '''
            Create a map_point object. If label is not specified,
            it is the same as name of that object
            '''
            self.name = name
            if not label == '':
                self.label = label
            else:
                self.label = name
            self.connected = []

        def set_connected(self, other_point):
            self.connected.append(other_point)

        def check_connected(self, other_point):
            if other_point in self.connected:
                return True
            else:
                return False

        def list_connected(self):
            return self.connected

    # Map initialisation
    monet = Map_point('monet')
    node1 = Map_point('node1')
    node2 = Map_point('node2')
    node3 = Map_point('node3')
    for x in (node1, node3):
        monet.set_connected(x)
        x.set_connected(monet)
    node1.set_connected(node2)
    node2.set_connected(node1)