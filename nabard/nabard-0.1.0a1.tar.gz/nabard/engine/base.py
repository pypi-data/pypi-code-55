import multiprocessing as mp
import socket

from . import Robot


class Engine:
    """
    Engine is the base class of a game engine that creates the robots processes
     and starts them on running the engine.
    """

    def __init__(self, *args):
        self.robots = []
        for item in args:
            robot = Robot(item.id)
            robot.sock, item.sock = socket.socketpair()
            robot.process = mp.Process(target=item.run)
            robot.process.daemon = True
            self.robots.append(robot)

    def run(self):
        """
        Runs the engine and also starts the robots processes.
        """
        for robot in self.robots:
            robot.process.start()
