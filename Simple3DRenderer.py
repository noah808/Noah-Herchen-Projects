import pygame
import numpy as np
import math

GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 234, 0)

GRAV = 0.1

def rotate2d(pos, rad):
    x,y = pos
    s,c = math.sin(rad), math.cos(rad)
    return x*c-y*s, y*c+x*s


class Cam:
    def __init__(self, pos=(0,0,0), rot=(0,0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel
            x/=100
            y/=100
            self.rot[0]+=y
            self.rot[1] +=x

    def update(self, dt, key):
        s = dt*10

        if key[pygame.K_q]: self.pos[1]-=s
        if key[pygame.K_e]: self.pos[1]+=s

        x,y = s*math.sin(self.rot[1]), s*math.cos(self.rot[1])

        if key[pygame.K_w]:
            self.pos[0]+=x
            self.pos[2]+=y
        if key[pygame.K_s]:
            self.pos[0]-=x
            self.pos[2]-=y
        if key[pygame.K_a]:
            self.pos[0]-=y
            self.pos[2]+=x
        if key[pygame.K_d]:
            self.pos[0]+=y
            self.pos[2]-=x

class Cube:
    vertices = [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    faces = (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
    colors = RED, GREY, GREEN, BLACK, BLUE, YELLOW

    def __init__(self, pos = (0,0,0)):
        x,y,z = pos
        self.verts = [(x+X/2,y+Y/2,z+Z/2) for X,Y,Z in self.vertices]

pygame.init()
w, h = 800, 800
cx, cy = w//2, h//2
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("3D Renderer")
clock = pygame.time.Clock()
run = True
cam = Cam((0, 0, -5))
pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

shape = []
shape = (0,0,0),(0,0,-1),(0,0,1),(0,0,-2),(0,0,2),(-1,0,0),(-1,0,-1),(-1,0,1),(-1,0,-2),(-1,0,2),(1,0,0),(1,0,-1),(1,0,1),(1,0,-2),(1,0,2),(2,0,0),(2,0,-1),(2,0,1),(2,0,-2),(2,0,2),(0,1,0),(0,1,-1),(0,1,1),(-1,1,0),(-1,1,-1),(-1,1,1),(1,1,0),(1,1,-1),(1,1,1)
base_size = 1
#for j in range(base_size // 2 + 1):
#    print(j)
#    for i in range(base_size - 2*j):
#        print("i",i)
#        for k in range(base_size - 2*j):
#            shape.append((i-base_size//2, -j, k-base_size//2))
#print(shape)
cubes = [Cube((x,y,z)) for x,y,z in shape]

while run:
    dt = clock.tick()/1000

    for event in pygame.event.get():
        cam.events(event)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    screen.fill(WHITE)

    face_list = []
    face_color = []
    depth = []

    for obj in cubes:
        vert_list = []
        screen_coords = []


        for x,y,z in obj.verts:
            x -= cam.pos[0]
            y -= cam.pos[1]
            z -= cam.pos[2]
            x, z = rotate2d((x, z), cam.rot[1])
            y, z = rotate2d((y, z), cam.rot[0])
            vert_list.append([x,y,z])

            f = 200 / z
            x, y = x * f, y * f
            screen_coords.append((cx + int(x), cy + int(y)))


        for f in range(len(obj.faces)):
            face = obj.faces[f]
            on_screen = False
            for i in face:
                x,y = screen_coords[i]
                if vert_list[i][2]>0 and x>0 and x<w and y>0 and y<h:
                    on_screen = True
                    break
            if on_screen:
                coords = [screen_coords[i] for i in face]
                face_list.append(coords)
                face_color.append(obj.colors[f])

                depth.append(sum(sum(vert_list[j][i] for j in face)**2 for i in range(3)))

    order = sorted(range(len(face_list)), key = lambda i: depth[i], reverse = 1)

    for i in order:
        try: pygame.draw.polygon(screen, face_color[i], face_list[i])
        except: pass
    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt, key)




