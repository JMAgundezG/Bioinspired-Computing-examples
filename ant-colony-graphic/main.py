from ant import Ant
from map import Map
from visual import Visual


class Controller:
    def __init__(self, dim_x=30, dim_y=30, initial_pos=(3,3), final_pos=(25, 25), n_population=100, dead_turn=120):
        self.map = Map(dim_x, dim_y, initial_pos, final_pos, n_population, dead_turn)
        self.v = Visual()
        self.dim_x =dim_x
        self.dim_y = dim_x
    
    def run(self):
        self.map.turn()
        table = self.map.printable_table()
        self.v.update_table(table, self.dim_x, self.dim_y)    
        self.v.update_gui()


c = Controller()
while True:
    c.run()