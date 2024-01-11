import pygame as pg
import math

from src.env.utils import *


class Particule:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ttl = 1

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.ttl -= dt

    def draw(self, screen, scale):
        if self.ttl < 0:
            return
        pg.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.x * scale), int(self.y * scale)),
            scale,
        )


class Smoke(Particule):
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.v = math.sqrt(vx**2 + vy**2)
        self.dx = vx / self.v if self.v > 0 else 0
        self.dy = vy / self.v if self.v > 0 else 0
        self.ttl = 1

    def update(self, dt):
        vx = self.dx * self.v * self.ttl**0.5
        vy = self.dy * self.v * self.ttl**0.5
        vy -= 9.81 * dt

        self.x += vx * dt
        self.y += vy * dt
        self.ttl -= dt

    def draw(self, screen, scale):
        if self.ttl < 0:
            return
        r = 0.1 / (self.ttl * self.ttl + 0.1)
        part = pg.Surface((r * 2 * scale, r * 2 * scale),
                          pg.SRCALPHA)
        color = (1 - self.ttl) * 100 + 100
        pg.draw.circle(part, (color, color, color),
                       (int(r * scale), int(r * scale)),
                       int(r * scale))
        part.set_alpha(int(self.ttl * self.ttl * 255))
        screen.blit(part, (self.x * scale - r * scale,
                           self.y * scale - r * scale))
