
PHEROMONE_VALUE = 10

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
        
        p = np.array([table[x][y] for x, y in possible_pos]) 
        p /= max([table[x][y] for x, y in possible_pos])
        self.current_pos = np.random.choice(possible_pos, 1, p= p))
        table[self.current_pos[0]][self.current_pos[1]] += PHEROMONE_VALUE
        self.turn += 1

