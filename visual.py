import pygame, sys, time, math
import random
import threading
from pygame.locals import *

autoincrement = 0


class MapConfig:
    def __init__(self, n_polygons=40, population=30):
        self.population = population
        self.polygons = [(random.randint(50, 800), random.randint(50, 800), random.randint(10, 100),
                          random.randint(10, 100)) for _ in range(n_polygons)]
        self.goal = [700, 400]


MAP_CONFIG = MapConfig()


class Chromosome:
    def __init__(self, position=None, direction=None):
        global autoincrement
        self.id = autoincrement
        autoincrement += 1
        self.blocked = False
        self.position = [0, 400] if position is None else position
        self.direction = 0 if direction is None else direction
        self.vector = (0, 0)
        self.update_vector()
        self.round = 0
        self.actions = []
        self.rand_actions()
        self.color = (255, 0, 0)

    def distance(self):
        return math.sqrt(pow(abs(self.position[0] - MAP_CONFIG.goal[0]), 2) + pow(abs(self.position[1] - MAP_CONFIG.goal[1]), 2))

    def h(self):
        return self.distance()

    def update_vector(self):
        self.vector = ((math.cos(math.radians(self.direction))),
                       (math.sin(math.radians(self.direction))))

    def rotate(self, degrees):
        self.direction = (self.direction + degrees) % 360

    def rotate_up(self):
        self.rotate(5)
        self.move()

    def rotate_down(self):
        self.rotate(355)
        self.move()

    def move(self):
        if not self.blocked:
            self.update_vector()
            self.position[0] += self.vector[0]
            self.position[1] += self.vector[1]

    def dead(self):
        pass

    def add_move(self):
        self.actions.append(("MOVE", self.move))

    def add_rotate_up(self):
        self.actions.append(("ROTATE_UP", self.rotate_up))

    def add_rotate_down(self):
        self.actions.append(("ROTATE_DOWN", self.rotate_down))

    def add_dead(self):
        self.actions.append(("DEAD", self.dead))

    def action(self):
        action = self.actions[self.round][0]
        print self.id
        print action
        if action == "MOVE":
            self.move()
        elif action == "ROTATE_UP":
            self.rotate_up()
        elif action == "ROTATE_DOWN":
            self.rotate_down()
        self.round += 1
        print "ROUND: ", self.round
        print self.position
        print "--------------"

    def rand_action(self, i):
        random.seed()
        j = random.randint(0, 3)
        if j == 1:
            self.actions[i] = ("ROTATE_UP", self.rotate_up)
        if j == 2:
            self.actions[i] = ("ROTATE_DOWN", self.rotate_down)
        else:
            self.actions[i] = ("MOVE", self.move)

    def rand_actions(self):
        random.seed()
        for _ in range(5000):
            i = random.randint(0, 10)
            if i == 1:
                self.add_rotate_up()
            if i == 2:
                self.add_rotate_down()
            else:
                self.add_move()
        self.actions = random.sample(self.actions, len(self.actions))

    def child_actions(self, mother, father):
        for i in range(5000):
            rand = random.randint(0, 3002)
            if rand < 1500:
                self.actions[i] = father.actions[i]
            elif rand < 3000:
                self.actions[i] = mother.actions[i]
            else:
                self.rand_action(i)

    def finished(self):
        return self.distance() == 0

    def restart(self):
        self.round = 0
        self.blocked = False
        self.position = [0, 400]
        self.direction = 0
        self.update_vector()
        self.color = (0, 255, 0)


class Population:
    def __init__(self, n_population=100):
        self.n_population = n_population
        self.population = [Chromosome([0, 400]) for _ in range(self.n_population)]
        self.eliminated = []
        self.achieved = []
        self.round = 0
        self.generation = 0

    def finished_generation(self):
        return len(self.population) == 0

    def update(self):
        self.round += 1
        #Removes the blocked chromosomes
        self.population = filter(lambda x: not x.blocked, self.population)
        #Finish in the round 3000
        if self.round > 3000:
            self.eliminated.extend(self.population)
            self.population = []
        #blocks chromosomes if there are out of the map or collided with a obstacle
        for i in self.population:
            if i.position[0] < 0 or i.position[0] > 800 or i.position[1] < 0 or i.position[1] > 800:
                i.blocked = True
                self.eliminated.append(i)
            if not i.blocked:
                for j in MAP_CONFIG.polygons:
                    if j[0] < i.position[0] < (j[0] + j[2]):
                        if j[1] < i.position[1] < (j[1] + j[3]):
                            if not i.finished():
                                i.blocked = True
                                self.eliminated.append(i)
                            else:
                                self.achieved.append(i)
            if not i.blocked:
                i.action()

    def create_next_generation(self):
        print "[INFO] CREATING NEW GENERATION"
        previous_generation = self.achieved[:]
        previous_generation.extend(self.eliminated[:])
        previous_generation = sorted(previous_generation, key=lambda x: x.h())
        mother = previous_generation[0]
        father = previous_generation[1]
        mother.restart()
        father.restart()
        self.population = [Chromosome([0, 400]) for _ in range(self.n_population)]
        for i in range(len(self.population), 4):
            t1 = threading.Thread(target=self.population[i].child_actions(mother, father), name="Thread1")
            t2 = threading.Thread(target=self.population[i + 1].child_actions(mother, father), name="Thread2")
            t3 = threading.Thread(target=self.population[i + 2].child_actions(mother, father), name="Thread3")
            t4 = threading.Thread(target=self.population[i + 3].child_actions(mother, father), name="Thread4")
            t1.start()
            t2.start()
            t3.start()
            t4.start()
        #map(lambda x: x.child_actions(mother, father), self.population)
        self.population.append(mother)
        self.population.append(father)
        self.eliminated = []
        self.achieved = []
        self.generation += 1
        self.round = 0
        print "[INFO] NEW GEN CREATED"


class GUI:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption('Genetics algorithms exhibition')
        self.display.fill((255, 255, 255))
        self.pop = Population(MAP_CONFIG.population)
        self.fps = 30
        fps_clock = pygame.time.Clock()
        fps_clock.tick(self.fps)

    def run(self):
        font_obj = pygame.font.Font('freesansbold.ttf', 32)
        while True:  # main game loop
            self.display.fill((255, 255, 255))
            for i in MAP_CONFIG.polygons:
                pygame.draw.rect(self.display, (50, 50, 50), i)
            for i in self.pop.population:
                pygame.draw.circle(self.display, i.color, (int(i.position[0]), int(i.position[1])), 6, 0)
            pygame.draw.circle(self.display, (0 , 255, 0), (MAP_CONFIG.goal[0], MAP_CONFIG.goal[1]), 6, 0)
            round_text_surface_obj = font_obj.render("round:" + str(self.pop.round), True, (255, 255, 255), (0, 0, 0))
            gen_text_surface_obj = font_obj.render("generation:" + str(self.pop.generation), True, (255, 255, 255), (0, 0, 0))
            round_text_rect_obj = round_text_surface_obj.get_rect()
            gen_text_rect_obj = gen_text_surface_obj.get_rect()
            round_text_rect_obj.center = (100, 20)
            gen_text_rect_obj.center = (350, 20)
            self.display.blit(round_text_surface_obj, round_text_rect_obj)
            self.display.blit(gen_text_surface_obj, gen_text_rect_obj)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            if self.pop.finished_generation():
                self.pop.create_next_generation()
            else:
                self.pop.update()



if __name__ == '__main__':
    GUI().run()
