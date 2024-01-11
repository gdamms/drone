import pygame as pg
import math
import random

from src.env.drone import Drone
from src.env.particule import Smoke
from src.env.utils import *


class Env:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale
        self.screen = pg.display.set_mode([
            width * scale,
            height * scale,
        ])

        self.particules = []
        self.drone = Drone(self, self.width / 2, self.height / 2)

        self.target_x = self.width / 2
        self.target_y = self.height / 2

    def smoke(self, x, y, vx, vy, dx, dy, p):
        if random.uniform(0, 1) > p:
            return
        ox, oy = rotate_vector(dx, dy, math.pi / 2)

        rand = random.uniform(0, 1) - 0.5
        x += 0.5 * dx + ox * rand * 0.4
        y += 0.5 * dy + oy * rand * 0.4

        pvx = vx + 10 * p * dx
        pvy = vy + 10 * p * dy

        part = Smoke(x, y, pvx, pvy)
        self.particules.append(part)

    def update(self, dt):
        self.drone.update(dt)
        for part in self.particules:
            part.update(dt)
        self.particules = [part for part in self.particules if part.ttl > 0]

        (ltx, lty), (rtx, rty) = self.drone.thruster_poss()
        self.smoke(ltx, lty,
                   self.drone.vx, self.drone.vy,
                   math.cos(self.drone.a + self.drone.lta),
                   math.sin(self.drone.a + self.drone.lta),
                   self.drone.ltp)
        self.smoke(rtx, rty,
                   self.drone.vx, self.drone.vy,
                   math.cos(self.drone.a + self.drone.rta),
                   math.sin(self.drone.a + self.drone.rta),
                   self.drone.rtp)

    def draw(self):
        for part in self.particules:
            part.draw(self.screen, self.scale)

        self.drone.draw(self.screen, self.scale)

        target_color = (255, 0, 0)
        if (self.target_x - self.drone.x)**2 + (self.target_y - self.drone.y)**2 < 0.5**2:
            target_color = (0, 255, 0)
        pg.draw.circle(self.screen, target_color,
                       (int(self.target_x * self.scale),
                        int(self.target_y * self.scale)),
                       0.3 * self.scale)

    def f(x):
        return (1 - math.exp(-(x*x))) * x / abs(x) if x != 0 else 0


if __name__ == '__main__':
    env = Env(30, 30, 50)

    running = True
    clock = pg.time.Clock()
    clock.tick()
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    env.target_x, env.target_y = event.pos
                    env.target_x /= env.scale
                    env.target_y /= env.scale

        dt = clock.tick() / 1000

        # # Random target
        # if target_delay < target_timer:
        #     target_x = math.random.rand() * self.width * 2/3 + self.width / 6
        #     target_y = math.random.rand() * self.height * 2/3 + self.height / 6
        #     target_timer = 0.0
        # else:
        #     if (target_x - drone.x)**2 + (target_y - drone.y)**2 < target_delta**2:
        #         target_timer += dt
        #         target_color = (0, 255, 0)
        #     else:
        #         target_timer = 0.0
        #         target_color = (255, 0, 0)

        # # Circle target
        # if (target_x - drone.x)**2 + (target_y - drone.y)**2 < target_delta**2:
        #     target_timer += self.width * 0.0003
        #     target_x = self.width / 2 + \
        #         math.sin(target_timer) * self.width / 4
        #     target_y = self.height / 2 + \
        #         math.cos(target_timer) * self.height / 4

        lta = math.pi / 2 - env.drone.a - env.drone.va
        rta = math.pi / 2 - env.drone.a - env.drone.va

        ltp = 0.5 - env.drone.a - env.drone.va
        rtp = 0.5 + env.drone.a + env.drone.va

        f_x = Env.f(env.target_x - env.drone.x - env.drone.vx)
        f_y = Env.f(env.target_y - env.drone.y - env.drone.vy)

        ltp *= 1.0 - (1.0 * f_y)
        rtp *= 1.0 - (1.0 * f_y)

        lta += f_x * 0.5
        rta += f_x * 0.5

        env.drone.set_target(lta, rta, ltp, rtp)

        env.update(dt)

        env.screen.fill((121, 223, 255))

        env.draw()

        pg.display.flip()
