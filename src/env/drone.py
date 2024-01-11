import pygame as pg
import math

from src.env.utils import *


class Drone:

    THRUSTER_ROTATION_SPEED = 1
    THRUSTER_POWER_CHANGE_SPEED = 1
    THRUSTER_ANGLE_LIMIT = math.pi / 4

    ROTATION_FRICTION = 0.999
    SPEED_FRICTION = 0.999

    G = 9.81

    def __init__(self, env, x, y):
        self.env = env
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.a = 0
        self.va = 0
        self.lta = math.pi
        self.rta = 0
        self.ltp = 0
        self.rtp = 0
        self.mass = 10
        self.inertia = 10
        self.tp = 98.1

        self.taget_lta = math.pi / 2
        self.taget_rta = math.pi / 2
        self.taget_ltp = 0.5
        self.taget_rtp = 0.5

    def set_target(self, lta, rta, ltp, rtp):
        self.taget_lta = lta
        self.taget_rta = rta
        self.taget_ltp = ltp
        self.taget_rtp = rtp

    def update(self, dt):
        # Thrusters angle.
        if abs(self.lta - self.taget_lta) > Drone.THRUSTER_ROTATION_SPEED * dt:
            self.lta += sign(self.taget_lta - self.lta) * \
                Drone.THRUSTER_ROTATION_SPEED * dt
        else:
            self.lta = self.taget_lta

        if abs(self.rta - self.taget_rta) > Drone.THRUSTER_ROTATION_SPEED * dt:
            self.rta += sign(self.taget_rta - self.rta) * \
                Drone.THRUSTER_ROTATION_SPEED * dt
        else:
            self.rta = self.taget_rta

        # Thrusters power.
        if abs(self.ltp - self.taget_ltp) > Drone.THRUSTER_POWER_CHANGE_SPEED * dt:
            self.ltp += sign(self.taget_ltp - self.ltp) * \
                Drone.THRUSTER_POWER_CHANGE_SPEED * dt
        else:
            self.ltp = self.taget_ltp

        if abs(self.rtp - self.taget_rtp) > Drone.THRUSTER_POWER_CHANGE_SPEED * dt:
            self.rtp += sign(self.taget_rtp - self.rtp) * \
                Drone.THRUSTER_POWER_CHANGE_SPEED * dt
        else:
            self.rtp = self.taget_rtp

        # Cliping.
        self.rta = clip(self.rta, math.pi / 2 - Drone.THRUSTER_ANGLE_LIMIT,
                        math.pi / 2 + Drone.THRUSTER_ANGLE_LIMIT)
        self.lta = clip(self.lta, math.pi / 2 - Drone.THRUSTER_ANGLE_LIMIT,
                        math.pi / 2 + Drone.THRUSTER_ANGLE_LIMIT)
        self.rtp = clip(self.rtp, 0, 1)
        self.ltp = clip(self.ltp, 0, 1)

        # Acceleration.
        fx = 0
        fy = 0
        torq = 0

        # Gravity.
        fy += Drone.G * self.mass

        # Thrusters.
        (ltx, lty), (rtx, rty) = self.thruster_poss()
        ltfx = self.tp * self.ltp * math.cos(self.a + self.lta + math.pi)
        ltfy = self.tp * self.ltp * math.sin(self.a + self.lta + math.pi)
        rtfx = self.tp * self.rtp * math.cos(self.a + self.rta + math.pi)
        rtfy = self.tp * self.rtp * math.sin(self.a + self.rta + math.pi)
        fx += ltfx + rtfx
        fy += ltfy + rtfy
        lttorq = -(ltfx * (lty - self.y) - ltfy * (ltx - self.x))
        rttorq = -(rtfx * (rty - self.y) - rtfy * (rtx - self.x))
        torq += lttorq + rttorq

        # Friciton.
        fx -= self.vx * Drone.SPEED_FRICTION
        fy -= self.vy * Drone.SPEED_FRICTION
        torq -= self.va * Drone.ROTATION_FRICTION

        # Integrates.
        self.vx += fx / self.mass * dt
        self.vy += fy / self.mass * dt
        self.va += torq / self.inertia * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.a += self.va * dt

    def thruster_poss(self):
        return ((self.x - 3 * math.cos(self.a),
                 self.y - 3 * math.sin(self.a)),
                (self.x + 3 * math.cos(self.a),
                 self.y + 3 * math.sin(self.a)))

    def draw(self, screen, scale):
        (ltx, lty), (rtx, rty) = self.thruster_poss()

        p0 = (self.x + 0.5 * math.cos(self.a + math.pi / 2),
              self.y + 0.5 * math.sin(self.a + math.pi / 2))

        def draw_thruster(x, y, angle, power):
            dx = math.cos(angle)
            dy = math.sin(angle)
            ox, oy = rotate_vector(dx, dy, math.pi / 2)
            dx2 = math.cos(angle + math.pi / 2)
            dy2 = math.sin(angle + math.pi / 2)
            dx_2 = math.cos(angle - math.pi / 2)
            dy_2 = math.sin(angle - math.pi / 2)
            dx6 = math.cos(angle + math.pi / 6)
            dy6 = math.sin(angle + math.pi / 6)
            dx_6 = math.cos(angle - math.pi / 6)
            dy_6 = math.sin(angle - math.pi / 6)
            p1 = (x + 0.3 * dx2,
                  y + 0.3 * dy2)
            p2 = (x + 0.3 * dx_2,
                  y + 0.3 * dy_2)
            p3 = (x + 0.5 * dx_6,
                  y + 0.5 * dy_6)
            p4 = (x + 0.5 * dx6,
                  y + 0.5 * dy6)
            p5 = ((p3[0] + p4[0]) / 2 - 0.1 * dx,
                  (p3[1] + p4[1]) / 2 - 0.1 * dy)
            p6 = (p5[0] + 0.2 * dx2,
                  p5[1] + 0.2 * dy2)
            p7 = (p5[0] + 0.2 * dx_2,
                  p5[1] + 0.2 * dy_2)
            p8 = (p5[0] + 0.3 * dx_6,
                  p5[1] + 0.3 * dy_6)
            p9 = (p5[0] + 0.3 * dx6,
                  p5[1] + 0.3 * dy6)
            v5_0 = (p0[0] - p5[0], p0[1] - p5[1])
            d5_0 = math.sqrt(v5_0[0]**2 + v5_0[1]**2)
            e5_0 = (v5_0[0] / d5_0, v5_0[1] / d5_0)
            o5_0 = rotate_vector(e5_0[0], e5_0[1], math.pi / 2)
            p10 = (p0[0] - o5_0[0] * 0.08, p0[1] - o5_0[1] * 0.08)
            p11 = (p0[0] + o5_0[0] * 0.08, p0[1] + o5_0[1] * 0.08)
            p14 = (p5[0] + o5_0[0] * 0.04, p5[1] + o5_0[1] * 0.04)
            p15 = (p5[0] - o5_0[0] * 0.04, p5[1] - o5_0[1] * 0.04)
            p12 = (p11[0] - 1.5 * e5_0[0], p11[1] - 1.5 * e5_0[1])
            p13 = (p14[0] + v5_0[0] - e5_0[0] * 1.5,
                   p14[1] + v5_0[1] - e5_0[1] * 1.5)
            p16 = (p15[0] + v5_0[0] - e5_0[0] * 1.5,
                   p15[1] + v5_0[1] - e5_0[1] * 1.5)
            p17 = (p10[0] - 1.5 * e5_0[0], p10[1] - 1.5 * e5_0[1])

            p18 = ((p8[0] + p9[0]) / 2, (p8[1] + p9[1]) / 2)
            p19 = (p18[0] + 0.4 * dx, p18[1] + 0.4 * dy)
            p20 = (p18[0] + 0.25 * ox, p18[1] + 0.25 * oy)
            p21 = (p18[0] - 0.25 * ox, p18[1] - 0.25 * oy)
            p22 = (p19[0] - 0.1 * ox, p19[1] - 0.1 * oy)
            p23 = (p19[0] + 0.1 * ox, p19[1] + 0.1 * oy)

            pg.draw.circle(screen, (0, 0, 0),
                           (int(x * scale),
                            int(y * scale)),
                           0.3 * scale)
            pg.draw.circle(
                screen,
                (255, 0, 0),
                (int(p18[0] * scale), int(p18[1] * scale)),
                int(0.25 * scale),
            )
            pg.draw.circle(
                screen,
                (255, 0, 0),
                (int(p19[0] * scale), int(p19[1] * scale)),
                int(0.1 * scale),
            )
            pg.draw.polygon(
                screen,
                (255, 0, 0),
                [
                    (int(p20[0] * scale), int(p20[1] * scale)),
                    (int(p21[0] * scale), int(p21[1] * scale)),
                    (int(p22[0] * scale), int(p22[1] * scale)),
                    (int(p23[0] * scale), int(p23[1] * scale)),
                ],
            )
            pg.draw.polygon(screen, (100, 100, 100),
                            [(int(p6[0] * scale), int(p6[1] * scale)),
                             (int(p7[0] * scale), int(p7[1] * scale)),
                             (int(p8[0] * scale), int(p8[1] * scale)),
                             (int(p9[0] * scale), int(p9[1] * scale))])

            pg.draw.polygon(screen, (0, 0, 0),
                            [(int(p1[0] * scale), int(p1[1] * scale)),
                             (int(p2[0] * scale), int(p2[1] * scale)),
                             (int(p3[0] * scale), int(p3[1] * scale)),
                             (int(p4[0] * scale), int(p4[1] * scale))])
            pg.draw.polygon(screen, (100, 100, 100),
                            [(int(p10[0] * scale), int(p10[1] * scale)),
                             (int(p11[0] * scale), int(p11[1] * scale)),
                             (int(p12[0] * scale), int(p12[1] * scale)),
                             (int(p13[0] * scale), int(p13[1] * scale)),
                             (int(p14[0] * scale), int(p14[1] * scale)),
                             (int(p15[0] * scale), int(p15[1] * scale)),
                             (int(p16[0] * scale), int(p16[1] * scale)),
                             (int(p17[0] * scale), int(p17[1] * scale))])
            pg.draw.circle(screen, (100, 100, 100),
                           (int(p5[0] * scale),
                            int(p5[1] * scale)),
                           0.04 * scale)
            # pg.draw.circle(
            #     screen,
            #     color,
            #     (int(p1[0] * scale), int(p1[1] * scale)),
            #     int(r1 * scale),
            # )
            # ox, oy = rotate_vector(self.dx, self.dy, math.pi / 2)
            # pg.draw.polygon(
            #     screen,
            #     color,
            #     [
            #         (int((self.x + ox * r0) * scale),
            #          int((self.y + oy * r0) * scale)),
            #         (int((self.x - ox * r0) * scale),
            #          int((self.y - oy * r0) * scale)),
            #         (int((p1[0] - ox * r1) * scale),
            #          int((p1[1] - oy * r1) * scale)),
            #         (int((p1[0] + ox * r1) * scale),
            #          int((p1[1] + oy * r1) * scale)),
            #     ],
            # )

        draw_thruster(ltx, lty, self.a + self.lta, self.ltp)
        draw_thruster(rtx, rty, self.a + self.rta, self.rtp)

        pg.draw.circle(screen, (0, 0, 0),
                       (int(self.x * scale),
                        int(self.y * scale)),
                       int(scale))
        pg.draw.line(screen, (0, 0, 0),
                     (int(ltx * scale), int(lty * scale)),
                     (int(rtx * scale), int(rty * scale)),
                     int(0.3 * scale))
