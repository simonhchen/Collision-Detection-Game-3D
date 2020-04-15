import sys
import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Cube(object):
    sides = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
             (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

    def __init__(self, position, size, color):
        self.position = position
        self.color = color
        x, y, z = map(lambda i: i / 2, size)
        self.vertices = (
            (x, -y, -z), (x, y, -z),
            (-x, y, -z), (-x, -y, -z),
            (x, -y, z), (x, y, z),
            (-x, -y, z), (-x, y, z))

    def render(self):
        glPushMatrix()
        glTranslate(*self.position)
        glBegin(GL_QUADS)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        for side in Cube.sides:
            for v in side:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()


class Block(Cube):
    color = (0, 0, 1, 1)
    speed = 0.01

    def __init__(self, position, size):
        super().__init__(position, (size, 1, 1), Block.color)
        self.size = size

    def update(self, dt):
        x, y, z = self.position
        z += Block.speed * dt
        self.position = x, y, z

class Light(object):
    enabled = False
    colors = [(1., 1., 1., 1.), (1., 0.5, 0.5, 1.),
              (0.5, 1., 0.5, 1.), (0.5, 0.5, 1., 1.)]

    def __init__(self, light_id, position):
        self.light_id = light_id
        self.position = position
        self.current_color = 0

    def render(self):
        light_id = self.light_id
        color = Light.colors[self.current_color]
        glLightfv(light_id, GL_POSITION, self.position)
        glLightfv(light_id, GL_DIFFUSE, color)
        glLightfv(light_id, GL_CONSTANT_ATTENUATION, 0.1)
        glLightfv(light_id, GL_LINEAR_ATTENUATION, 0.05)

    def switch_color(self):
        self.current_color += 1
        self.current_color %= len(Light.colors)

    def enable(self):
        if not Light.enabled:
            glEnable(GL_LIGHTING)
            Light.enable = True
        glEnable(self.light_id)


class Sphere(object):
    slices = 40
    stacks = 40

    def __init__(self, radius, position, color):
        self.radius = radius
        self.position = position
        self.color = color
        self.quadratic = gluNewQuadric()

    def render(self):
        glPushMatrix()
        glTranslate(*self.position)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        gluSphere(self.quadratic, self.radius,
                  Sphere.slices, Sphere.stacks)
        glPopMatrix()


class App(object):
    def __init__(self, width=800, height=600):
        self.title = "OpenGL demo"
        self.fps = 60
        self.width = width
        self.height = height
        self.game_over = False
        self.light = Light(GL_LIGHT0, (0, 15, -25, 1))
        self.player = Sphere(1, position=(0, 0, 0),
                             color=(0, 1, 0, 1))
        self.ground = Cube(position=(0, -1, -20),
                           size=(16, 1, 60),
                           color=(1, 1, 1, 1))

    def start(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height),
                                OPENGL | DOUBLEBUF)
        pygame.display.set_caption(self.title)
        glEnable(GL_CULL_FACE)
        # ...
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_CULL_FACE)
        self.main_loop()

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.quit()
            if not self.game_over:
                self.display()
                dt = clock.tick(self.fps)
                for block in self.blocks:
                    block.update(dt)
                self.clear_past_blocks()
                self.add_random_blocks(dt)
                self.check_collisions()
                self.process_input(dt)

    def check_collisions(self):
        blocks = filter(lambda x: 0 < x.positions[2] < 1,
                        self.blocks)
        x = self.player.position[0]
        r = self.player.radius
        for block in blocks:
            x1 = block.position[0]
            s = block.size / 2
            if x1-s < x-r < x1+s or x1-s < x+r < x1+s:
                self.game_over = True
                print("Game over!")

    def process_input(self, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                if event.key == K_F1:
                    self.quit()

        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.distance -= 0.01 * dt
        if pressed[K_DOWN]:
            self.distance += 0.01 * dt
        if pressed[K_LEFT]:
            self.angle -= 0.005 * dt
        if pressed[K_RIGHT]:
            self.angle += 0.005 * dt

        self.distance = max(10, min(self.distance, 20))
        self.angle %= math.pi * 2

    def display(self):
        # ...
        self.light.render()
        self.sphere1.renders()
        self.sphere2.renders()
        pygame.display.flip()
