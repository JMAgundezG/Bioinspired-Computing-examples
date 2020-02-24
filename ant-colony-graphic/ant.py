import numpy as np

PHEROMONE_VALUE = 1

class Ant:
    def __init__(self, id, initial_pos):
        self.id = id
        self.current_pos = initial_pos
        self.path = []
        self.turn = 0
    def move (self, table):
        possible_pos = []
        
        if self.current_pos[0] > 1:
            possible_pos.append((self.current_pos[0] - 1, self.current_pos[1]))
        if self.current_pos[0] < table.shape[0] - 1:
            possible_pos.append((self.current_pos[0] + 1, self.current_pos[1]))
        if self.current_pos[1] > 1:
            possible_pos.append((self.current_pos[0], self.current_pos[1] - 1))
        if self.current_pos[1] < table.shape[1] - 1:
            possible_pos.append((self.current_pos[0], self.current_pos[1] + 1))
        possible_pos = list(set(possible_pos) - set(self.path))
        if len(possible_pos) > 0:
            p = np.array([table[x][y] for x, y in possible_pos]) 
            p **= 2
            p /= p.sum()
            self.current_pos = possible_pos[np.random.choice(range(len(possible_pos)), 1, p= p)[0]]
            # print(self.current_pos, self.id)   
            self.path.append(self.current_pos)
            # table[self.current_pos[0]][self.current_pos[1]] += PHEROMONE_VALUE
            self.turn += 1
        else:
            self.turn = 99999

