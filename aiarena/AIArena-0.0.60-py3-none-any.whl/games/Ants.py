import random
import copy

class Ants:
    def __init__(self, state=None, AIs=None):
        self.bounds = (10,10)

        self.AIs = AIs
        if state is not None:
            self.state = state
        else:
            self.freshState()


    def freshState(self):
        self.state = {"bots":[]}
        usedPos = []
        for i in range(len(self.AIs)):
            for _ in range(10): #Soldier
                newPos = (random.randint(0,self.bounds[0]-1), random.randint(0,self.bounds[1]-1))
                while newPos in usedPos:
                    newPos = (random.randint(0,self.bounds[0]-1), random.randint(0,self.bounds[1]-1))
                usedPos.append(newPos)
                bot = {
                    "ai":i,
                    "pos":newPos,
                    "health":100,
                    "type":"Soldier"
                }
                self.state["bots"].append(bot)

            for _ in range(2): #Queen
                newPos = (random.randint(0,self.bounds[0]-1), random.randint(0,self.bounds[1]-1))
                while newPos in usedPos:
                    newPos = (random.randint(0,self.bounds[0]-1), random.randint(0,self.bounds[1]-1))
                usedPos.append(newPos)
                bot = {
                    "ai":i,
                    "pos":newPos,
                    "health":100,
                    "type":"Queen",
                    "breedWait":3
                }
                self.state["bots"].append(bot)


    def printBoard(self):
        board = []
        for i in range(self.bounds[0]):
            col = []
            for j in range(self.bounds[1]):
                col.append(0)
            board.append(col)

        for bot in self.state["bots"]:
            board[bot["pos"][0]][bot["pos"][1]] = (bot["type"][0], bot["ai"])

        pStr = "= " * (self.bounds[0] + 2)
        print(pStr)
        for j in range(self.bounds[1]):
            rj = self.bounds[1] - 1 - j
            pStr = "= "
            for i in range(self.bounds[0]):
                if board[i][rj] == 0:
                    pStr += "  "
                else:
                    pStr += self.colorFormat(board[i][rj][1], board[i][rj][0] + " ")
            pStr += "= "
            print(pStr)
        pStr = "= " * (self.bounds[0] + 2)
        print(pStr)

    def colorFormat(self, index, text):
        color=41+index
        return "\033[1;%dm%s\033[0m" % (color, text)

    def runGame(self):
        self.printBoard()
        result = 1
        while result == 1:
            result = self.round()
            self.printBoard()
            x = input("hit enter for next move...")

    def round(self):
        #make moves
        #print(self.state)
        for bot in self.state["bots"]:
            moveState = copy.deepcopy(self.state)
            moveState["bot"] = copy.deepcopy(bot)
            action, position = self.AIs[bot["ai"]].makeMove(moveState)
            #print(action,position)
            target = None
            for tbot in self.state["bots"]:
                if tbot["pos"] == position:
                    target = tbot

            if action == "move" and target == None:
                if position[0] >= 0 and position[0] < self.bounds[0] and position[1] >= 0 and position[1] < self.bounds[1]:
                    if abs(position[0] - bot["pos"][0]) <= 1 and abs(position[1] - bot["pos"][1]) <= 1:
                        bot["pos"] = position

            if action == "attack" and target != None:
                if abs(position[0] - bot["pos"][0]) <= 1 and abs(position[1] - bot["pos"][1]) <= 1:
                    dmg = 34
                    target["health"] = target["health"] - dmg

            if action == "breed" and bot["type"] == "Queen":
                if bot["breedWait"] == 0:
                    newBot = {
                        "ai": bot["ai"],
                        "pos": bot["pos"],
                        "health": 100,
                        "type": "Soldier"
                    }
                    self.state["bots"].append(newBot)
                    bot["breedWait"] = 3
                else:
                    bot["breedWait"] -= 1

        #check for dead to remove
        botsCnt = len(self.state["bots"])
        for i in range(botsCnt):
            if self.state["bots"][botsCnt - 1 - i]["health"] <= 0:
                del self.state["bots"][botsCnt - 1 - i]

        #check if all dead
        if len(self.state["bots"]) == 0:
            return -1

        #check for two different ais
        match = self.state["bots"][0]["ai"]
        for bot in self.state["bots"]:
            if bot["ai"] != match:
                return 1

        #winner
        return 0





class AntsAI:
    def __init__(self, id="antsAI"):
        self.id = id
        self.game = "Ants"

    def makeMove(self,state):
        if state["bot"]["type"] == "Soldier":
            move = self.makeMove_Soldier(state)
        elif state["bot"]["type"] == "Queen":
            move = self.makeMove_Queen(state)
        return move

    def makeMove_Soldier(self,state):
        closest = 99999999
        closestPos = None
        myPos = state["bot"]["pos"]
        for bot in state["bots"]:
            if bot == state["bot"]:#Me
                continue
            if bot["ai"] == state["bot"]["ai"]:#My team
                continue

            dist = ((myPos[0]-bot["pos"][0])**2 + (myPos[1]-bot["pos"][1])**2)**(1/2)
            if dist < closest:
                closest = dist
                closestPos = bot["pos"]

        #print(closest,closestPos)

        if closest < 2:
            return "attack", closestPos

        dx = 0
        if closestPos[0] > myPos[0]:
            dx = 1
        elif closestPos[0] < myPos[0]:
            dx = -1

        dy = 0
        if closestPos[1] > myPos[1]:
            dy = 1
        elif closestPos[1] < myPos[1]:
            dy = -1

        return "move", (myPos[0] + dx, myPos[1] + dy)

    def makeMove_Queen(self, state):
        return "breed", (0,0)


if __name__ == "__main__":
    ai1 = AntsAI(id="ai1")
    ai2 = AntsAI(id="ai2")
    game = Ants(state=None,AIs=[ai1,ai2])
    game.runGame()