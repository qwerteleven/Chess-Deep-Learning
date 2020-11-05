import glob
import os
import random as rn
import time

import cv2
import numpy as np
import pygame


class visor:

    def __init__(self, length, width):
        self.done = 0
        self.table = np.zeros((length, width))
        self.newState = np.zeros((length, width))
        self.state = np.arange(1, 10).reshape(3, 3)
        self.stateFinal = np.arange(1, 10).reshape(3, 3)
        self.length = length
        self.width = width
        self.lengthRange = range(length)
        self.widthRange = range(width)
        self.data = self.loadPuzzle()
        self.chargePuzzle()
        rn.shuffle(self.state.reshape(9))
        self.usedMoves = {}

    def chargePuzzle(self):

        p = np.zeros((0, 10))

        for i in self.state.reshape(9):
            p = np.vstack((p, self.data[i]))

        vsplit = np.vsplit(p, 3)

        q = np.zeros((30, 0))

        for i in vsplit:
            q = np.hstack((q, i))

        self.table = q

    def loadPuzzle(self):
        img_dir = "./numbers"
        data_path = os.path.join(img_dir, '*g')
        files = glob.glob(data_path)
        data = {}

        q = 1

        for f1 in files:
            data[q] = np.transpose(np.array(cv2.imread(f1, cv2.IMREAD_GRAYSCALE)))
            q += 1
        return data

    def distanceManhattan(self):
        d = np.zeros((3, 3))
        tD = 0
        blanck = 0

        for i in range(3):
            for j in range(3):
                d[i][j] = np.abs(i - int((self.state[i][j] - 1) / 3)) + np.abs(j - int((self.state[i][j] - 1) % 3))
                tD += d[i][j]
                if self.state[i][j] == 9:
                    blanck = (i, j)

        return d, tD, blanck

    def nextStep(self, blanck, switch):
        a = self.state[blanck[0]][blanck[1]]
        self.state[blanck[0]][blanck[1]] = self.state[switch[0]][switch[1]]
        self.state[switch[0]][switch[1]] = a

    def switchPiece(self, blanck, dM):
        m = {}

        try:
            m[(blanck[0] + 1, blanck[1])] = (dM[blanck[0] + 1][blanck[1]] +
                                            np.abs(self.state[blanck[0] + 1][blanck[1]] - self.stateFinal[blanck[0] + 1][blanck[1]]))
        except Exception:
            print()
        try:
            if blanck[0] - 1 > -1:
                m[(blanck[0] - 1, blanck[1])] = (dM[blanck[0] - 1][blanck[1]] +
                                            np.abs(self.state[blanck[0] - 1][blanck[1]] - self.stateFinal[blanck[0] - 1][blanck[1]]))
        except Exception:
            print()

        try:
            m[(blanck[0], blanck[1] + 1)] = (dM[blanck[0]][blanck[1] + 1] +
                                            np.abs(self.state[blanck[0]][blanck[1] + 1] - self.stateFinal[blanck[0]][blanck[1] + 1]))
        except Exception:
            print()

        try:
            if blanck[1] - 1 > -1:
                m[(blanck[0], blanck[1] - 1)] = (dM[blanck[0]][blanck[1] - 1] +
                                            np.abs(self.state[blanck[0]][blanck[1] - 1] - self.stateFinal[blanck[0]][blanck[1] - 1]))
        except Exception:
            print()

        m = {k: v for k, v in sorted(m.items(), key=lambda item: item[1], reverse=True)}

        keys = list(m.keys())


        for i in keys:
            self.nextStep(blanck, i)
            key = str(self.state)
            if key not in self.usedMoves:
                self.usedMoves[key] = 1
                break
            else:
                self.nextStep(blanck, i)


    def updateU(self):
        dM, tD, blanck = self.distanceManhattan()

        if tD == 0:
            self.done = 1
            return

        self.switchPiece(blanck, dM)

        self.chargePuzzle()


h, w = 300, 300
border = 5

v = visor(0, 10)

pygame.init()
screen = pygame.display.set_mode((w + (2 * border), h + (2 * border)))
pygame.display.set_caption("Serious Work - not games")
done = False
clock = pygame.time.Clock()

    # Get a font for rendering the frame number
basicfont = pygame.font.SysFont(None, 32)

    # Clear screen to white before drawing
screen.fill((255, 255, 255))
steps = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

            # Convert to a surface and splat onto screen offset by border width and height
    surface = pygame.surfarray.make_surface(v.table)

    surface = pygame.transform.scale(surface, (300, 300))
    screen.blit(surface, (border, border))

    pygame.display.flip()
    clock.tick(60)


    v.updateU()

    # time.sleep(1)

