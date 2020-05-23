import copy

cnsts = {}

#board
cnsts['boardWidth'] = 100
cnsts['boardHeight'] = 200

#ships
cnsts['shipDim'] = 10
shipDim_h = cnsts['shipDim'] / 2
cnsts['shipSpeed'] = 2.5
cnsts['shipHealth'] = 1000
cnsts['shipReload'] = 70

cnsts['minXpos'] = cnsts['shipDim']
cnsts['maxXpos'] = cnsts['boardWidth'] - cnsts['shipDim']

#bullets
cnsts['bulletWidth'] = 4
cnsts['bulletHeight'] = 15
cnsts['bulletSpeed'] = 4
cnsts['bulletDamage'] = 200
cnsts['bulletsTTL'] = 5

bulletWidth_h = cnsts['bulletWidth'] / 2
bulletHeight_h = cnsts['bulletHeight'] / 2

class SpaceFighter:
    def __init__(self, state=None, remotePlayers=None):
        self.aiIDs = remotePlayers
        self.flippedAI = self.aiIDs[1]
        self.playerViews = {}

        if state == None:
            self.state = {
                "ships": {
                    self.aiIDs[0]: {
                        "pos": (cnsts['shipDim'],cnsts['shipDim']),
                        "health": cnsts['shipHealth'],
                        "speed": cnsts['shipSpeed'],
                        "reload": 0
                    },
                    self.aiIDs[1] : {
                        "pos": (cnsts['boardWidth']-cnsts['shipDim'], cnsts['boardHeight']-cnsts['shipDim']),
                        "health": cnsts['shipHealth'],
                        "speed": cnsts['shipSpeed'],
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
            if newX < cnsts['minXpos']:
                newX = cnsts['minXpos']
            if newX > cnsts['maxXpos']:
                newX = cnsts['maxXpos']

            self.state["ships"][aiID]["pos"] = (newX, self.state["ships"][aiID]["pos"][1])

        if "fire" in move and move["fire"] is True and self.state["ships"][aiID]["reload"] == 0:
            posX = self.state["ships"][aiID]["pos"][0]
            posY = self.state["ships"][aiID]["pos"][1] + shipDim_h + bulletHeight_h + 1
            velY = cnsts['bulletSpeed']
            if aiID == self.flippedAI:
                #posX = self.state["ships"][aiID]["pos"][0]
                posY = self.state["ships"][aiID]["pos"][1] - shipDim_h - bulletHeight_h - 1
                velY = -velY

            color = "red" if aiID == self.flippedAI else "blue"
            self.newBullet((posX,posY), (0,velY), color)
            self.state["ships"][aiID]["reload"] = cnsts['shipReload']

    def newObjectID(self):
        objId = "obj_" + str(self.state["objCnt"])
        self.state["objCnt"] += 1
        return objId

    def newBullet(self, pos, velocity, color):
        objId = self.newObjectID()

        self.state["objects"][objId] = {
            "type": "bullet",
            "pos": pos,
            "velocity": velocity,
            "color": color,
            "ttl": cnsts['bulletsTTL']
        }

    def newExplosion(self, pos):
        objId = self.newObjectID()

        self.state["objects"][objId] = {
            "type": "explosion",
            "pos": pos,
            "ttl": 20
        }

    def tick(self):
        #update reloads
        for key, object in self.state["ships"].items():
            self.state["ships"][key]["reload"] = max(object["reload"] - 1, 0)

        #update objects
        deletes = []
        for key, object in self.state["objects"].items():
            if object["type"] == "bullet":
                curPos = self.state["objects"][key]["pos"]
                velocity = self.state["objects"][key]["velocity"]
                self.state["objects"][key]["pos"] = (curPos[0] + velocity[0], curPos[1] + velocity[1])
            elif object["type"] == "explosion":
                if object["ttl"] <= 0:
                    deletes.append(key)
                self.state["objects"][key]["ttl"] = object["ttl"] - 1


        #check collisions
        collisions = self.getCollisions()
        for aiID, objID in collisions:
            if self.state["objects"][objID]["type"] == "bullet":
                self.state["ships"][aiID]["health"] -= cnsts['bulletDamage']
                del self.state["objects"][objID]
                self.newExplosion(self.state["ships"][aiID]['pos'])

        #check bounds of objects

        for key, object in self.state["objects"].items():
            if object["type"] == "bullet":
                if object["pos"][1] > cnsts['boardHeight'] or object["pos"][1] < 0:
                    curVel = self.state["objects"][key]["velocity"]
                    self.state["objects"][key]["velocity"] = (curVel[0], -curVel[1])

                    curTTL = self.state["objects"][key]["ttl"]
                    curTTL -= 1
                    self.state["objects"][key]["ttl"] = curTTL
                    if curTTL <= 0:
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
            overlapX = True if (abs(shipPos[0] - objPos[0]) < (shipDim_h + bulletWidth_h)) else False
            overlapY = True if (abs(shipPos[1] - objPos[1]) < (shipDim_h + bulletHeight_h)) else False
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
            if object["type"] == "bullet":
                flippedView["objects"][key]["velocity"] = (-object["velocity"][0], -object["velocity"][1])
                flippedView["objects"][key]["color"] =  "red" if object["color"] == "blue" else "blue"

        self.playerViews[self.aiIDs[1]] = flippedView


    def flipCoords(self, coors):
        return (cnsts['boardWidth'] - coors[0], cnsts['boardHeight'] - coors[1])



if __name__ == "__main__":
    game = SpaceFighter(remotePlayers=["alice","bob"])