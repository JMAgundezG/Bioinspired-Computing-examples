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


    def update_table(self, table, height, width):
        for y in range(width):
            for x in range(height):
                rect = pygame.Rect(x*self.block_size + 3 * x, y*self.block_size + 3 * y, self.block_size, self.block_size)
                pygame.draw.rect(self.window, table[x][y], rect)
    
    def update_gui(self):
        pygame.display.update()

