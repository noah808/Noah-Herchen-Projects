import pygame
import numpy as np
from math import *
from spheres import create_sphere


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("let's go")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

THETA_COUNT = 20
PHI_COUNT = 10

theta = np.linspace(0, 2*pi, THETA_COUNT)
phi = np.linspace(0, pi, PHI_COUNT)
points = create_sphere(theta, phi, 1)

scale = 100
circle_pos = (WIDTH/2, HEIGHT/2)

projected_points = [
    [n, n] for n in range(len(points))
]

def connect_points(i, j, points):
    pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]), 1)
def fill_points(tl, bl, tr, br, color, points):
    print(type(tl))
    print(tl, bl, tr, br)
    pygame.draw.polygon(screen, color, [(points[tl][0], points[tl][1]), (points[bl][0], points[bl][1]), (points[br][0], points[br][1]), (points[tr][0], points[tr][1])])

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

angle = 0

clock = pygame.time.Clock()

while True:

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


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

    angle +=0.01

    screen.fill(WHITE)
    i = 0
    for p in points:
        rotated2d = np.dot(rotation_z, p.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale + circle_pos[0])
        y = int(projected2d[1][0] * scale + circle_pos[1])

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, BLACK, (x, y), 5)
        i += 1
    for c in range(THETA_COUNT * PHI_COUNT):
        if c+1 < THETA_COUNT * PHI_COUNT:
            connect_points(c, c+1, projected_points)
        if c+THETA_COUNT < THETA_COUNT * PHI_COUNT:
            connect_points(c, c+THETA_COUNT, projected_points)
        if c+THETA_COUNT+1 < THETA_COUNT * PHI_COUNT:
            color = (127.5 + np.matrix.tolist(points[c])[0][0] * 127.5, 127.5 + np.matrix.tolist(points[c])[0][1] * 127.5, 127.5 + np.matrix.tolist(points[c])[0][2] * 127.5)
            fill_points(c, c+THETA_COUNT, c+1, c+THETA_COUNT+1, color, projected_points)
    pygame.display.update()