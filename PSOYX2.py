import pygame
import os
import numpy as np
import PSOYX4

global centerx, centery, magnification
centerx = 400
centery = 300
magnification = 2

#Create pygameGUI and call environment
def mainPygame(RBFN):
    global centerx, centery, magnification
    carcenter, destination, edge = readFile("map/case01.txt")

    destination = destination*magnification
    destination = PSOYX4.Destination(centerx + destination[0], centery - destination[1], (destination[2] - destination[0]), (destination[3] - destination[1]))

    edge = (1, -1)*edge*magnification + (centerx, centery)
    car = PSOYX4.Car(RBFN, centerx + carcenter[0], centery + carcenter[1], carcenter[2], magnification, edge)
    edge = PSOYX4.Edge(edge)

    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    gameExit = False

    pygame.init()
    gameDisplay = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        pygame.display.update()
        gameDisplay.fill((255, 255, 255))

        if destination.detectCarCollision(car.getCar_X_Y()[0], car.getCar_X_Y()[1]):
            showWinGraphic(gameDisplay)
        else:
            destination.draw(gameDisplay)
            car.draw(gameDisplay)
            edge.draw(gameDisplay)

        clock.tick(30)
    pygame.quit()

def showWinGraphic(gameDisplay):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    textSurface = largeText.render("Win", True, (255, 0, 0))
    textSurface.get_rect().center = ((centerx / 2), (centery / 2))
    gameDisplay.blit(textSurface, textSurface.get_rect())
    pygame.display.update()

#Read wall boundary
def readFile(file):
    try:
        string = ""
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = file
        print(script_dir, rel_path)
        abs_file_path = os.path.join(script_dir, rel_path)
        pfile1 = open(abs_file_path, "r")
        string = pfile1.read()
        string = string.split('\n')
        # string to double list
        string = [i.split(',') for i in string]
        string = [x for x in string if x != ['']]

        carcenter = string[0]
        destination = string[1] + string[2]
        edge = string[3:]
    except Exception as e:
        print(e)

    return np.array(carcenter, dtype=int), \
           np.array(destination, dtype=int), \
           np.array(edge, dtype=int)

