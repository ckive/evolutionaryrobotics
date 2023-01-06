import pybullet as p

class Robot():
    def __init__(self) -> None:
        self.sensors = {}
        self.motors = {}
        self.id = p.loadURDF("body.urdf")
    