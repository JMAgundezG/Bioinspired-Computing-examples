import pygame

class Visual:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 800))
        self.background_color = (10, 10, 10)
        self.block_size = 30
        self.fps = 30
        fps_clock = pygame.time.Clock()
        fps_clock.tick(self.fps)

    def color_value(self, val):
        return (255, 255 - val, 255 - val)


    def update_table(self, table, height, width, ants=[]):
        ant_pos = {i.current_pos for i in ants}
        for y in range(width):
            for x in range(height):
                rect = pygame.Rect(x*self.block_size + 3 * x, y*self.block_size + 3 * y, self.block_size, self.block_size)
                pygame.draw.rect(self.window, (0, 255, 0) if (x, y) in ant_pos else self.color_value(table[x][y]), rect)
    
    def update_gui(self):
        pygame.display.update()

