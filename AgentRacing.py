import pygame
import numpy as np
import math
from utils import scale_image

import tensorflow as tf
from Learning import Agent


#tf.compat.v1.disable_eager_execution()

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
        self.angle = 90
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
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90


class PlayerCar(Car):
    IMG = RED_CAR
    START_POS = (180, 200)


    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


def cast_ray(arr, pos, angle):
    #xSlope = math.cos(angle*180/math.pi)
    #ySlope = math.sin(angle * 180 / math.pi)
    angle = angle * math.pi/180
    for i in range(800):
        if arr[int(pos[0] + i * math.cos(angle))][int(pos[1] + i * math.sin(angle))][0] == 0 and arr[int(pos[0] + i * math.cos(angle))][int(pos[1] + i * math.sin(angle))][1] == 121:
            return (pos[1] + i * math.sin(angle), pos[0] + i * math.cos(angle))
    return


pygame.init()
w, h = 800, 800
cx, cy = w//2, h//2
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Race AI Game")
bg_img = pygame.transform.scale(pygame.image.load("track2.png"), (w, h))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS', 30)
screen.fill(WHITE)
run = True
"""
def start():
    text_surface = font.render('Press 1 if you have a map already.', False, (0, 0, 0))
    text_surface2 = font.render('Press 2 if would like to make one.', False, (0, 0, 0))
    screen.blit(text_surface, (150, 350))
    screen.blit(text_surface2, (150, 450))
    pygame.display.flip()
    answer = input()
    if answer == "1":
        screen.fill(WHITE)
        text_surface3 = font.render('Enter the name of your map.', False, (0, 0, 0))
        answer2 = input()
        bg_img = pygame.transform.scale(pygame.image.load(answer2+".png"), (w, h))
"""
def get_reward(speed, obs):
    #dist1 = math.sqrt((obs[0]-obs[10])**2 + (obs[1]-obs[11])**2)
    dist2 = math.sqrt((obs[0]-obs[14])**2 + (obs[1]-obs[15])**2)
    #print(dist2)
    if dist2 == 0:
        return -100.0
    return 2


#start()
players = []
for i in range(1):
    car = PlayerCar(5, 6)
    agent = Agent(gamma = 0.99, epsilon = 1.0, lr = 0.001, input_dims = (18, ),
              n_actions = 2, mem_size = 1000000, batch_size = 64, epsilon_end = 0.01)
    players.append([car, agent])
#scores = []
#eps_history = []
score = 0
while run:
    clock.tick(120)
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    screen.fill(WHITE)
    screen.blit(bg_img, (0, 0))

    """"
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        car.move_forward()
    if key[pygame.K_s]:
        car.move_backward()
    if key[pygame.K_a]:
        car.rotate(left = True)
    if key[pygame.K_d]:
        car.rotate(right = True)
    """
    s = pygame.surfarray.array3d(screen).swapaxes(0, 1)
    s = np.ascontiguousarray(s, dtype=np.uint8)

    done = False
    for car, agent in players:
        car.move_forward()
        rot_img = pygame.transform.rotate(car.IMG, car.angle)
        new_rect = rot_img.get_rect(
            center=car.IMG.get_rect(topleft=(car.x - car.IMG.get_width() / 2, car.y - car.IMG.get_height() / 2)).center)
        screen.blit(rot_img, new_rect.topleft)
        #pygame.display.flip()
        spot1=(car.x, car.y)
        spot2=cast_ray(s, (car.y, car.x), car.angle % 360)
        spot3=cast_ray(s, (car.y, car.x), (car.angle + 45) % 360)
        spot4=cast_ray(s, (car.y, car.x), (car.angle + 90) % 360)
        spot5=cast_ray(s, (car.y, car.x), (car.angle + 135) % 360)
        spot6=cast_ray(s, (car.y, car.x), (car.angle + 180) % 360)
        spot7=cast_ray(s, (car.y, car.x), (car.angle + 225) % 360)
        spot8=cast_ray(s, (car.y, car.x), (car.angle + 270) % 360)
        spot9=cast_ray(s, (car.y, car.x), (car.angle + 315) % 360)

        rays = [
            spot1[0],
            spot1[1],
            spot2[0],
            spot2[1],
            spot3[0],
            spot3[1],
            spot4[0],
            spot4[1],
            spot5[0],
            spot5[1],
            spot6[0],
            spot6[1],
            spot7[0],
            spot7[1],
            spot8[0],
            spot8[1],
            spot9[0],
            spot9[1]
        ]
        observation = rays
        action = agent.choose_action(observation)
        #print(action)
        #if action == 0:
        #    car.move_forward()
        #if action == 2:
            #car.move_backward()
        if action == 0:
            car.rotate(left=True)
            #print("left")
        if action == 1:
            car.rotate(right=True)
            #print("right")

        nspot1 = (car.x, car.y)
        nspot2 = cast_ray(s, (car.y, car.x), car.angle % 360)
        nspot3 = cast_ray(s, (car.y, car.x), (car.angle + 45) % 360)
        nspot4 = cast_ray(s, (car.y, car.x), (car.angle + 90) % 360)
        nspot5 = cast_ray(s, (car.y, car.x), (car.angle + 135) % 360)
        nspot6 = cast_ray(s, (car.y, car.x), (car.angle + 180) % 360)
        nspot7 = cast_ray(s, (car.y, car.x), (car.angle + 225) % 360)
        nspot8 = cast_ray(s, (car.y, car.x), (car.angle + 270) % 360)
        nspot9 = cast_ray(s, (car.y, car.x), (car.angle + 315) % 360)

        observation_ = [
            nspot1[0],
            nspot1[1],
            nspot2[0],
            nspot2[1],
            nspot3[0],
            nspot3[1],
            nspot4[0],
            nspot4[1],
            nspot5[0],
            nspot5[1],
            nspot6[0],
            nspot6[1],
            nspot7[0],
            nspot7[1],
            nspot8[0],
            nspot8[1],
            nspot9[0],
            nspot9[1]
        ]
        reward = get_reward(car.vel, observation_)
        if reward == -100.0:
            car.reset()
            done = True
        score += reward
        print(score)
        agent.store_transition(rays, action, reward, observation_, done)
        agent.learn()


    
    

    #for i in range(len(rays)):
    #    if rays[i] is not None:
    #        pygame.draw.line(screen, (255, 255, 255), (int(car.x), int(car.y)), rays[i])
    #    pygame.draw.line(screen, (255, 255, 255), (int(car.x), int(car.y)), (rays[10], rays[11]))
    #    pygame.draw.line(screen, (255, 255, 255), (int(car.x), int(car.y)), (rays[14], rays[15]))



    #pygame.draw.circle(screen, s[int(car.y)][int(car.x)], (400, 400), 100)
    #pygame.draw.circle(screen, (0, 0, 0), (car.x, car.y), 10)
    pygame.display.update()

    #  (0, 121, 2)
