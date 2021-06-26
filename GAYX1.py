import random

import pygame
from pygame.color import THECOLORS
from pygame.sprite import Sprite, Group
from pygame.surface import Surface


def uniform(x, y):
    r = (x ** 2 + y ** 2) ** 0.5
    return x / r, y / r


def dist(posa, posb):
    dx = posa[0] - posb[0]
    dy = posa[1] - posb[1]

    return (dx ** 2 + dy ** 2) ** 0.5


def my_map(origin, low, high, new_low, new_high):
    return origin / (high - low) * (new_high - new_low) + new_low


class DNA():
    def __init__(self, genes=None):
        self.genes = genes if genes is not None else self.create_genes()

    def create_genes(self):
        return [uniform(random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(400)]

    def crossover(self, other):
        mid = random.randint(0, len(self.genes))
        poss = 0.005
        genes = [self.genes[i] if i < mid else other.genes[i] for i in range(len(self.genes))]
        newgenes = [genes[i] if random.random() > poss else uniform(random.uniform(-1, 1), random.uniform(-1, 1))
                    for i in range(len(genes))]

        return DNA(newgenes)


class Rocket(Sprite):
    def __init__(self, dna=None):
        super(Rocket, self).__init__()
        self.pos = [300, 550]
        self.vel = [0, 0]
        self.acc = [0, 0]

        self.dna = dna if dna is not None else DNA()
        self.fitness = 0

        self.image = Surface((8, 8))
        self.image.fill(THECOLORS['white'])
        self.rect = self.image.get_rect()

    def get_force(self, force, timefactor):
        factor = 0.1 * timefactor
        self.acc[0] += force[0] * factor
        self.acc[1] += force[1] * factor

    def is_alive(self, target_pos, blocks):
        return self.rect.left > 0 and self.rect.right < 600 \
               and self.rect.top > 0 and self.rect.bottom < 600 \
               and dist(self.pos, target_pos) > 16 \
               and self.rect.collidelist(blocks) == -1

    def calc_fitness(self, target_pos, blocks):
        self.fitness = my_map(dist(self.rect.center, target_pos), 0, 600, 600, 0)
        if dist(self.pos, target_pos) < 16:
            self.fitness *= 10
        if self.rect.collidelist(blocks) != -1:
            self.fitness /= 10
        # if self.rect.left > 0 and self.rect.right < 600 \
        #        and self.rect.top > 0 and self.rect.bottom < 600:
        #     self.fitness /= 5
        return self.fitness

    def update(self, counter, target_pos, blocks, timefactor):
        self.vel[0] += self.acc[0] * timefactor
        self.vel[1] += self.acc[1] * timefactor

        if self.is_alive(target_pos, blocks):
            self.pos[0] += self.vel[0] * timefactor
            self.pos[1] += self.vel[1] * timefactor

        self.vel[0] *= 1
        self.vel[1] *= 1

        self.get_force(self.dna.genes[counter], timefactor)

        self.rect.center = self.pos


class Population(Group):
    def __init__(self, sprites: list = None):
        self.rockets = sprites if sprites is not None else [Rocket() for i in range(100)]
        super(Population, self).__init__(self.rockets)
        self.mating_pool = []

    def evaluate(self, target_pos, blocks):
        maxfit = 0

        for rocket in self.rockets:
            fit = rocket.calc_fitness(target_pos, blocks)
            maxfit = fit if fit > maxfit else maxfit

        for rocket in self.rockets:
            rocket.fitness /= maxfit

        self.mating_pool = []

        for rocket in self.rockets:
            self.mating_pool.extend([rocket for i in range(int(rocket.fitness * 100))])

    def selection(self):
        new_rockets = []
        for i in range(len(self.rockets)):
            parents = random.choices(self.mating_pool, k=2)
            newdna = parents[0].dna.crossover(parents[1].dna)
            new_rockets.append(Rocket(newdna))

        return new_rockets
