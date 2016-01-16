# Everything related to travels
#

default coords = monet.coordinates
default old_coords = monet.coordinates
screen map_screen():
    tag map
    modal True
    zorder 2
    if gl_no_rollback:
        $ renpy.block_rollback()
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
        at shiptransform(old_coords, coords)
        anchor (0.5, 1.0)
        #pos current_port.coordinates
        id 'ship'
        #at ship_d

transform shiptransform(old_coords, coords):
    # on replace:
    #     linear 0.5 pos coords
    pos old_coords
    linear 0.5 pos coords

init -5 python:

    def leave_node():
        """
        A simple function that calls current node's _quit label
        :return:
        """
        global current_port
        quit_label = '{0}_quit'.format(current_port.name)
        renpy.jump(quit_label)

    class MapEvent(object):
        """
        A simple class that contains event Ren'Py label, its weight
        and a list of nodes it can be issued at
        """
        def __init__(self, label = None, weight = 1, node_list = None):
            if label is None:
                raise ValueError('MapEvent cannot be created without a label')
            self.label = label
            self.weight = weight
            if node_list:
                self.node_list = node_list
                self.universal = False
            else:
                self.universal = True

    class EventDispatcher(object):
        """
        A singleton that gives nodes the MapEvent they should point to.
        Doesn't check for basic event probability, assumes node did that
        :param basic_probability: float
        """
        def __init__(self):
            self.visited = []  # A list of already visited nodes
            self.event_list = []

        def get_label(self, node):
            """
            Return a label eligible for a given node
            :param node: str
            """
            #  Generating the list of available events for this node
            avail = [x for x in self.event_list if x.universal or node in x.node_list if x not in self.visited]
            if avail:
                r = renpy.random.randint(0, sum(x.weight for x in avail))
                s = 0
                for label in avail:
                    s += label.weight
                    if r<s:
                        ret = label
                ret = label # In case the very highest possible value was rolled
                self.visited.append(ret)
                return ret.label
            else:
                return node

        def load_events(self, event_list):
            """
            Here for possible future extension, like loading from external file or something
            """
            if any(type(x) is not MapEvent for x in event_list):
                raise ValueError('Can only take MapEvent objects!')
            self.event_list = event_list

    class Travel(Action):
        def __init__(self, map_point, **kwargs):
            super(Action, self).__init__(**kwargs)
            self.map_point = map_point

        def __call__(self):
            global current_port
            global coords
            global old_coords
            current_port = self.map_point
            old_coords = coords
            coords = current_port.coordinates
            ship = renpy.get_widget('map_screen', 'ship')
            renpy.redraw(ship, 0)
            # renpy.force_full_redraw()
            renpy.hide_screen('map')
            renpy.jump(self.map_point.get_label())

        def get_sensitive(self):
            global current_port
            if self.map_point.check_connected(current_port):
                return True
            else:
                return False

    class Map_point():
        def __init__(self, name, coordinates, label_list = None, connected = [], hotspot_size=50, random_events=True):
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
            self.random_events = random_events
            self.label_list = label_list
            if not label_list is None:
                self.label_prob_sum = sum((x[1] for x in self.label_list))
            self.connected = connected

        def check_connected(self, other_point):
            if other_point in self.connected:
                return True
            else:
                return False

        def list_connected(self):
            return self.connected

        def get_label(self):
            """
            Return a label that the game must jump to upon entering port
            """
            if not self.random_events:
                return self.name
            else:
                #  Checking for random events
                global basic_event_probability
                global event_dispatcher
                if renpy.random.random() <= basic_event_probability:
                    l = event_dispatcher.get_label(self.name)
                else:
                    l = self.name
            return l


    ############################################
    # DATA
    ############################################


    # Map points initialization

    #  Cities
    monet = Map_point('monet', (150, 628), random_events=False)
    tartari = Map_point('tartari', (259, 103), random_events=False)
    plains = Map_point('plains', (584, 109), random_events=False)
    vein = Map_point('vein', (134, 267), random_events=False)
    poop = Map_point('poop', (642, 333), random_events=False)
    office = Map_point('office', (909, 377), random_events=False)
    yankee = Map_point('yankee', (365, 431), random_events=False)
    vortex = Map_point('vortex', (645, 518), random_events=False)
    monastery = Map_point('monastery', (594, 674), random_events=False)

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
    yankee.connected=[node10, node13, node14, node7]
    office.connected=[node11, node15]
    poop.connected=[node10, node11, node14]
    plains.connected=[node18, node19]
    tartari.connected=[node16, node17]
    monet.connected=[node1, node3]
    vein.connected=[node16, node12]
    node18.connected=[plains, node17, node14, node13]
    node20.connected=[node15, node19]
    node19.connected=[plains, node14, node20]
    node17.connected=[tartari, node13, node16, node18]
    node16.connected=[vein, tartari, node17]
    node15.connected=[office, node11, node20]
    node14.connected=[yankee, poop, node10, node13, node18, node19]
    node13.connected=[yankee, node9, node14, node17, node18]
    node12.connected=[vein, node3, node9]
    node11.connected=[poop, office, vortex, node8, node10, node15]
    node10.connected=[yankee, vortex, poop, node7, node10, node11, node14]
    node9.connected=[node3, node12, node13]
    node8.connected=[vortex, node6, node11]
    node7.connected=[node4, node5, node10, vortex, yankee]
    node6.connected=[node5, node8]
    node5.connected=[vortex, monastery, node6, node7]
    node4.connected=[node2, node3, node7]
    node3.connected=[monet, node4, node9, node12]
    node1.connected=[monet, node2]
    node2.connected=[node1, node4]

    # Random events and related stuff
    basic_event_probability = 0.5
    event_list = [MapEvent(label='node_rock_me_mama'),
                  MapEvent(label='node14_lost_in_sea', node_list=['node14']),
                  MapEvent(label='node_event1'),
                  MapEvent(label='node_event2', weight=2),
                  MapEvent(label='node_event3', weight=3)]
    event_dispatcher = EventDispatcher()
    event_dispatcher.load_events(event_list=event_list)
