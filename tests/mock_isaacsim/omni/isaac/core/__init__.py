class World:
    def __init__(self, *args, **kwargs):
        self.scene = Scene()
    def reset(self):
        pass
    def step(self, render=True):
        pass

class Scene:
    def add(self, entity):
        pass
