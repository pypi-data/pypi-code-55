import socket

from . import Engine


class TurnEngine(Engine):
    """
    TurnEngine is a simple engine for turn-based games like chess.
    """

    turn_timeout = 1  # default timeout is 1 second
    turns = 100  # default turns is 100

    def step(self, robot):
        """
        step must be a generator that yields the data to send to the robot.

        Example::
            def step(self, robot):
                data = get_data() #  does something to get the data
                response = yield data #  response is the robot response
                handle_response(response)
        """
        raise NotImplementedError()

    def end(self):
        """
        When the game is done this method is called for finishing the game.
         Calculating the scores, penalties and etc. Return the game status.
        """
        raise NotImplementedError()

    def run(self):
        """
        Runs the engine.
        """
        super().run()
        for robot in self.robots:
            robot.sock.settimeout(self.turn_timeout)

        for i in range(1, self.turns + 1):
            for robot in self.robots:
                step = self.step(robot)
                data = step.send(None)
                self.log({"from": "ENGINE", "to": robot.id, "step": i, "msg": data})
                robot.sock.send(data.encode())
                try:
                    response = robot.sock.recv(1048576).decode()  # 1 KiB
                    self.log(
                        {"from": robot.id, "to": "ENGINE", "step": i, "msg": response}
                    )
                    step.send(response)
                except socket.timeout:
                    robot.sock.send(b"TIMEOUT")
                    self.send(
                        {"from": "ENGINE", "to": robot.id, step: i, "msg": "TIMEOUT"}
                    )
                except StopIteration:
                    pass

        self.send({"from": "ENGINE", "to": "Ares", "step": -1, "msg": self.end()})
