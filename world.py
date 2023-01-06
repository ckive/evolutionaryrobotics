
import pybullet as p


class World():
    def __init__(self) -> None:
        planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")