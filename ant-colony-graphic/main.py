from ant import Ant
from map import map
from visual import Visual


class Controller:
    def __init__(self, dim_x=10, dim_y=10, initial_pos=(3,3), final_pos=(10, 10), n_population=30):
        self.map = Map(dim_x, dim_y, initial_pos, final_pos, n_population)
    

v = Visual()
table = [[0 for _ in range(10)] for i in range(10)]
table[1][6] = table[3][3] = 255
v.update_table(table, 10, 10)
v.update_gui()
