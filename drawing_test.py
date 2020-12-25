#!/usr/bin/env python3

import pygame
from drawing import *

try:
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('monospace', 14)
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    x2, y2 = (300, 300)
    bias = 1
    line_type = True
    color = (205, 10, 100)

    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))
        draw_text(screen, font, (255, 255, 0), 'CLICK to change the end point of the arrow', 10, 10)
        draw_text(screen, font, (255, 255, 0), 'Press SPACE to change the which side of the text the arrow comes from', 10, 30)
        draw_text(screen, font, (255, 255, 0), 'Press TAB to change the arrow line type', 10, 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x2, y2 = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_SPACE:
                    bias *= -1
                elif event.key == pygame.K_TAB:
                    line_type = not line_type
        if bias < 0:
            x1, y1 = (200, 250)
        else:
            x1, y1 = (270, 250)
        draw_text(screen, font, color, 'Arrow!', 220, 240)
        if line_type:
            draw_horizontal_arrow_2(screen, color, x1, y1, x2, y2, x_bias=bias)
        else:
            draw_horizontal_arrow_3(screen, color, x1, y1, x2, y2, x_bias=bias)
        # pygame.draw.circle(screen, (0, 255, 0), (x1, y1), 5)
        # pygame.draw.circle(screen, (255, 0, 0), (x2, y2), 5)
        pygame.display.update()
finally:
    pygame.quit()
