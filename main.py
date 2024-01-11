import asyncio
import pygame as pg
import math

from src.env.env import Env

pg.init()


clock = pg.time.Clock()
clock.tick()


async def main():

    env = Env(30, 30, 50)

    running = True
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
        #     target_x = np.random.rand() * self.width * 2/3 + self.width / 6
        #     target_y = np.random.rand() * self.height * 2/3 + self.height / 6
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
        #         np.sin(target_timer) * self.width / 4
        #     target_y = self.height / 2 + \
        #         np.cos(target_timer) * self.height / 4

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

        asyncio.sleep(0)


asyncio.run(main())
