__author__ = 'Mark Weinreuter'

# ! /usr/bin/python

import pygame
from pygame import *

WIN_BREITE = 800
WIN_HOEHE = 640
HALF_BREITE = int(WIN_BREITE / 2)
HALF_HOEHE = int(WIN_HOEHE / 2)

DISPLAY = (WIN_BREITE, WIN_HOEHE)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30


def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    up = down = left = right = running = False
    bg = Surface((32, 32))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                    PPPPPPPPPPP           P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P                                          P",
        "P                          PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                                          P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                                          P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", ]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    total_level_breite = len(level[0]) * 32
    total_level_hoehe = len(level) * 32
    camera = Kamera(total_level_breite, total_level_hoehe)
    entities.add(player)

    while 1:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit("ESCAPE")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.simple_camera(player.rect)

        # update player, draw everything else
        player.update(up, down, left, right, running, platforms)
        for e in entities:
            screen.blit(e.image, (e.rect.x + camera.x, e.rect.y + camera.y))

        pygame.display.update()


class Kamera(object):
    def __init__(self, breite, hoehe):
        self.breite = breite
        self.hoehe = hoehe
        self.x = 0
        self.y = 0

    def aktualisiere(self, ziel):
        l, t = -ziel.x + HALF_BREITE, -ziel.y + HALF_HOEHE

        l = min(0, l)  # stop scrolling at the left edge
        self.x = max(-(self.breite - WIN_BREITE), l)  # stop scrolling at the right edge
        t = max(-(self.hoehe - WIN_HOEHE), t)  # stop scrolling at the bottom
        self.y = min(0, t)  # stop scrolling at the top

    def simple_camera(self, ziel):
        self.x = -ziel.x + HALF_BREITE
        self.y = -ziel.y + HALF_HOEHE


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32, 32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not (left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print
                    "collide right"
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print
                    "collide left"
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    yvel = 0.3
                    self.rect.top = p.rect.bottom


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))


if __name__ == "__main__":
    main()
