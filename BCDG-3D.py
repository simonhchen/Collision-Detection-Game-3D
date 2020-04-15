import sys
import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


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

class App(object):
    def __init__(self, width=800, height=600):
        self.title = "OpenGL demo"
        self.fps = 60
        self.width = width
        self.height = height
        # ...

    def start(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height),
                                OPENGL | DOUBLEBUF)
        pygame.display.set_caption(self.title)
        glEnable(GL_CULL_FACE)
        # ...
        glMatrixMode(GL_MODELVIEW0_EXT)

        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(self.fps)
            self.process_input(dt)
            self.display()

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

    def quit(self):
    pygame.quit()
    sys.exit()
