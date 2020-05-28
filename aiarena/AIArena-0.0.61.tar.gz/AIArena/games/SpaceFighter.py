import copy
import random

cnsts = {}

#board
cnsts['boardWidth'] = 100
cnsts['boardHeight'] = 200

#ships
cnsts['shipDim'] = 10
shipDim_h = cnsts['shipDim'] / 2
cnsts['shipVelX'] = 2.5
cnsts['shipVelY'] = 0.02
cnsts['shipHealth'] = 1000
cnsts['shipReload'] = 30


cnsts['minXpos'] = cnsts['shipDim']
cnsts['maxXpos'] = cnsts['boardWidth'] - cnsts['shipDim']

#bullets
cnsts['bulletDim'] = 3
cnsts['bulletSpeed'] = 3
cnsts['bulletDamage'] = 30
cnsts['bulletsTTL'] = 5

bulletDim_h = cnsts['bulletDim'] / 2

#items
cnsts['ticksPerItem'] = 100
cnsts['itemDim'] = 10
itemDim_h = cnsts['itemDim'] / 2
cnsts['itemSpeed'] = 1.5

class SpaceFighter:
    def __init__(self, state=None, remotePlayers=None):
        self.aiIDs = remotePlayers
        self.flippedAI = self.aiIDs[1]
        self.playerViews = {}

        if state == None:
            self.state = {
                "ships": {
                    self.aiIDs[0]: {
                        "pos": [cnsts['shipDim'],cnsts['shipDim']],
                        "health": cnsts['shipHealth'],
                        "velocity": [0, cnsts['shipVelY']],
                        "reload": 0,
                        "target": [cnsts['boardWidth'] / 2 , cnsts['boardHeight'] / 2],
                        "level": 0
                    },
                    self.aiIDs[1] : {
                        "pos": [cnsts['boardWidth']-cnsts['shipDim'], cnsts['boardHeight']-cnsts['shipDim']],
                        "health": cnsts['shipHealth'],
                        "velocity": [0, -cnsts['shipVelY']],
                        "reload": 0,
                        "target": [cnsts['boardWidth'] / 2 , cnsts['boardHeight'] / 2],
                        "level": 0
                    }
                },

                "objects": {},
                "objCnt":0,
                "tickCnt":0
            }
        else:
            self.state = state

        self.tick()
        print(self.playerViews)

    def getStateForPlayer(self,aiID):
        return self.playerViews[aiID]

    # move:{"move":"left/right","fire":True/False
    def validateMove(self,move,playerID=None):
        if "move" not in move and "target" not in move:
            return False

        if ("move" in move and not (move["move"] == "left" or move["move"] == "right")):
            return False

        if ("target" in move and not (type(move["target"]) == list) and not (len(move["target"]) == 2)):
            return False

        return True

    def makeMove(self, move, playerID=None):
        aiID = playerID
        if "move" in move:
            direction = move["move"]
            if aiID == self.flippedAI:
                direction = "left" if direction == "right" else "right"


            dx = cnsts['shipVelX']
            if direction == "left":
                dx = -dx
            self.state["ships"][aiID]["velocity"][0] = dx

            newX = self.state["ships"][aiID]["pos"][0] + dx
            if newX < cnsts['minXpos']:
                newX = cnsts['minXpos']
            if newX > cnsts['maxXpos']:
                newX = cnsts['maxXpos']

            self.state["ships"][aiID]["pos"][0] = newX
        else:
            self.state["ships"][aiID]["velocity"][0] = 0

        if "target" in move:
            target = move["target"]
            if aiID == self.flippedAI:
                target = self.flipCoords(target)

            if aiID != self.flippedAI:
                minY = self.state["ships"][aiID]['pos'][1] + shipDim_h + bulletDim_h + 1
                if target[1] < minY:
                    target[1] = minY
            else:
                maxY = self.state["ships"][aiID]['pos'][1] - shipDim_h - bulletDim_h - 1
                if target[1] > maxY:
                    target[1] = maxY

            self.state["ships"][aiID]["target"] = target


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

    def newItem(self):
        objId = self.newObjectID()

        side = 1 if random.random() < 0.5 else -1
        posX = 50 + (side * (50 + (random.random() * 50)))
        posY = (random.random() * 100) + 50
        velX = random.random() * cnsts['itemSpeed'] * -side
        velY = (random.random() - 0.5) *cnsts['itemSpeed']

        self.state["objects"][objId] = {
            "type": "item",
            "pos": [posX,posY],
            "velocity": [velX,velY],
        }

    def tick(self):
        self.state["tickCnt"] += 1

        #update reloads and autofire and move closer
        for key, object in self.state["ships"].items():
            self.state["ships"][key]["reload"] = object["reload"] - 1
            if object["reload"] <= 1:
                posX = self.state["ships"][key]["pos"][0]
                posY = self.state["ships"][key]["pos"][1] + shipDim_h + bulletDim_h + 1

                if key == self.flippedAI:
                    posY = self.state["ships"][key]["pos"][1] - shipDim_h - bulletDim_h - 1


                velX = object['target'][0] - posX  # dx
                velY = object['target'][1] - posY  # dy
                uVec = self.toUnitVector([velX, velY])
                velX = uVec[0] * cnsts['bulletSpeed']  # unit vector then speed
                velY = uVec[1] * cnsts['bulletSpeed']  # unit vector then speed

                color = "red" if key == self.flippedAI else "blue"
                self.newBullet([posX, posY], [velX, velY], color)

                newReload = max(5, cnsts['shipReload'] - (2 * self.state["ships"][key]['level']))
                self.state["ships"][key]["reload"] = newReload

            self.state["ships"][key]['pos'][1] = object['pos'][1] + object['velocity'][1]


        #update objects
        deletes = []
        for key, object in self.state["objects"].items():
            if object["type"] == "bullet" or object["type"] == "item":
                curPos = self.state["objects"][key]["pos"]
                velocity = self.state["objects"][key]["velocity"]
                self.state["objects"][key]["pos"] = [curPos[0] + velocity[0], curPos[1] + velocity[1]]
            elif object["type"] == "explosion":
                if object["ttl"] <= 0:
                    deletes.append(key)
                self.state["objects"][key]["ttl"] = object["ttl"] - 1


        #check collisions
        #ships
        collisions = self.getShipCollisions()
        for aiID, objID in collisions:
            if self.state["objects"][objID]["type"] == "bullet":
                self.state["ships"][aiID]["health"] -= cnsts['bulletDamage']
                deletes.append(objID)
                self.newExplosion(self.state["ships"][aiID]['pos'])

        #objects
        collisions = self.getObjectCollisions()
        for objAID, objBID in collisions:
            if self.state["objects"][objAID]["type"] == "bullet" and self.state["objects"][objBID]["type"] == "bullet":
                self.newExplosion(self.state["objects"][objAID]["pos"])
                deletes.append(objAID)
                deletes.append(objBID)
            elif self.state["objects"][objAID]["type"] == "item" or self.state["objects"][objBID]["type"] == "item":
                itemID = objAID
                bullID = objBID
                if self.state["objects"][objBID]["type"] == "item":
                    itemID = objBID
                    bullID = objAID

                shipID = self.aiIDs[0]
                if self.state["objects"][bullID]["color"] == "red":
                    shipID = self.aiIDs[1]
                self.state['ships'][shipID]['level'] += 1

                self.newExplosion(self.state["objects"][objAID]["pos"])
                deletes.append(objAID)
                deletes.append(objBID)





        #check bounds of objects
        for key, object in self.state["objects"].items():
            if object["type"] == "bullet":
                if object["pos"][1] > cnsts['boardHeight'] or object["pos"][1] < 0:
                    deletes.append(key)
                if object["pos"][0] > cnsts['boardWidth'] or object["pos"][0] < 0:
                    curVel = self.state["objects"][key]["velocity"]
                    self.state["objects"][key]["velocity"][0] = -curVel[0]

                    curTTL = self.state["objects"][key]["ttl"]
                    curTTL -= 1
                    self.state["objects"][key]["ttl"] = curTTL
                    if curTTL <= 0:
                        deletes.append(key)
            elif object["type"] == "item":
                curVel = self.state["objects"][key]["velocity"]

                if object["pos"][0] < 0:
                    self.state["objects"][key]["velocity"][0] = abs(curVel[0])
                if object["pos"][0] > cnsts['boardWidth']:
                    self.state["objects"][key]["velocity"][0] = -abs(curVel[0])

                if object["pos"][1] < 0:
                    self.state["objects"][key]["velocity"][1] = abs(curVel[1])
                if object["pos"][1] > cnsts['boardHeight']:
                    self.state["objects"][key]["velocity"][1] = -abs(curVel[1])

        deletes = list(set([i for i in deletes]))
        for key in deletes:
            del self.state["objects"][key]

        #check health
        if self.state["ships"][self.aiIDs[0]]["health"] <= 0:
            self.state["Winner"] = 1
        elif self.state["ships"][self.aiIDs[1]]["health"] <= 0:
            self.state["Winner"] = 0


        #item creation
        if self.state["tickCnt"] % cnsts['ticksPerItem'] == 0:
            self.newItem()

        #update views
        self.generateViews()
        #print(self.playerViews)

    def getShipCollisions(self):
        collisions = []
        for key, object in self.state["objects"].items():
            if object["type"] == "bullet":
                if self.isColliding(self.state["ships"][self.aiIDs[0]]["pos"], "ship", object["pos"], object["type"]):
                    collisions.append((self.aiIDs[0], key))
                if self.isColliding(self.state["ships"][self.aiIDs[1]]["pos"], "ship", object["pos"], object["type"]):
                    collisions.append((self.aiIDs[1], key))
        return collisions

    def getObjectCollisions(self):
        collisions = []
        for key, object in self.state["objects"].items():
            if object["type"] == "bullet":
                for keyB, objectB in self.state["objects"].items():
                    if key == keyB:
                        continue
                    if objectB["type"] == "bullet" or objectB["type"] == "item":
                        if self.isColliding(object["pos"], object["type"], objectB["pos"], objectB["type"]):
                            if key < keyB:
                                collisions.append((key, keyB))
                            else:
                                collisions.append((keyB, key))

        #remove duplicates
        return list(set([i for i in collisions]))

    def isColliding(self, aPos, aType, bPos, bType):
        aDim_h = self.typeToDimH(aType)
        bDim_h = self.typeToDimH(bType)

        if aType == "bullet" and bType == "bullet":
            return self.isColliding_Circle_Circle(aPos, aDim_h, bPos, bDim_h)

        elif aType == "ship" or bType == "ship":
            shipPos = aPos
            bullPos = bPos
            if bType == "ship":
                shipPos = bPos
                bullPos = aPos

            return self.isColliding_Circle_Box(bullPos, bulletDim_h, shipPos, shipDim_h)

        elif aType == "item" or bType == "item":
            itemPos = aPos
            bullPos = bPos
            if bType == "item":
                itemPos = bPos
                bullPos = aPos

            return self.isColliding_Circle_Circle(bullPos, bulletDim_h, itemPos, itemDim_h)

    def isColliding_Circle_Circle(self, aPos, aDim_h, bPos, bDim_h):
        dx = aPos[0] - bPos[0]
        dy = aPos[1] - bPos[1]
        distance = (dx ** 2 + dy ** 2) ** (1 / 2)
        if distance < aDim_h + bDim_h:
            return True
        return False

    def isColliding_Box_Box(self, aPos, aDim_h, bPos, bDim_h):
        overlapX = True if (abs(aPos[0] - bPos[0]) < (aDim_h + bDim_h)) else False
        overlapY = True if (abs(aPos[1] - bPos[1]) < (aDim_h + bDim_h)) else False
        if overlapX and overlapY:
            return True
        return False

    def isColliding_Circle_Box(self, cPos, cDim_h, bPos, bDim_h):
        dx = abs(cPos[0] - bPos[0])
        dy = abs(cPos[1] - bPos[1])

        if dx > (cDim_h + bDim_h) or dy > (cDim_h + bDim_h): #centers too far
            return False

        if dx <= (cDim_h + bDim_h) or dy <= (cDim_h + bDim_h):#centers must be close enough
            return True

        cornerDist = (dx**2 + dy**2)**(1/2) #last edge case of corners overlapping
        if cornerDist < cDim_h + bDim_h:
            return True

        return False


    def typeToDimH(self, type):
        if type == "bullet":
            return bulletDim_h
        elif type == "ship":
            return shipDim_h

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
                flippedView["objects"][key]["velocity"] = [-object["velocity"][0], -object["velocity"][1]]
                flippedView["objects"][key]["color"] =  "red" if object["color"] == "blue" else "blue"

        self.playerViews[self.aiIDs[1]] = flippedView


    def flipCoords(self, coors):
        return [cnsts['boardWidth'] - coors[0], cnsts['boardHeight'] - coors[1]]

    def toUnitVector(self, vec):
        magnitude = (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)
        return [vec[0] / magnitude, vec[1] / magnitude]


if __name__ == "__main__":
    game = SpaceFighter(remotePlayers=["alice","bob"])
