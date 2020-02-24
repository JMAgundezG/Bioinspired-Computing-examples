from ant import Ant
from map import Map
from visual import Visual


class Controller:
    def __init__(self, dim_x=25, dim_y=25, initial_pos=(3,3), final_pos=(15, 15), n_population=50):
        self.map = Map(dim_x, dim_y, initial_pos, final_pos, n_population)
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