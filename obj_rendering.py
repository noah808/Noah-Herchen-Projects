import pygame
from math import *
WIDTH, HEIGHT = 1600, 1200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCALE = 100
LIGHT = (1600, 0, 0)
cw, ch = WIDTH//2, HEIGHT//2
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f_l = []
v_l = []

file = input("What file would you like to render? (please include .obj extension) \n")
with open(file) as f:
    line = f.readline()
    while line:
        if line[0] == "v" and line[1] != "n" and line[1] != "t":
            line = line.split(" ")
            v_l.append([float(line[1]) * SCALE + cw, float(line[2]) * SCALE + ch, float(line[3])])
        elif line[0] == "f":
            if "//" in line:
                f_l.append([line.split(" ")[1].split("//")[0], line.split(" ")[2].split("//")[0], line.split(" ")[3].split("//")[0]])
            elif "/" in line:
                f_l.append([line.split(" ")[1].split("/")[0], line.split(" ")[2].split("/")[0], line.split(" ")[3].split("/")[0]])
            else:
                f_l.append([line.split(" ")[1], line.split(" ")[2], line.split(" ")[3]])
        line = f.readline()

def draw_triangle_lines(i_l, color, v_l, index, quad = False):
    pygame.draw.line(screen, color, (float(v_l[int(i_l[index][0])-1][0]), float(v_l[int(i_l[index][0])-1][1])), (float(v_l[int(i_l[index][1])-1][0]), float(v_l[int(i_l[index][1])-1][1])), 1)
    pygame.draw.line(screen, color, (float(v_l[int(i_l[index][1])-1][0]), float(v_l[int(i_l[index][1])-1][1])), (float(v_l[int(i_l[index][2])-1][0]), float(v_l[int(i_l[index][2])-1][1])), 1)
    pygame.draw.line(screen, color, (float(v_l[int(i_l[index][2])-1][0]), float(v_l[int(i_l[index][2])-1][1])), (float(v_l[int(i_l[index][0])-1][0]), float(v_l[int(i_l[index][0])-1][1])), 1)
    if quad == True:
        pygame.draw.line(screen, color, (float(v_l[int(i_l[index][0]) - 1][0]), float(v_l[int(i_l[index][0]) - 1][1])),
                         (float(v_l[int(i_l[index][2]) - 1][0]), float(v_l[int(i_l[index][2]) - 1][1])), 1)
        pygame.draw.line(screen, color, (float(v_l[int(i_l[index][2]) - 1][0]), float(v_l[int(i_l[index][2]) - 1][1])),
                         (float(v_l[int(i_l[index][3]) - 1][0]), float(v_l[int(i_l[index][3]) - 1][1])), 1)
        pygame.draw.line(screen, color, (float(v_l[int(i_l[index][3]) - 1][0]), float(v_l[int(i_l[index][3]) - 1][1])),
                         (float(v_l[int(i_l[index][0]) - 1][0]), float(v_l[int(i_l[index][0]) - 1][1])), 1)
def draw_triangles(i_l, color_list, v_l, index, quad = False):
    if quad:
        color_val = ((color_list[int(i_l[index][0])-1][0] + color_list[int(i_l[index][1])-1][0] + color_list[int(i_l[index][2])-1][0] + color_list[int(i_l[index][3])-1][0]) / 4, (color_list[int(i_l[index][0])-1][1] + color_list[int(i_l[index][1])-1][1] + color_list[int(i_l[index][2])-1][1] + color_list[int(i_l[index][3])-1][1]) / 4, (color_list[int(i_l[index][0])-1][2] + color_list[int(i_l[index][1])-1][2] + color_list[int(i_l[index][2])-1][2] + color_list[int(i_l[index][3])-1][2]) / 4)
    else:
        color_val = ((color_list[int(i_l[index][0])-1][0] + color_list[int(i_l[index][1])-1][0] + color_list[int(i_l[index][2])-1][0]) / 3, (color_list[int(i_l[index][0])-1][1] + color_list[int(i_l[index][1])-1][1] + color_list[int(i_l[index][2])-1][1]) / 3, (color_list[int(i_l[index][0])-1][2] + color_list[int(i_l[index][1])-1][2] + color_list[int(i_l[index][2])-1][2]) / 3)
    pygame.draw.polygon(screen, color_val, [(float(v_l[int(i_l[index][0])-1][0]), float(v_l[int(i_l[index][0])-1][1])), (float(v_l[int(i_l[index][1])-1][0]), float(v_l[int(i_l[index][1])-1][1])), (float(v_l[int(i_l[index][2])-1][0]), float(v_l[int(i_l[index][2])-1][1]))])
    if quad:
        pygame.draw.polygon(screen, color_val,
                            [(float(v_l[int(i_l[index][0]) - 1][0]), float(v_l[int(i_l[index][0]) - 1][1])),
                             (float(v_l[int(i_l[index][2]) - 1][0]), float(v_l[int(i_l[index][2]) - 1][1])),
                             (float(v_l[int(i_l[index][3]) - 1][0]), float(v_l[int(i_l[index][3]) - 1][1]))])

def ray(pointOne, pointTwo):
    dist = sqrt((pointOne[0] - pointTwo[0])**2 + (pointOne[1] - pointTwo[1])**2 + (pointOne[2] - pointTwo[2])**2)
    phi = atan((pointOne[1]-pointTwo[1])/(pointOne[0]-pointTwo[0]))
    theta = atan((pointOne[2]-pointTwo[2])/(pointOne[0]-pointTwo[0]))
    return [dist, phi, theta]

run = True
clock = pygame.time.Clock()
angle = 0
p_l = v_l
n_c = []
for val in v_l:
    n_c.append([(val[0] - cw)/SCALE, (val[1] - ch)/SCALE, val[2]])
while run:
    ray_list = []
    clr = [(200, 50, 100) for i in range(len(v_l))]
    clock.tick(60)
    angle+=0.01
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    screen.fill((0, 0, 0))
    for i in range(len(f_l)):
        if len(f_l[0]) == 4:
            #draw_triangle_lines(f_l, WHITE, p_l, i, quad=True)
            draw_triangles(f_l, clr, p_l, i, quad=True)
        else:
            #draw_triangle_lines(f_l, WHITE, p_l, i, quad=False)
            draw_triangles(f_l, clr, p_l, i, quad=False)
    for spot in range(len(n_c)):
        x = n_c[spot][0]
        y = n_c[spot][1]
        z = n_c[spot][2]
        p_l[spot] = [(x*cos(angle) + z*sin(angle)) * SCALE + cw, (-y) * SCALE + ch, (-x * sin(angle) + z * cos(angle))]
        ray_list.append(ray(LIGHT, p_l[spot]))
    for i, r in enumerate(ray_list):
        for other in ray_list:
            if r != other:
                if abs(r[1]-other[1]) < 0.1:
                    if abs(r[2] - other[2]) < 0.1:
                        if r[0] > other[0]:
                            #clr[i] = (clr[i][0]*.8, clr[i][1]*.8, clr[i][2]*.8)
                            clr[i] = (255, 255, 255)
    pygame.display.update()