import pygame
import numpy as np
from math import *
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 234, 0)

ACCELERATION = 0.1
THETA_COUNT = 20
PHI_COUNT = 10
angle = 0

rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ])

rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

class Ball:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), speedX = 0,speedY=0, a_dir="down", size = 5, history = False, points = []):
        self.pos = list(pos)
        self.rot = list(rot)
        self.speedX = speedX
        self.speedY = speedY
        self.accel_dir = a_dir
        self.size = size
        self.history = history
        self.points = points
        self.projected_points = [(n, n) for n in range(len(points))]

    def check_collision(self, xMax, yMax):
        if xMax < self.pos[0]+self.size or 0>self.pos[0]-self.size:
            return [True, "X"]
        if yMax < self.pos[1]+self.size or 0>self.pos[1]-self.size:
            return [True, "Y"]
        return False
    def update(self, key):

        i = 0
        for p in self.points:
            rotated2d = np.dot(rotation_z, p.reshape((3, 1)))
            rotated2d = np.dot(rotation_y, rotated2d)
            projected2d = np.dot(projection_matrix, rotated2d)

            x = int(projected2d[0][0] * self.size + self.pos[0])
            y = int(projected2d[1][0] * self.size + self.pos[1])

            self.projected_points[i] = [x, y]
            i += 1

        if self.history == True:
            self.history = False
        else:
            results = self.check_collision(w, h)

            if results is not False:
                self.history = True
                if results[1] == "Y":
                    self.speedY = -self.speedY * .8
                else:
                    self.speedX = -self.speedX * .8

        if key[pygame.K_w]:
            self.accel_dir = "up"
        if key[pygame.K_s]:
            self.accel_dir = "down"
        if key[pygame.K_a]:
            self.accel_dir = "left"
        if key[pygame.K_d]:
            self.accel_dir = "right"

        if self.accel_dir == "right":
            self.pos = (self.pos[0] + self.speedX, self.pos[1] + self.speedY, self.pos[2])
            self.speedX += ACCELERATION
        if self.accel_dir == "left":
            self.pos = (self.pos[0] + self.speedX, self.pos[1] + self.speedY, self.pos[2])
            self.speedX -= ACCELERATION
        if self.accel_dir == "down":
            self.pos = (self.pos[0] + self.speedX, self.pos[1] + self.speedY, self.pos[2])
            self.speedY += ACCELERATION
        if self.accel_dir == "up":
            self.pos = (self.pos[0] + self.speedX, self.pos[1] + self.speedY, self.pos[2])
            self.speedY -= ACCELERATION


pygame.init()
w, h = 800, 800
cx, cy = w//2, h//2
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("3D Renderer")
clock = pygame.time.Clock()
run = True


theta = np.linspace(0, 2 * pi, THETA_COUNT)
phi = np.linspace(0, pi, PHI_COUNT)
points = []
for p in phi:
    for t in theta:
        x = cos(t) * sin(p)
        y = sin(t) * sin(p)
        z = cos(p)
        points.append(np.matrix([x, y, z]))

ball = Ball(pos = (400, 400, 0), points = points, size = 50)

def fill_points(tl, bl, tr, br, color, points):
    pygame.draw.polygon(screen, color, [(points[tl][0], points[tl][1]), (points[bl][0], points[bl][1]), (points[br][0], points[br][1]), (points[tr][0], points[tr][1])])

clock = pygame.time.Clock()

while run:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    screen.fill(WHITE)

    #pygame.draw.circle(screen, BLACK, (ball.pos[0], ball.pos[1]), ball.size)


    for c in range(THETA_COUNT * PHI_COUNT):
        if c+THETA_COUNT+1 < THETA_COUNT * PHI_COUNT:
            color = (127.5 + np.matrix.tolist(points[c])[0][0] * 127.5, 127.5 + np.matrix.tolist(points[c])[0][1] * 127.5, 127.5 + np.matrix.tolist(points[c])[0][2] * 127.5)
            fill_points(c, c+THETA_COUNT, c+1, c+THETA_COUNT+1, color, ball.projected_points)
    pygame.display.flip()

    key = pygame.key.get_pressed()
    ball.update(key)