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
        def __init__(self, name, label = '', connected = []):
            '''
            Create a map_point object. If label is not specified,
            it is the same as name of that object
            '''
            self.name = name
            if not label == '':
                self.label = label
            else:
                self.label = name

            self.connected = connected

        def check_connected(self, other_point):
            if other_point in self.connected:
                return True
            else:
                return False

        def list_connected(self):
            return self.connected

    # Map points initialization

    #  Cities
    monet = Map_point('monet', connected=[node1, node3])
    tartari = Map_point('tartari', connected=[node16, node17])
    plains = Map_point('plains', connected=[node18, node19])
    vein = Map_point('vein', connected=[node16, node12])
    poop = Map_point('poop', connected=[node11, node14, node20]
    office = Map_point('office', connected=[node8, node11, node15])
    yankee = Map_point('yankee', connected=[node10, node13, node14])
    vortex = Map_point('vortex', connected=[node5, node7, node8, node10, node11])
    monastery = Map_point('monastery', connected=[node5])
    #  Nodes
    node1 = Map_point('node1', connected=[monet, node2])
    node2 = Map_point('node2', connected=[node1, node4])
    node3 = Map_point('node3', connected=[monet, node4, node9, node12])
    node4 = Map_point('node4', connected=[node2, node3, node7, node10])
    node5 = Map_point('node5', connected=[vortex, monastery, node6, node7])
    node6 = Map_point('node6', connected=[node5, node8])
    node7 = Map_point('node7', connected=[node4, node5, node10, vortex])
    node8 = Map_point('node8', connected=[vortex, office, node6, node11])
    node9 = Map_point('node9', connected=[node3, node12, node13, node17])
    node10 = Map_point('node10', connected=[yankee, vortex, node7, node10, node11, node14])
    node11 = Map_point('node11', connected=[poop, office, vortex, node8, node10])
    node12 = Map_point('node12', connected=[vein, node3, node9])
    node13 = Map_point('node13', connected=[yankee, node9, node14, node17, node18])
    node14 = Map_point('node14', connected=[yankee, poop, node10, node13, node18, node19])
    node15 = Map_point('node15', connected=[office, node20])
    node16 = Map_point('node16', connected=[vein, tartari, node17])
    node17 = Map_point('node17', connected=[tartari, node9, node13, node16, node18])
    node18 = Map_point('node18', connected=[plains, node17, node19, node14, node13])
    node19 = Map_point('node19', connected=[plains, node14, node18, node20])
    node20 = Map_point('node20', connected=[poop, node15, node19])
