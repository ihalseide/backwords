import pygame
from drawing import draw_text
from random import randint
from math import sqrt

class Bubble:
    def __init__ (self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.show = True
        self.speed = 100 // self.r

def rbubble ():
    x = randint(0, 500)
    y = randint(-1500, 0)
    r = randint(20, 50)
    color = (randint(200, 255), randint(200, 255), randint(200, 255))
    return Bubble(x, y, r, color)

def dist (x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx*dx + dy*dy)

def intersect (bubble, point):
    return dist(bubble.x, bubble.y, point[0], point[1]) <= bubble.r

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Bubble Pop')
run = True
bubbles = [rbubble() for x in range(20)]
nbubbles = len(bubbles)
clock = pygame.time.Clock()

while run:
    clock.tick(60)
    clicks = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicks.append(event.pos)
    screen.fill((100, 100, 255))
    for b in bubbles:
        if b.show:
            pygame.draw.circle(screen, b.color, (b.x, b.y), b.r, 1)
            for c in clicks:
                if intersect(b, c):
                    b.show = False
                    nbubbles -= 1
                    clicks.remove(c)
        b.y += b.speed
        if b.y > 600:
            b.y = -1500
    if nbubbles == 0:
        draw_text(screen, font, (255, 255, 255), 'You burst my bubbles!', 150, 240)
    pygame.display.update()
pygame.quit()

