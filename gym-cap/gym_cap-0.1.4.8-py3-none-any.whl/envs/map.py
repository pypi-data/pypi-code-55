import os
import sys

import numpy as np
import random
import pickle 

from .const import *

class Map:
    def __init__(self):
        self.map
        self.static_map
        self.agent_locs

    def save(self, fname):
        self_dict = self.__dict__.copy()
        with open(fname, "wb") as pickle_out:
            pickle.dump(self_dict, pickle_out)

    def load(self, fname):
        with open(fname, "rb") as pickle_in:
            self_dict = pickle.load(pickle_in)
            for k in self_dict.keys():
                setattr(self, k, self_dict[k])

    def _connected(self):
        pass

class board_connect:
    def __init__(self, dim): 
        self.dim = dim

    def reset(self, board):
        self.board = board
        self.nodes = np.argwhere(board != 8)
        num_nodes = len(self.nodes)

        self.neighbours = []
        self.add_neighbours(self.nodes[0])

        self.connected = len(self.neighbours) == num_nodes
        
    def add_neighbours(self, node):
        stack = [tuple(node)]

        dx = [0, 0, 1, -1]
        dy = [1,-1, 0,  0]

        while len(stack) > 0:
            x, y = stack.pop(0)
            self.neighbours.append((x,y))
            for delta in zip(dx, dy):
                nx = delta[0] + x
                ny = delta[1] + y
                if nx < 0 or nx >= self.dim or ny < 0 or ny >= self.dim: continue
                if self.board[nx][ny] == 8: continue
                if (nx, ny) in self.neighbours: continue
                if (nx, ny) in stack: continue
                stack.append((nx,ny))


def gen_fair_map(path, num_board, in_seed=None):
    '''
    generates fair boards
    '''
    # init the seed
    if in_seed: np.random.seed(in_seed)

    # constanst
    dim = 40
    density = 0.15

    num_flag = 1
    num_agent = 4
    num_uav = 2
    num_tank = 0

    flag_boarder_distance = 4
    agent_boarder_distance = 3
        
    os.makedirs(path, exist_ok=True)
    bc = board_connect(dim)
    
    j = 0
    while j < num_board:
        # obstacles init
        obs_selector = np.random.randint(0, 2)
        if obs_selector == 0: # Quadrant
            obs_map = np.zeros([dim//2,dim//2], dtype=int)
        elif obs_selector == 1:  # Half-and-half
            obs_map = np.zeros([dim//2,dim], dtype=int)
        mx, my = obs_map.shape
        num_obst = np.random.randint(1, (mx*my*density)//4)
        offset = 1
        for i in range(num_obst):
            cx = np.random.randint(offset,mx-offset)
            cy = np.random.randint(offset,my-offset)
            sx, sy = np.random.randint(1,4,[2])

            x1, y1 = cx-sx, cy-sy
            x2, y2 = cx+sx, cy+sy
            x1 = max(x1,0); y1 = max(y1,0)
            x2 = min(mx, x2); y2 = min(my, y2)
            obs_map[x1:x2, y1:y2] = 1
        if obs_selector == 0: # Quadrant
            obs_map_lr = np.fliplr(obs_map)
            obs_map = np.concatenate([obs_map, obs_map_lr], axis=1)
            obs_map_ud = np.flipud(obs_map)
            obs_map = np.concatenate([obs_map, obs_map_ud], axis=0)
        elif obs_selector == 1:  # Half-and-half
            obs_map_ud = np.flipud(obs_map)
            obs_map = np.concatenate([obs_map, obs_map_ud], axis=0)

        
        # zone init
        selector = np.random.randint(0, 2)
        new_map = np.full([dim, dim], TEAM1_BACKGROUND, dtype=int)
        if selector == 0: # Quadrant
            new_map[dim//2:,:dim//2] = TEAM2_BACKGROUND
            new_map[:dim//2,dim//2:] = TEAM2_BACKGROUND
        elif selector == 1:  # Half-and-half
            new_map[dim//2:,:] = TEAM2_BACKGROUND
        new_map[obs_map==1] = OBSTACLE  # Overlay obstacle

        team1_pool = np.argwhere(new_map==TEAM1_BACKGROUND).tolist()
        
        # define location of flag
        while True:
            fx, fy = random.choice(team1_pool)
            if abs(fx - (dim+1)/2) < flag_boarder_distance: continue
            if selector == 0 and abs(fy - (dim+1)/2) < flag_boarder_distance: continue
                
            new_map[fx, fy] = TEAM1_FLAG
            new_map[dim-fx-1, fy] = TEAM2_FLAG
            break

        team1_pool = np.argwhere(new_map==TEAM1_BACKGROUND).tolist()

        # define location of ground agents
        agent_placed = 0
        while agent_placed < num_agent:
            ax, ay = random.choice(team1_pool)
            if new_map[ax, ay] != TEAM1_BACKGROUND:
                continue
            if abs(ax - (dim+1)/2) < agent_boarder_distance: continue
            if selector == 0 and abs(ay - (dim+1)/2) < agent_boarder_distance: continue
            agent_placed += 1
            new_map[ax, ay] = TEAM1_UGV
            new_map[dim-ax-1, ay] = TEAM2_UGV

            if selector == 0 and obs_selector == 0:
                agent_placed += 1
                new_map[dim-ax-1, dim-ay-1] = TEAM1_UGV
                new_map[ax, dim-ay-1] = TEAM2_UGV

        # define location of air agents
        agent_placed = 0
        while agent_placed < num_uav:
            ax, ay = random.choice(team1_pool)
            if new_map[ax, ay] != TEAM1_BACKGROUND:
                continue
            if abs(ax - (dim+1)/2) < agent_boarder_distance: continue
            if selector == 0 and abs(ay - (dim+1)/2) < agent_boarder_distance: continue
            agent_placed += 1
            new_map[ax, ay] = TEAM1_UAV
            new_map[dim-ax-1, ay] = TEAM2_UAV

            if selector == 0 and obs_selector == 0:
                agent_placed += 1
                new_map[dim-ax-1, dim-ay-1] = TEAM1_UAV
                new_map[ax, dim-ay-1] = TEAM2_UAV

        # define location of tank agents
        agent_placed = 0
        while agent_placed < num_tank:
            ax, ay = random.choice(team1_pool)
            if new_map[ax, ay] != TEAM1_BACKGROUND:
                continue
            if abs(ax - (dim+1)/2) < agent_boarder_distance: continue
            if selector == 0 and abs(ay - (dim+1)/2) < agent_boarder_distance: continue
            agent_placed += 1
            new_map[ax, ay] = TEAM1_UGV2
            new_map[dim-ax-1, ay] = TEAM2_UGV2

            if selector == 0 and obs_selector == 0:
                agent_placed += 1
                new_map[dim-ax-1, dim-ay-1] = TEAM1_UGV2
                new_map[ax, dim-ay-1] = TEAM2_UGV2

        # random rotation and flip
        new_map = np.rot90(new_map, np.random.randint(1,4))
        if 0.5 < np.random.random():
            new_map = np.fliplr(new_map)
        if 0.5 < np.random.random():
            new_map = np.flipud(new_map)

        ## Exclusions:
        # Balance Quadrant
        if selector == 0:
            if np.count_nonzero((new_map[:dim//2, :dim//2]==TEAM1_UGV).flat) == num_agent: continue
            if np.count_nonzero((new_map[:dim//2, dim//2:]==TEAM1_UGV).flat) == num_agent: continue
            if np.count_nonzero((new_map[dim//2:, :dim//2]==TEAM1_UGV).flat) == num_agent: continue
            if np.count_nonzero((new_map[dim//2:, dim//2:]==TEAM1_UGV).flat) == num_agent: continue

        # Tests
        bc.reset(new_map)
        if not bc.connected:
            continue

        density = len(np.argwhere(new_map==8)) / len(new_map.flat)
        if density > 0.4 or density < 0.2:
            continue

        try:
            np.argwhere(new_map==TEAM1_FLAG)[num_flag-1]
            np.argwhere(new_map==TEAM2_FLAG)[num_flag-1]
            np.argwhere(new_map==TEAM1_UGV)[num_agent-1]
            np.argwhere(new_map==TEAM2_UGV)[num_agent-1]
            if num_tank > 0:
                np.argwhere(new_map==TEAM1_UGV2)[num_tank-1]
                np.argwhere(new_map==TEAM2_UGV2)[num_tank-1]
            if num_uav > 0:
                np.argwhere(new_map==TEAM1_UAV)[num_uav-1]
                np.argwhere(new_map==TEAM2_UAV)[num_uav-1]
        except Exception:
            continue
        
        np.savetxt('{}/board_{:04d}.txt'.format(path, (j+1)), new_map, delimiter=' ', fmt='%d')
        j += 1

if __name__=='__main__':
    gen_fair_map(sys.argv[1], 10)
