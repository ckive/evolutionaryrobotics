
import pybullet as p


class World():
    def __init__(self) -> None:
        self.id = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")