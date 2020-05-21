#!python      
#published under MIT license
#set $SNK_DIR to anywhere you want it to save scores there

#it was originally named snk
import curses
import time
import random
import threading
from operator import getitem , attrgetter

stdscr = curses.initscr()
brdrwin= curses.newwin(1,1,1,1) 
L,W= stdscr.getmaxyx()
curses.start_color()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
stdscr.keypad(1)
L,W = stdscr.getmaxyx()
L= L-1 # comment this and see what happens (-_Q)
normal,infiltrate,get2goal,runaway=0,1,2,3


def MID(L,D): #move in direction
    R =L.copy()
    if D == 360:
        return R
    if 0<D<180:
        R.y = R.y-1
    elif 180 < D < 360 :
        R.y = R.y+1
    if 90 < D < 270:
        R.x = R.x-1
    elif 270 < D or D< 90:
        R.x = R.x+1
    return R

#point-related stuff
class point(object): #a point ,starting with y because of curses' priority of lines over columns
    def __init__(self,y,x):
        self.y =y
        self.x =x
    def __cmp__(self,other):
        if self.x == other.x and self.y == other.y :
            return 0
        else:
            return -1
    def __str__(self):
        return str((self.y,self.x))
    def __repr__(self):
        return str(self)
    def copy(self):
        return point(self.y,self.x)

def pointgen(L,W): # Generate a random point
    x = point(0,0)
    x.y=random.randint(0+1,L-2)
    x.x=random.randint(0+1,W-2)
    return x

class dummy(object): # holds a text on a point
    def __init__(self,char,location=point(1,1)):
        self.location=location
        self.char=char

    def draw(self,window):
        window.addstr(self.location.y,self.location.x,self.char)

#living animals

class man(object): # the player
    def __init__(self):
        self.score = 0
        self.location=point(1,1)
    def move(self,D):
        X = MID(self.location,D)
        if X.y != 0 and X.x != 0:
            if X.y != L-1 and X.x != W-1:
                self.location = X
    def live(self):
        pass
    def chance(self):
        return chance((500-self.score)/5)
    def draw(self,window):
        window.addstr(self.location.y,self.location.x,'@',curses.A_BOLD)

class rat(object): # pet rats
    def __init__(self):
        self.location = pointgen(L,W)
        self.attached=False
        self.previous_escape=45
        self.phase=normal
    def move(self,D):
	nogo=[]
	for s in snakes:
		nogo+= s.pieces
        X = MID(self.location,D)
        if X.y != 0 and X.x != 0:
            if X.y !=L-1 and X.x != W-1:
		if not X in nogo:
                   self.location = X 
                   return True
        return False

    def draw(self,window):
        window.addstr(self.location.y,self.location.x,'r',curses.A_REVERSE)

    def live(self,snakes):#escapes from snakes, picks up the gold and gives it to player
        rat = self.location
        snk = nearest_snake(snakes,rat).pieces[-1]
        threats = danger_directions(snakes,rat)
        sdistance = distance(rat,snk)
        isPhase = self.isPhase
        self.isAttached()
        escape = False
        if isPhase(infiltrate):
            if not self.goal in threats:
                self.phase = normal
            else:
                escape = True
                d = closest(self.goal)[0]

        if isPhase(runaway):
            if sdistance > 12:
                self.phase = normal

        if sdistance <= 12:
            if isPhase(runaway):
                escape = True
                if sdistance <= 4 :
                    d = opposite(direction(rat,snk))
                elif self.previous_escape not in threats:
                    d = self.previous_escape
                else:
                    d = opposite(direction(rat,snk))
            elif sdistance <= 8:
                escape = True
                if sdistance <= 4 :
                    d = opposite(direction(rat,snk))
                elif isPhase(infiltrate) :
                     d = closest(self.previous_escape)[0]
                else:
                    if self.previous_escape not in threats :
                        d = self.previous_escape
                    else:
                        d = opposite(direction(rat,snk))
                self.phase = runaway

        if isPhase(normal):
            self.phase = get2goal

        if self.phase == get2goal and self.goal() == direction(rat,snk):
            self.phase = infiltrate
            escape = True
            d = closest(self.goal())[0]

        if self.phase == get2goal:
            d = self.goal()
        if self.goal() == 360:
            self.attached = True

        if not self.move(d) :
            if isPhase(get2goal) and distance(rat,coin.location)== 1:
                self.attached = True
            s = closest(d)
            for n in s:
                d = n
                if self.move(d):
                    break
        if self.attached:
            coin.location = MID(self.location,d)
        if escape :
              self.previous_escape = d
    def isAttached(self):#is coin attached
        if distance(self.location,coin.location) > 1:
            self.attached = False
    def isPhase(self,phase):#what is the phase, for example passing through snakes or reaching the coin
        if self.phase == phase:
            return True
        else:
            return False
    def goal(self):# what is rat's goal to reach? i.e coin,man
        if self.attached:
            return direction(self.location,dude.location)
        else:
            return direction(self.location,coin.location)
    def chance(self):
        return chance((300-dude.score)/3)
        
class snake(object): # enemies
    def __init__(self):
        self.lenght=random.randint(3,7)
        self.pieces=[point(1,1)]
    def move(self,D):
        X=MID(self.pieces[-1],D)
        if X.y != 0 and X.x != 0:
            if X.y!= L-1 and X.x !=W-1:
		if X!=coin.location and X!=gate.location:
      	           self.pieces.append(X)
	           if len(self.pieces) > self.lenght:
	                   del(self.pieces[0])
	           return True
    def draw(self,window):
        for p in self.pieces:
            window.addstr(p.y,p.x,'s')
        p = self.pieces[-1]
        window.addstr(p.y,p.x,'S')
    def live(self,dude): #hunger is based on the amount of gold the player has collected, if the leading snake is too near to the player others will let it eat alone.
        global snakes,rats
        m = dude.location

        snk = self.pieces[-1]

        l = snakes[0]
        ldng = l.pieces[-1]
        h = distance(ldng,m)
        k = distance(snk,ldng)

        
        if self !=l and h < 5 and k < 14 :
                d = opposite(direction(snk,ldng))

        elif dude.chance():
                d= random.randint(0,8)*45
        else:
             d= direction(snk,m)

        if not self.move(d) :
            for n in closest(d):
                if self.move(n):
                    break

        if  m in self.pieces:
            snakeeaten(m,stdscr)
            if type(dude)==rat:
                del(rats[rats.index(dude)])
                return False
            else:
                return True
            self.lenght= self.lenght+1

def danger_directions(snakes,target): #directions leading to a snake's mouth
    ret=[]
    for s in snakes:
        ret.append(direction(target,s.pieces[-1]))
    return ret  
def nearest_snake(_snakes,target):
     snakes = _snakes[:]
     a = map(getitem,map(attrgetter('pieces'),snakes),[-1]*len(snakes) ) #makes a list of the snake heads
     b = map(distance,a,[target]*len(snakes)) #makes a list of their distances to the target
     nearest = b.index(sorted(b)[0])
     return snakes[nearest]

def direction(point,target):
    if point.x > target.x:
        if point.y > target.y:
            return 135
        if point.y == target.y:
            return 180
        if point.y < target.y:
            return 225
    if point.x == target.x:
        if point.y > target.y:
            return 90
        if point.y == target.y:
            return 360
        if point.y < target.y:
            return 270
    if point.x < target.x:
        if point.y > target.y:
            return 45
        if point.y == target.y:
            return 0
        if point.y < target.y:
            return 315

def opposite(drctn):
    if drctn == 360:
        return 360
    else :
        return closest(drctn)[-1]

def distance(point,target):
    return int(((point.x-target.x)**2+(point.y-target.y)**2)**0.5)

def closest(drctn): # availible directions sorted by their closeness to given one
    if drctn == 360:
        return [360]
    l = []
    append = l.append
    a,b = drctn,drctn
    x = 1
    while a != b or x:
        if x:
            x=not x
        a = a + 45
        b = b - 45
        if b < 0:
            b = 315
        if  a == 360:
            a= 0
        append(a)
        append(b)
    return l

#animation-related stuff  
def drw_ln(r,D,L,win,m='#'):
       h=L
       c=0
       while c!=r:
           try:
               win.addstr(h.y,h.x,m)
           except:
               pass
           h = MID(h,D)
           c=c+1

def drw_sqr(r,location,window):
    _1=point(location.y-r/2,location.x-r/2)
    drw_ln(r,0,_1,window)
    drw_ln(r,270,_1,window)
    _2=point(location.y+r/2,location.x+r/2)
    drw_ln(r,180,_2,window)
    drw_ln(r,90,_2,window)

def gatelight(location,window):
    c=0
    while c != 6:
        time.sleep(0.05)
        drw_sqr(c,location,window)
        window.refresh()
        c=c+1
    curses.flushinp()

def sparkle(location,window):
    window.addstr(location.y,location.x,'*')
    window.refresh()
    time.sleep(0.2)
    try:
    	window.addstr(location.y-1,location.x-1,'\\|/')
    	window.addstr(location.y,location.x-1,'- -')
    	window.addstr(location.y+1,location.x-1,'/|\\')
    	window.refresh()
    except:
	pass
    curses.flushinp()

def snakeeaten(location,window):#when an snake eats something
    window.addstr(location.y-1,location.x-1,'/-\\')
    window.addstr(location.y,location.x-1,  '.@.')
    try:
     window.addstr(location.y+1,location.x-1,'\\-/')
    except:
        pass
    window.refresh()
    c=0
    while c != 10:
        time.sleep(0.1)
        if c % 2 == 1:
            window.addstr(location.y,location.x,'@')
            window.refresh()
        else:
            window.addstr(location.y,location.x,' ')
            window.refresh()
        c = c+1
    window.addstr(location.y-1,location.x-1, '0_0')
    window.addstr(location.y,location.x-1,  '\\_/')
    try:
       window.addstr(location.y+1,location.x-1,'   ')
    except:
        pass
    window.refresh()
    time.sleep(0.5)
    window.addstr(location.y-1,location.x-1,'-')
    window.refresh()
    time.sleep(0.5)
    window.addstr(location.y-1,location.x-1,'0')
    window.refresh()
    time.sleep(0.5)
    curses.flushinp()

def snakestare(snakes,window):# all snakes stare in disbelief
    locations=[]
    for s in snakes:
        locations.append(s.pieces[-1])
    for l in locations:
        window.addstr(l.y-1,l.x-1,'0_0!!')
        window.addstr(l.y,l.x-1,'\\_/')
        window.refresh()
    time.sleep(1)
    c=0
    while c != 22:
        for l in locations:
            if c%2:
                window.addstr(l.y-1,l.x-1,'0_0  ')
            else:
                window.addstr(l.y-1,l.x-1,'-_-')
        window.refresh()
        time.sleep(0.1)
        c=c+1
    time.sleep(1.5)
    curses.flushinp()

def snakehappy(snakes,target,window):#snakes welcome the new rat
    ls=[]
    for s in snakes:
        ls.append(s.pieces[-1])
    for l in ls:
        window.addstr(l.y-1,l.x-1,'0-0')
        window.addstr(l.y,l.x-1,'\\_/')
    window.refresh()
    time.sleep(0.2)
    for l in ls:
        window.addstr(l.y-1,l.x-1,'^-^')
    window.refresh()
    time.sleep(1)
    curses.flushinp()

def chance(percent):#if 60 is given, it will return True 60% of times
    if percent < 4:
       percent = 4
    x = random.randint(1,100)
    if x <= percent:
        return True
    else:
        return False
#def border():
#    stdscr.border(ord('|'),ord('|'),ord('-'),ord('-'),ord('+'),ord('+'),ord('+'),ord('+'))
def border():
	for y in range(L):
		stdscr.addstr(y,0,'|')
		stdscr.addstr(y,W-1,'|')
	for x in range(W):
		stdscr.addstr(0,x,'-')
		stdscr.addstr(L-1,x,'-')
	stdscr.addstr(L-1,0,'+')
	stdscr.addstr(L-1,W-1,'+')
	stdscr.addstr(0,0,'+')
	stdscr.addstr(0,W-1,'+')
	
def windowsave(window):# prevents program's crashing when minimizing the window or zooming out
    maxx,maxy=stdscr.getmaxyx()
    while(maxx<W or maxy<L):
	maxx,maxy=stdscr.getmaxyx()
    	stdscr.addstr(0,0,'Please resize the window',curses.A_BOLD)
    	stdscr.refresh()
    	time.sleep(0.5)
        
tb = dummy('',point(0,0))
dude = man()
dude.location = pointgen(L,W)
snakes=[snake(),snake(),snake()]
dude.location=pointgen(L,W)
rats = []
reached350=False
firsttimebuyingrat=False
Q=map(ord,('Q','q'))
R=map(ord,('R','r'))
for s in snakes:
        s.pieces[0]=pointgen(L,W)
        while s.pieces[0] == dude.location:
            s.pieces[0]=pointgen(L,W)
coin = dummy('$',pointgen(L,W))
gate = dummy('#',pointgen(L,W))
while gate.location == coin.location:
        gate.location = pointgen(L,W)

def snakefoo(location,lenght,window):#the snakes makes it tongue out
    window.nodelay(1)
    while 1:
	    window.addstr(location.y-1,location.x-1,'0-0')
	    window.addstr(location.y,location.x-1,'\\_/')
	    window.refresh()
	    if window.getch()!=curses.ERR:
		window.nodelay(0)
		curses.ungetch('a')
		return
	    time.sleep(0.5)
	    window.addstr(location.y-1,location.x-1,'>-<')
	    window.addstr(location.y,location.x-1, '\\_/')
	    window.refresh()
	    if window.getch()!=curses.ERR:
	        window.nodelay(0)
		curses.ungetch('a')
	        return
	    time.sleep(0.2)
	    c = 1
	    while c <= lenght:
	        window.addstr(location.y+c,location.x,'^')
	        if c>=2:
	          window.addstr(location.y+c-1,location.x,'|')
                  window.refresh()
   	        c = c+1
       	        if window.getch()!=curses.ERR:
                  window.nodelay(0)
                  curses.ungetch('a')
                  return
                time.sleep(0.2)
	    while 1 <= c:
	        window.addstr(location.y+c,location.x,' ')
       		if c != 1:
              		window.addstr(location.y+c-1,location.x,'^')
	                window.refresh()
	        c = c-1
		if window.getch()!=curses.ERR:
	        	window.nodelay(0)
			curses.ungetch('a')
        		return
	        time.sleep(0.2)
	    window.addstr(location.y-1,location.x-1,'0-0')
	    window.addstr(location.y,location.x-1, '\\_/')
	    window.refresh()
            for i in range(10):
	          if window.getch()!=curses.ERR:
	                window.nodelay(0)
	           	curses.ungetch('a')
	                return
		  time.sleep(0.1)
       
def start_page(window):
    maxy,maxx = window.getmaxyx()
    s =  'B O A S'
    paktc = 'Press any key to continue'
    window.addstr(maxy/2+-2,maxx/2-len(s)/2,s,curses.A_BOLD)
    window.addstr(maxy/2+1,maxx/2-1-len(paktc)/2,paktc)
    snakefoo(point(maxy/2,maxx/2),2,window)
    window.refresh()
    window.getch()
    window.erase()

def TheGame(window):
    global tb,dude,snakes,rats,reached350,coin,gate
    input=0
    while 1:
        if not reached350 and dude.score >= 350:
            reached350 = True
            firsttimebuyingrat=True
            tb.char = '***You may now buy pet rats by pressing R***'
        window.erase()
        there_are_rats= len(rats)>0
        try:
          border()
          for s in snakes:
              s.draw(window)
          if there_are_rats:
            for r in rats:
              r.draw(window)
          dude.draw(window)
          gate.draw(window)
          coin.draw(window)
          tb.draw(window)
          window.refresh()
	  brdrwin.refresh()
        except:
          windowsave(window)
        if len(rats) >= 1:
            rats[-1].live(snakes)
            for r in rats[:-1]:
                r.move(random.randint(0,8)*45)

        input = window.getch() 
        if input == curses.KEY_UP:
            dude.move(90)
        elif input == curses.KEY_DOWN:
            dude.move(270)
        elif input == curses.KEY_LEFT:
            dude.move(180)
        elif input == curses.KEY_RIGHT:
            dude.move(0)
        elif input in Q:
            tb.char='"You chicken!"'
            tb.draw(window)
            window.refresh()
            snakestare(snakes,window)
            return (0,dude.score)
        elif input in R:
          if reached350 and dude.score >= 200:
            dude.score=dude.score-200
            if firsttimebuyingrat :
                        dude.score=0
                        firsttimebuyingrat=False
            tb.char='"REAL food!"'
            tb.draw(window)
            window.refresh()
            rats.append(rat())
            sparkle(rats[-1].location,window)
            window.addstr(rats[-1].location.y,rats[-1].location.x,'r')
            snakehappy(snakes,rats[-1].location,window)

        for s in snakes:
            if len(rats) > 0 :
                h=rats[-1]
            else:
                h=dude
            if s.live(h) == True:
                return (-1,dude.score)

        if dude.location == coin.location:
            dude.score =dude.score+int(3000*(1.0/(W+L)))
            tb.char=str(dude.score)+'$'+(" (R)"*reached350*(dude.score>=200))
            coin.location=pointgen(L,W)
            while(coin.location == gate.location):
                  coin.location=pointgen(L,W)
        if dude.location == gate.location:
            gatelight(gate.location,window)
            snakestare(snakes,window)
            return (1,dude.score)
            break

start_page(stdscr)
x=TheGame(stdscr)
stdscr.erase()
curses.nocbreak(),curses.echo(),curses.endwin(),curses.endwin()

def score_load(_list):
    scores = list()
    players = list()

    for l in _list:
        l = l.replace('\n','')
    for l in _list:
        n = l.split(':')
        players.append(n[0])
        scores.append(int(n[1]))

    return players,scores

def add2scoreboard(score):
    import os 
    player = os.environ['USER']
    if 'SNK_DIR' in os.environ and os.path.exists(os.environ['SNK_DIR']):
        snkdir = os.environ['SNK_DIR']+'/'
    else:
        snkdir = ''
    if not os.path.exists(snkdir+'.snk'):
        try:
           os.mkdir(snkdir+'.snk')
        except:
            snkdir = ''
            if not os.path.exists('.snk'):
                os.mkdir(snkdir+'.snk')
        n = open(snkdir+'.snk/scoreboard','w')
        n.close()
    scoreboard = open(snkdir+'.snk/scoreboard','r')
    players, scores = score_load(scoreboard.readlines())
    n = len(scores)-1
    while n != -1 and score > scores[n] :
        n = n-1
    if n == len(scores)-1:
        if len(scores) > 10:
            return 0
        else:
            scores.append(score)
            players.append(player)
    else:
        scores.insert(n+1,score)
        players.insert(n+1,player)
        while len(scores) > 10:
            del(scores[-1])
            del(players[-1])
    if n == -1 and len(players) >= 4:
        scr = scores[1]
        plr = players[1]
        if plr == player:
            plr = 'yourself'

        print "\n****CONRAGULATIONS!***\n",\
              "     _____ You bet the\n",\
              "   .'     |   previous\n",\
              " .'       |     record\n",\
              " |  .|    |         of\n",\
              " |.' |    |      %4d\n"%scr,\
              "     |    |    held by\n",\
              "  ___|    |___%s\n"%plr,\
              " |            |\n",\
              " |____________|","\n",\
              "**********************\n"

    print "***Top Ten***"
    c = 0
    n = n+1
    while c < len(players) and c < 10:
        if c == n:
            print ">>>",
        print c+1,')',players[c],':',scores[c]
        c = c+1
    file = open(snkdir+'.snk/scoreboard','w')
    c = 0;namnam = list()
    while c != len(players):
        namnam.append(players[c]+':'+str(scores[c])+'\n')
        c = c +1
    file.writelines(namnam)
    file.flush()

if x[0]==-1:
    print ("You\'ve been eaten with %s pieces of gold you found"%x[1])
if x[0]==0:
    print ("You left the game embarrassingly, having only %s pieces of gold"%x[1])
if x[0] == 1:
    print ("You escaped with %s zorkmids"%x[1])
    add2scoreboard(x[1])
