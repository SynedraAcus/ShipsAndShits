# Everything related to travels

screen map_screen:
    tag map
    modal True
    zorder 10
    imagemap:
        auto 'images/1024map_%s.png'
        hotspot (132, 610, 37, 37) action Travel(monet)
        hotspot (203, 550, 14, 14) action Travel(node3)
        hotspot (130, 706, 14, 14) action Travel(node1)
        hotspot (289, 693, 14, 14) action Travel(node2)

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