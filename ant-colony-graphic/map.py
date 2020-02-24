import numpy as np
from ant import Ant, PHEROMONE_VALUE

class Map:
    def __init__(self, dim_x, dim_y, initial_pos, final_pos, n_population):
        self.dims = (dim_x, dim_y)
        self.map_hormones = np.zeros(self.dims, dtype=float)
        self.map_hormones += 1
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        self.population = [Ant(i, initial_pos) for i in range(n_population)]
        self.n_population = n_population
        self.ant_id = n_population
        self.global_turn = 1
    def turn(self):
        for i in self.population: 
            i.move(self.map_hormones)
        self.win_ants()
        self.kill_ants()
        while len(self.population) < self.n_population:
            self.population.append(Ant(self.ant_id, self.initial_pos))
            self.ant_id += 1
        if self.global_turn % 20 == 0:
            self.map_hormones *= 0.9
        self.global_turn += 1

    def kill_ants(self):
        self.population = list(filter(lambda x: x.turn < 80, self.population))
    def win_ants(self):
        winning = [x.path for x in self.population if x.current_pos == self.final_pos]
        self.population = list(filter(lambda x: x.current_pos != self.final_pos, self.population))
        for i in winning: self.spread_pheromones(i)

    def spread_pheromones(self, positions):
        for x,y in positions:
            self.map_hormones[x][y] += 20 * PHEROMONE_VALUE
        
    
    def color_value(self, val):
        return (255, max(255 - val, 0), max(0, 255 - val))

    def printable_table(self):
        printable_table = [[(0,0,0) for i in range(self.dims[0])] for i in range(self.dims[1])]
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                printable_table[i][j] = self.color_value(self.map_hormones[i][j])
        for i in self.population:
            printable_table[i.current_pos[0]][i.current_pos[1]] = (0, 255, 0)
        printable_table[self.initial_pos[0]][self.initial_pos[1]] = printable_table[self.final_pos[0]][self.final_pos[1]] = (0, 255, 255)
        return printable_table

