# Everything related to travels
#
screen map_screen:
    tag map
    modal True
    zorder 2
    imagemap:
        auto 'images/1024map_%s.png'
        #  Main cities
        hotspot monet.hotspot action Travel(monet)
        hotspot tartari.hotspot action Travel(tartari)
        hotspot plains.hotspot action Travel(plains)
        hotspot poop.hotspot action Travel(poop)
        hotspot office.hotspot action Travel(office)
        hotspot yankee.hotspot action Travel(yankee)
        hotspot vortex.hotspot action Travel(vortex)
        hotspot monastery.hotspot action Travel(monastery)
        hotspot vein.hotspot action Travel(vein)
        #  Nodes (in no particular order)
        hotspot node3.hotspot action Travel(node3)
        hotspot node1.hotspot action Travel(node1)
        hotspot node2.hotspot action Travel(node2)
        hotspot node16.hotspot action Travel(node16)
        hotspot node17.hotspot action Travel(node17)
        hotspot node18.hotspot action Travel(node18)
        hotspot node19.hotspot action Travel(node19)
        hotspot node20.hotspot action Travel(node20)
        hotspot node13.hotspot action Travel(node13)
        hotspot node14.hotspot action Travel(node14)
        hotspot node15.hotspot action Travel(node15)
        hotspot node12.hotspot action Travel(node12)
        hotspot node9.hotspot action Travel(node9)
        hotspot node10.hotspot action Travel(node10)
        hotspot node11.hotspot action Travel(node11)
        hotspot node4.hotspot action Travel(node4)
        hotspot node7.hotspot action Travel(node7)
        hotspot node8.hotspot action Travel(node8)
        hotspot node5.hotspot action Travel(node5)
        hotspot node6.hotspot action Travel(node6)
    add 'images/1024ship.png':
        anchor (0.5, 1.0)
        pos current_port.coordinates
        id 'ship'
        #at ship_d

transform ship_d(new_pos):
    linear 1.0 pos new_pos

transform slow:
    pause 5.0

#transform move_ship(x1, y1, x2, y2, time):
#    on update:
#        xpos x1
#        ypos y1
#        linear time xpos x2 ypos y2

init -2 python:
    class Travel(Action):
        def __init__(self, map_point, **kwargs):
            super(Action, self).__init__(**kwargs)
            self.map_point = map_point

        def __call__(self):
            global current_port
            current_port = self.map_point
            ship = renpy.get_widget('map_screen', 'ship')
            ship.pos = current_port.coordinates
            renpy.hide_screen('map')
            renpy.jump(self.map_point.label)

        def get_sensitive(self):
            global current_port
            if self.map_point.check_connected(current_port):
                return True
            else:
                return False

    class Map_point():
        def __init__(self, name, coordinates, label = '', connected = [], hotspot_size=50):
            '''
            Create a map_point object. If label is not specified,
            it is the same as name of that object
            '''
            if not((type(coordinates) is tuple) and (len(coordinates)==2)):
                raise TypeError('Coordinates must be two-item tuple!')
            self.name = name
            self.coordinates = coordinates
            self.hotspot = (coordinates[0]-int(hotspot_size/2),
                           coordinates[1]-int(hotspot_size/2),
                           hotspot_size,
                           hotspot_size)
            self.hotspot_size=hotspot_size
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
    monet = Map_point('monet', (150, 628))
    tartari = Map_point('tartari', (259, 103))
    plains = Map_point('plains', (584, 109))
    vein = Map_point('vein', (134, 267))
    poop = Map_point('poop', (642, 333))
    office = Map_point('office', (909, 377))
    yankee = Map_point('yankee', (365, 431))
    vortex = Map_point('vortex', (645, 518))
    monastery = Map_point('monastery', (594, 674))

    #  Nodes
    node1 = Map_point('node1', (137, 713))
    node2 = Map_point('node2', (296, 700))
    node3 = Map_point('node3', (210, 557))
    node4 = Map_point('node4', (394, 572))
    node5 = Map_point('node5', (632, 612))
    node6 = Map_point('node6', (819, 664))
    node7 = Map_point('node7', (527, 541))
    node8 = Map_point('node8', (819, 476))
    node9 = Map_point('node9', (269, 422))
    node10 = Map_point('node10', (558, 431))
    node11 = Map_point('node11', (727, 392))
    node12 = Map_point('node12', (105, 366))
    node13 = Map_point('node13', (394, 316))
    node14 = Map_point('node14', (492, 344))
    node15 = Map_point('node15', (864, 319))
    node16 = Map_point('node16', (147, 149))
    node17 = Map_point('node17', (328, 197))
    node18 = Map_point('node18', (458, 171))
    node19 = Map_point('node19', (654, 205))
    node20 = Map_point('node20', (809, 209))

    #  *.connected
    monastery.connected=[node5]
    vortex.connected=[node5, node7, node8, node10, node11]
    yankee.connected=[node10, node13, node14]
    office.connected=[node11, node15]
    poop.connected=[node10, node11, node14]
    plains.connected=[node18, node19]
    tartari.connected=[node16, node17]
    monet.connected=[node1, node3]
    vein.connected=[node16, node12]
    node18.connected=[plains, node17, node19, node14, node13]
    node20.connected=[node15, node19]
    node19.connected=[plains, node14, node18, node20]
    node17.connected=[tartari, node9, node13, node16, node18]
    node16.connected=[vein, tartari, node17]
    node15.connected=[office, node11, node20]
    node14.connected=[yankee, poop, node10, node13, node18, node19]
    node13.connected=[yankee, node9, node14, node17, node18]
    node12.connected=[vein, node3, node9]
    node11.connected=[poop, office, vortex, node8, node10, node15]
    node10.connected=[yankee, vortex, poop, node7, node10, node11, node14, node4]
    node9.connected=[node3, node12, node13, node17]
    node8.connected=[vortex, node6, node11]
    node7.connected=[node4, node5, node10, vortex]
    node6.connected=[node5, node8]
    node5.connected=[vortex, monastery, node6, node7]
    node4.connected=[node2, node3, node7, node10]
    node3.connected=[monet, node4, node9, node12]
    node1.connected=[monet, node2]
    node2.connected=[node1, node4]
