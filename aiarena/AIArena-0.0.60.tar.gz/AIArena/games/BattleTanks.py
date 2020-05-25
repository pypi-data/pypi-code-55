# BattleTanks.py -- Implements a multiplayer arena style deathmatch between AI agents.
# General operation:
# Arena.py works on a simple 50x50 grid where each player may take up one space.
# On each "turn", an agent may opt to do one of the following:
#  1. Move one space in any direction
#  2. Pick up an object present on the space
#  3. "Fire" on a given space with coordinates (depending on the object/weapon equipped)
# Each space is represented as a tuple with the following attrributes:
# (player, item)
# player is either None or the name of the AI on that space.
# item is either None or an int referring to one of the following item codes:
# 0 - health pickup (+10 health)
# 1 - AoE pickup (increases the radius of attacks by one tile)
# TODO: add more of these
# 
# On each turn, the agent will be passed the following game state information:
# {"health": player health as an integer,
#  "board": game board information,
#  "position": the player's position (tuple; row, column)
#  "inventory": list of items picked up
#  "range": The player's firing range (max euclidean distance to a given tile)
#  "aoe": The radius (in tiles) of splash damage on the player's shots
#  "lastmove": bool representing whether the last move was valid
#  "score": Integer representing the player's current score.
# }

import random
import math
import copy
import uuid

WIDTH=25*32
HEIGHT=25*32
HEALTH=100
ITEMS=[{"aoe": 2, "range": -1, "health": 0}, # Area of Effect pickup
       {"aoe": 0, "range": 3, "health": 0}, # Range pickup
       {"aoe": 0, "range": 0, "health": 25}, # Health pickup
       {"aoe": random.randint(-1, 2), "range": random.randint(-5, 5), "health": random.randint(-10, 30)} # Random bonus pickup.
       ]

PROJECTILESPLASH=32
PROJECTILEDAMAGE=30
PROJECTILESCLFAC=1
BOMBSPLASH=128
BOMBDAMAGE=20
BOMBSCLFAC=0.5
MOVESPEED=5
PROJMOVESPEED=10


# Utility functions:

def euDist(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

class BTObject:
    def __init__(self, id, pos, vel, health, type, inventory, width, height, timer=-1):
        self.id=id
        self.pos=pos
        self.vel=vel
        self.health=health
        self.inventory=inventory
        self.type=type
        self.width=width
        self.height=height
        self.timer=timer
        
    def getBoundingBox(self):
        # Top left, top right, bottom left bottom right
        return [(self.pos[0]-self.width/2, self.pos[1]-self.height/2), (self.pos[0]+self.width/2, self.pos[1]-self.height/2), (self.pos[0]-self.width/2, self.pos[1]+self.height/2), (self.pos[0]+self.width/2, self.pos[1]+self.height/2)]
        
    def detectHit(self, other):
        ourbb=self.getBoundingBox()
        thrbb=other.getBoundingBox()
        hit=False
        for pt in thrbb:
            hit=hit or (pt[0]>=ourbb[0][0] and pt[0]<=ourbb[3][0] and pt[1]>=ourbb[0][1] and pt[1]<=ourbb[3][1])
        
        return hit
        
    # Returns a set of objects struck + their associated damages if our type is correct
    def splash(self, otherObjects, basedmg, scalefactor, radius):
        objs=[]
        for o in otherObjects:
            if o.type!="explosion":
                # Don't perform splash for explosions (ie. graphics)
                dist=euDist(self.pos, o.pos)
                if dist<radius:
                    #objs.append((o.id, playerDamage[player]=int(basedmg/((dist+1)*scalefactor))))
                    #Tristans attempt at fixing:
                    objs.append((o.id, int(basedmg / ((dist+1) * scalefactor))))
        return objs
    
    def move(self):
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        
        # This might prove to be an interesting intentional quirk: have rigid collisions with the board bounds:
        if self.pos[0]>WIDTH:
            self.vel[0]*=-1
            self.pos[0]=WIDTH
            print("BOUNCE")
        elif self.pos[0]<0:
            print("BOUNCENEG")
            self.vel[0]*=-1
            self.pos[0]=0
        
        if self.pos[1]>HEIGHT:
            print("BOUNCEY")
            self.vel[1]*=-1
            self.pos[1]=HEIGHT
        elif self.pos[1]<0:
            print("BOUNCEYNEG")
            self.vel[1]*=-1
            self.pos[1]=0
        
    
    def tick(self):
        if self.timer!=-1:
            self.timer-=1
            
    # returns true on death:
    def applyDamage(self, dmg):
        self.health-=dmg
        return self.health<0
    
    def getDict(self):
        d={}
        d['pos']=self.pos
        d['vel']=self.vel
        d['health']=self.health
        d['inventory']=self.inventory
        d['type']=self.type
        d['dims']=[self.width, self.height]
        d['timer']=self.timer
        
        return d

class BattleTanks:
    def __init__(self, state=None, remotePlayers=None):
        self.ais=remotePlayers
        self.items=[]
        self.projectiles=[]
        self.timedProjectiles=[]
        self.deathList=[]
        # Represents sprites in the JS engine:
        self.graphics=[]
        self.dims=(WIDTH, HEIGHT)
        self.objectSet={}
        self.tickct=0
        # This is only kept for compatibility with the new ref.
        self.state={}
        
        # Populate the world with players
        for ai in self.ais:
            pos=[random.randint(0, self.dims[0]-1), random.randint(0, self.dims[1]-1)]
            self.objectSet[ai]=BTObject(ai, pos, [0, 0], 100, "player", {}, 32, 32)
        
        # Populate the world with an initial item set (more will be added at random based on tick):
        for i in range(4):
            itemID=str(uuid.uuid4())
            pos=[random.randint(0, self.dims[0]-1), random.randint(0, self.dims[1]-1)]
            self.items.append(itemID)
            self.objectSet[itemID]=BTObject(itemID, pos, [0, 0], 1, "item", [ITEMS[i]], 32, 32)
            
            
    def getStateForPlayer(self, player):
        ps={}
        # This state is going to be large and slow (for now)
        ps['id']=player
        ps['boarddims']=[WIDTH, HEIGHT]
        ps['players']={p: self.objectSet[p].getDict() for p in self.ais}
        ps['items']={p: self.objectSet[p].getDict() for p in self.items}
        ps['projectiles']={p: self.objectSet[p].getDict() for p in self.projectiles}
        ps['timedprojectiles']={p: self.objectSet[p].getDict() for p in self.timedProjectiles}
        ps['graphics']={p: self.objectSet[p].getDict() for p in self.graphics}
        return ps
    
    def doPickup(self, aiid, itid, aiobj, itobj):
        # Add item attributes to player:
        for it in itobj.inventory:
            # Right now, we're only going to consider health:
            health=it['health']
            self.objectSet[aiid].health+=health
        # Item object cleanup is performed externally.ooo
    
    # Allow player input:
    def makeMove(self, move, playerID=None):
        if playerID is None:
            return
        
        ai=playerID
        
        if ai in self.deathList:
            # Don't allow dead AIs to submit moves.
            return
        
        # Move and stopmoving are mutually exclusive:
        if "move" in move:
            angle=move['move']
            xdir=math.cos(angle)
            ydir=math.sin(angle)
            
            # scale the vector to the correct velocity:
            dst=euDist((xdir, ydir), (0, 0))
            sf=MOVESPEED/dst
            xdir*=sf
            ydir*=sf
            print("\tSETTING VELOCITY TO ", [xdir, ydir])
            self.objectSet[ai].vel=[xdir, ydir]
            
        elif "stopmoving" in move:
            # Zero out velocity:
            self.objectSet[ai].vel=[0, 0]
        
        # fire and place (planting a bomb) are mutually exclusive)
        if "fire" in move:
            itemID=str(uuid.uuid4())
            pos=self.objectSet[ai].pos
            
            angle=move['fire']
            xdir=math.cos(angle)
            ydir=math.sin(angle)
            
            # scale the vector to the correct velocity:
            dst=euDist((xdir, ydir), [0, 0])
            sf=PROJMOVESPEED/dst
            xdir*=sf
            ydir*=sf
            self.projectiles.append(itemID)
            self.objectSet[itemID]=BTObject(itemID, pos, [xdir, ydir], 1, "projectile", [], 32, 32)
        
        elif "place" in move:
            # todo: implement this
            pass
        
    def validateMove(self, move, playerID=None):
        ## This is a stub at the moment:
        return True
        
        
    def tick(self):
        self.tickct+=1
        
        if len(self.ais)==0 and len(self.deathList)!=0:
            # The winner is the last AI to die:
            print("\tCALLING MATCH WITH DEATHLIST: ", self.deathList)
            self.state['Winner']=self.deathList[-1]
            return
        
        elif len(self.ais)==0:
            print("\tCALLING MATCH WITH EMPTY DEATHLIST: ", self.deathList)
            self.state['Winner']=None
            return
        
        rawobjlist=[]
        
        # Perform object movement updates:
        for o in self.objectSet:
            self.objectSet[o].move()
            self.objectSet[o].tick()
            
        # Determine if any graphics have expired:
        graphicremlist=[]
        for g in self.graphics:
            gobj=self.objectSet[g]
            if gobj.timer==0:
                graphicremlist.append(g)
        
        # Remove all expired graphics prior to computing explosions, projectiles, etc:
        graphicremlist=list(set(graphicremlist))
        for g in graphicremlist:
            del self.graphics[self.graphics.index(g)]
            del self.objectSet[g]
            
        rawobjlist=[self.objectSet[o] for o in self.objectSet]
        
        # Determine if any timed projectiles should go off:
        objremlist=[]
        for t in self.timedProjectiles:
            tobj=self.objectSet[t]
            if tobj.timer==0:
                objremlist.append(t)
                splashlist=tobj.splash(rawobjlist, BOMBDAMAGE, BOMBSCLFAC, BOMBSPLASH)
                
                for s in splashlist:
                    # We're already removing the current object.
                    sobj=s[0]
                    sdmg=s[1]
                    if self.objectSet[sobj].applyDamage(sdmg):
                        objremlist.append(sobj)
                
                
                
        # Perform collision detection:
        for ai in self.ais:
            aiobj=self.objectSet[ai]
            
            # Perform item collision detection and pickups
            for i in self.items:
                it=self.objectSet[i]
                if aiobj.detectHit(it):
                    self.doPickup(ai, i, aiobj, it)
                    objremlist.append(i)
            
            # Perform projectile collision detection and splash damage:
            for p in self.projectiles:
                pobj=self.objectSet[p]
                
                if aiobj.detectHit(pobj):
                    splashlist=pobj.splash(rawobjlist, PROJECTILEDAMAGE, PROJECTILESCLFAC, PROJECTILESPLASH)
                    for s in splashlist:
                        sobj=s[0]
                        sdmg=s[1]
                        if self.objectSet[sobj].applyDamage(sdmg):
                            objremlist.append(sobj)
        
        # De-duplicate the object removal list:
        objremlist=list(set(objremlist))
        
        for o in objremlist:
            obj=self.objectSet[o]
            
            # Since all graphics have already been culled as appropriate, let's spawn an explosion graphic:
            explID=str(uuid.uuid4())
            pos=obj.pos
            self.graphics.append(explID)
            self.objectSet[explID]=BTObject(explID, pos, [0, 0], 1, "explosion", [], 32, 32, timer=7)
            
            if obj.type=="player":
                if obj.id not in self.deathList:
                    self.deathList.append(obj)
                    del self.ais[self.ais.index(o)]
                    
                    # Then we're the de facto winner:
                    if len(self.ais)==0:
                        self.state['Winner']=obj.id
                        print("\tCALLING MATCH WITH WINNER: ", self.state['Winner'])
                        return
            elif obj.type=="item":
                del self.items[self.items.index(o)]
                del self.objectSet[o]
            elif obj.type=="projectile":
                del self.projectiles[self.projectiles.index(o)]
                del self.objectSet[o]
            elif obj.type=="timedprojectile":
                del self.timedProjectilesp[self.timedProjectiles.index(o)]
                del self.objectSet[o]
            elif obj.type=="explosion":
                pass # Don't allow explosions to get destroyed by collisions.
            else:
                del self.objectSet[o]
                
                    
        
        
