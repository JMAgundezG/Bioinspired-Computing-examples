import numpy as np
from ant import Ant, PHEROMONE_VALUE

class Map:
    def __init__(self, dim_x, dim_y, initial_pos, final_pos, n_population):
        self.dims = (dim_x, dim_y)
        self.map_hormones = np.zeros(self.dims, dtype=float)
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        self.population = [Ant(i) for i in range(n_population)]

    def turn(self):
        for i in self.population: i.move()
        def_win_ants()

    def kill_ants(self):
        self.population = list(filter(self.population, key=lambda x: x.turn < 80))

    def win_ants(self):
        winning = [x.path for x in self.population if x.current_pos == final_pos]
        self.population = list(filter(self.population, key=lambda x: x.current_pos == final_pos))
        for i in winning: self.pread_pheromones(i)

    def spread_pheromones(self, positions):
        for x,y in positions:
            self.map_hormones[x][y] += 2 * PHEROMONE_VALUE
        