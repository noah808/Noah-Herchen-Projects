import pygame
import numpy as np
import math
from utils import scale_image

#constants
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 234, 0)
RED_CAR = scale_image(pygame.image.load("red-car.png"), 0.55)
PURPLE_CAR = scale_image(pygame.image.load("purple-car.png"), 0.55)


class Car:
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal


class PlayerCar(Car):
    IMG = RED_CAR
    START_POS = (180, 200)


    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


def cast_ray(arr, pos, dir1, dir2):
    #xSlope = math.cos(angle*180/math.pi)
    #ySlope = math.sin(angle * 180 / math.pi)
    print(arr.shape)
    for i in range(800):
        if arr[int(pos[0] + i * dir1)][int(pos[1] + i * dir2)][0] == 0 and arr[int(pos[0] + i * dir1)][int(pos[1] + i * dir2)][1] == 121:
            return (pos[1] + i * dir2, pos[0] + i * dir1)
    return

pygame.init()
w, h = 800, 800
cx, cy = w//2, h//2
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Race AI Game")
bg_img = pygame.transform.scale(pygame.image.load("track2.png"), (w, h))
clock = pygame.time.Clock()
run = True

car = PlayerCar(2, 3)

while run:
    clock.tick(120)
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    #screen = pygame.image.load("track.png")
    screen.fill(WHITE)
    screen.blit(bg_img, (0, 0))


    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        car.move_forward()
    if key[pygame.K_s]:
        car.move_backward()
    if key[pygame.K_a]:
        car.rotate(left = True)
    if key[pygame.K_d]:
        car.rotate(right = True)

    s = pygame.surfarray.array3d(screen).swapaxes(0, 1)

    rot_img = pygame.transform.rotate(car.IMG, car.angle)
    new_rect = rot_img.get_rect(
        center=car.IMG.get_rect(topleft=(car.x-car.IMG.get_width()/2, car.y-car.IMG.get_height()/2)).center)
    screen.blit(rot_img, new_rect.topleft)
    pygame.display.flip()

    s = np.ascontiguousarray(s, dtype=np.uint8)
    rays = [cast_ray(s, (car.y, car.x), 1, 0), cast_ray(s, (car.y, car.x), -1, 0), cast_ray(s, (car.y, car.x), 0, 1), cast_ray(s, (car.y, car.x), 0, -1)]
    for i in range(len(rays)):
        if rays[i] is not None:
            pygame.draw.line(screen, (255, 255, 255), (int(car.x), int(car.y)), rays[i])



    #pygame.draw.circle(screen, s[int(car.y)][int(car.x)], (400, 400), 100)
    #pygame.draw.circle(screen, (0, 0, 0), (car.x, car.y), 10)
    pygame.display.update()

    #  (0, 121, 2)