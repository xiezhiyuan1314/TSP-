import math

import pygame
from pygame.color import THECOLORS
from pygame.sprite import Group

from GAYX1 import Rocket, Population


def gayx_main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('宋体', 20)
    timefactor = 0.1
    population = Population()
    counter = 0
    target_pos = (300, 50)

    while True:
        clock.tick(60)
        fps = font.render('fps: {:.0f}'.format(clock.get_fps()), 1, THECOLORS['white'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

        screen.fill(THECOLORS['black'])
        pygame.draw.circle(screen, THECOLORS['red'], target_pos, 16)

        blocks = [pygame.draw.rect(screen, THECOLORS['yellow'], (100, 250, 400, 20)),
                  pygame.draw.rect(screen, THECOLORS['yellow'], (100, 150, 20, 100)),
                  pygame.draw.rect(screen, THECOLORS['yellow'], (480, 150, 20, 100)),
                  pygame.draw.rect(screen, THECOLORS['yellow'], (480, 270, 20, 120)),
                  pygame.draw.rect(screen, THECOLORS['yellow'], (0, 400, 100, 20))]

        for i in range(int(1 / timefactor)):
            population.update(counter, target_pos, blocks, timefactor)

        population.draw(screen)

        screen.blit(fps, (0, 0))

        pygame.display.update()
        counter += 1

        alives = 0
        for rocket in population:
            alives += 1 if rocket.is_alive(target_pos, blocks) else 0
        if counter >= 400 or alives == 0:
            population.evaluate(target_pos, blocks)

            population = Population(population.selection())
            print('next_gen', counter)

            counter = 0
