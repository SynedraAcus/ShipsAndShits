# Everything related to travels

screen map:
    imagemap:
        auto 'images/1024map_%s.png'
        hotspot

init -2 python:
    class Travel(Action):
        def __init__(self, map_point, **kwargs):
            Super(Action, self).__init__(kwargs)
            pass

        def __call__(self, destination):
            pass

        def get_sensitive(self):
            pass

    class Map_point():
        def __init__(self, name):
            pass

        def set_connected(self, other_point):
            pass

        def check_connected(self, other_point):
            pass

        def list_connected(self):
            pass