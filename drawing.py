#!/usr/bin/env python3

import pygame
from math import sin, cos
from pygame.draw import line

def draw_text (screen, font, color, string, x, y, antialias=False):
    txt = font.render(string, antialias, color)
    screen.blit(txt, (x, y))

def draw_arrow_head (screen, color, x, y, dx, dy, head_breadth=6, filled=True):
    p0 = (x, y)
    p1 = (x - dx, y - dy)
    p2 = (x - dx, y + dy)
    thickness = 0 if filled else 1
    pygame.draw.polygon(screen, color, points, thickness)

def sign (x):
    return x // abs(x)

def draw_horizontal_arrow_1 (screen, color, x1, x2, y):
    line(screen, color, (x1, y), (x2, y))
    if x1 < x2:
        direction = 'right'
    else:
        direction = 'left'
    draw_arrow_head(screen, color, x2, y, direction)

def draw_horizontal_arrow_2 (screen, color, x1, y1, x2, y2, x_bias=1):
    x0 = x2
    if x1 < x2:
        direction = 'right'
    else:
        direction = 'left'
    x2 += -12 if x1 < x2 else +12
    dy = y2 - y1
    dx = x2 - x1
    dy2 = abs(dy) // 2 * sign(x_bias)
    x3 = x1 + dy2
    line(screen, color, (x1, y1), (x3, y1))
    line(screen, color, (x3, y1), (x2, y2))
    draw_arrow_head(screen, color, x0, y2, direction)

def draw_horizontal_arrow_3 (screen, color, x1, y1, x2, y2, x_bias=1):
    dy = y2 - y1
    dx = x2 - x1
    dy2 = abs(dy) // 2 * sign(x_bias)
    x3 = x1 + dy2
    x4 = (x3 + x2) // 2
    line(screen, color, (x1, y1), (x3, y1))
    line(screen, color, (x3, y1), (x4, y2))
    line(screen, color, (x4, y2), (x2, y2))
    if x3 < x4:
        direction = 'right'
    else:
        direction = 'left'
    draw_arrow_head(screen, color, x2, y2, direction)

def draw_vertical_arrow_1 (screen, color, x, y1, y2):
    line(screen, color, (x1, y), (x2, y))
    if x1 < x2:
        direction = 'right'
    else:
        direction = 'left'
    draw_arrow_head(screen, color, x2, y, direction)

def draw_vertical_arrow_2 (screen, color, x1, y1, x2, y2, y_bias=1):
    x0 = x2
    if x1 < x2:
        direction = 'right'
    else:
        direction = 'left'
    x2 += -12 if x1 < x2 else +12
    dy = y2 - y1
    dx = x2 - x1
    dy2 = abs(dy) // 2 * sign(y_bias)
    x3 = x1 + dy2
    line(screen, color, (x1, y1), (x3, y1))
    line(screen, color, (x3, y1), (x2, y2))
    draw_arrow_head(screen, color, x0, y2, direction)

def draw_vertical_arrow_3 (screen, color, x1, y1, x2, y2, y_bias=1):
    dy = y2 - y1
    dx = x2 - x1
    dy2 = abs(dy) // 2 * sign(y_bias)
    x3 = x1 + dy2
    x4 = (x3 + x2) // 2
    line(screen, color, (x1, y1), (x3, y1))
    line(screen, color, (x3, y1), (x4, y2))
    line(screen, color, (x4, y2), (x2, y2))
    if x3 < x4:
        direction = 'right'
    else:
        direction = 'left'
    draw_arrow_head(screen, color, x2, y2, direction)

