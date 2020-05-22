import copy

#board
bWidth = 100
bHeight = 200

#ships
sDim = 10
sDim_h= sDim / 2
sSpeed = 5
sHealth = 1000
sReload = 20

minWidth = sDim
maxWidth = bWidth - sDim

#bullets
bullWidth = 4
bullHeight = 15
bullSpeed = 8
bullDamage = 300

bullWidth_h = bullWidth / 2
bullHeight_h = bullHeight / 2

class SpaceFighter:
    def __init__(self, state=None, remotePlayers=None):
        self.aiIDs = remotePlayers
        self.flippedAI = self.aiIDs[1]
        self.playerViews = {}

        if state == None:
            self.state = {
                "ships": {
                    self.aiIDs[0]: {
                        "pos": (sDim,sDim),
                        "health": sHealth,
                        "speed": sSpeed,
                        "reload": 0
                    },
                    self.aiIDs[1] : {
                        "pos": (bWidth-sDim, bHeight-sDim),
                        "health": sHealth,
                        "speed": sSpeed,
                        "reload": 0
                    }
                },

                "objects": {},
                "objCnt":0
            }
        else:
            self.state = state

        self.tick()
        print(self.playerViews)

    def getStateForPlayer(self,aiID):
        return self.playerViews[aiID]

    # move:{"move":"left/right","fire":True/False
    def validateMove(self,move,playerID=None):
        if "move" not in move and "fire" not in move:
            return False

        if ("move" in move and not (move["move"] == "left" or move["move"] == "right")):
            return False

        if ("fire" in move and not (move["fire"] == True or move["fire"] == False)):
            return False

        return True

    def makeMove(self, move, playerID=None):
        aiID = playerID
        if "move" in move:
            direction = move["move"]
            if aiID == self.flippedAI:
                direction = "left" if direction == "right" else "right"

            dx = self.state["ships"][aiID]["speed"]
            if direction == "left":
                dx = -dx

            newX = self.state["ships"][aiID]["pos"][0] + dx
            if newX < minWidth:
                newX = minWidth
            if newX > maxWidth:
                newX = maxWidth

            self.state["ships"][aiID]["pos"] = (newX, self.state["ships"][aiID]["pos"][1])

        if "fire" in move and move["fire"] is True and self.state["ships"][aiID]["reload"] == 0:
            posX = self.state["ships"][aiID]["pos"][0]
            posY = self.state["ships"][aiID]["pos"][1] + sDim_h + bullHeight_h + 1
            velY = bullSpeed
            if aiID == self.flippedAI:
                #posX = self.state["ships"][aiID]["pos"][0]
                posY = self.state["ships"][aiID]["pos"][1] - sDim_h - bullHeight_h - 1
                velY = -velY

            self.newObject("bullet", (posX,posY), (0,velY))
            self.state["ships"][aiID]["reload"] = sReload

    def newObject(self, type, pos, velocity):
        objId = "obj_"+str(self.state["objCnt"])
        self.state["objCnt"] += 1

        self.state["objects"][objId] = {
            "type": type,
            "pos": pos,
            "velocity": velocity
        }

    def tick(self):
        #update reloads
        for key, object in self.state["ships"].items():
            self.state["ships"][key]["reload"] = max(object["reload"] - 1, 0)

        #move objects
        for key, object in self.state["objects"].items():
            curPos = self.state["objects"][key]["pos"]
            velocity = self.state["objects"][key]["velocity"]
            self.state["objects"][key]["pos"] = (curPos[0] + velocity[0], curPos[1] + velocity[1])

        #check collisions
        collisions = self.getCollisions()
        for aiID, objID in collisions:
            if self.state["objects"][objID]["type"] == "bullet":
                self.state["ships"][aiID]["health"] -= bullDamage
                del self.state["objects"][objID]

        #check bounds of objects
        deletes = []
        for key, object in self.state["objects"].items():
            if object["type"] == "bullet":
                if object["pos"][1] > bHeight + bullHeight_h or object["pos"][1] < - bullHeight_h:
                    deletes.append(key)

        for key in deletes:
            del self.state["objects"][key]

        #check health
        if self.state["ships"][self.aiIDs[0]]["health"] <= 0:
            self.state["Winner"] = 1
        elif self.state["ships"][self.aiIDs[1]]["health"] <= 0:
            self.state["Winner"] = 0

        #update views
        self.generateViews()
        #print(self.playerViews)

    def getCollisions(self):
        collisions = []
        for key, object in self.state["objects"].items():
            if self.isColliding(self.state["ships"][self.aiIDs[0]]["pos"], object["pos"], object["type"]):
                collisions.append((self.aiIDs[0], key))
            if self.isColliding(self.state["ships"][self.aiIDs[1]]["pos"], object["pos"], object["type"]):
                collisions.append((self.aiIDs[1], key))
        return collisions

    def isColliding(self, shipPos, objPos, objType):
        if objType == "bullet":
            overlapX = True if (abs(shipPos[0] - objPos[0]) < (sDim_h + bullWidth_h)) else False
            overlapY = True if (abs(shipPos[1] - objPos[1]) < (sDim_h + bullHeight_h)) else False
            if overlapX and overlapY:
                return True
            return False

    def generateViews(self):
        #standard view
        self.playerViews[self.aiIDs[0]] = {
            "me": copy.deepcopy(self.state["ships"][self.aiIDs[0]]),
            "enemy": copy.deepcopy(self.state["ships"][self.aiIDs[1]]),
            "objects": copy.deepcopy(self.state["objects"])
        }

        #flipped view
        flippedView = {
            "me": copy.deepcopy(self.state["ships"][self.aiIDs[1]]),
            "enemy": copy.deepcopy(self.state["ships"][self.aiIDs[0]]),
            "objects": copy.deepcopy(self.state["objects"])
        }

        flippedView["me"]["pos"] = self.flipCoords(flippedView["me"]["pos"])
        flippedView["enemy"]["pos"] = self.flipCoords(flippedView["enemy"]["pos"])

        for key, object in flippedView["objects"].items():
            flippedView["objects"][key]["pos"] = self.flipCoords(object["pos"])
            flippedView["objects"][key]["velocity"] = (-object["velocity"][0], -object["velocity"][1])

        self.playerViews[self.aiIDs[1]] = flippedView


    def flipCoords(self, coors):
        return (bWidth - coors[0], bHeight - coors[1])



if __name__ == "__main__":
    game = SpaceFighter(remotePlayers=["alice","bob"])