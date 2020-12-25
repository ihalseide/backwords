#!/usr/bin/env python3
import time
import pygame
from virtual_machine import VM
import drawing

def init_screen (title, width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    return screen
    
def poll (machine, screen):
    do_redraw = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            do_step(machine)
            do_redraw = True
    return True, do_redraw

def draw_text (screen, font, color, string, x, y, antialias=False):
    txt = font.render(string, antialias, color)
    screen.blit(txt, (x, y))

def draw_2p_arrow (screen, color, x1, y1, x2, y2):
    dy = y2 - y1
    pygame.draw.line(screen, color, (x1, y1), (x1 + dy, y2))
    draw_hz_arrow(screen, color, x1 + dy, y2, x2)

def draw_hz_arrow (screen, color, x, y, end_x):
    head_width = 12
    head_height = 6
    pygame.draw.line(screen, color, (x, y), (end_x, y))
    points = [(end_x - head_width, y - head_height),
              (end_x - head_width, y + head_height),
              (end_x, y)]
    pygame.draw.polygon(screen, color, points)

def draw_stack (screen, font, color, stack, x, y, width, height):
    pad_x = 24
    if stack:
        # Draw the top of stack indicator
        draw_hz_arrow(screen, color, x, y + height//2, x + pad_x)
        # Draw all stack values
        for i, item in enumerate(reversed(stack)):
            ix = x + pad_x
            iy = y + i * height
            draw_text(screen, font, color, str(item), pad_x + ix, iy)
            pygame.draw.rect(screen, color, (x + pad_x, iy, width, height), 1)
    else:
        # Indicate an empty stack
        draw_text(screen, font, color, 'Empty', x + pad_x, y)

def hex_nibble (x) -> str:
    assert (0 <= x < 16)
    return '0123456789ABCDEF'[x]

def byte_string (byte) -> str:
    assert (0 <= byte <= 255)
    high = byte >> 4
    low = byte & 0x0f
    return hex_nibble(high) + hex_nibble(low)

def draw_byte (screen, font, color, x, y, size, byte):
    pygame.draw.rect(screen, color, (x, y, size, size), 1)
    draw_text(screen, font, color, byte_string(byte), x + 2, y + 3)

def draw_memory (memory, start, length, screen, font, color, x, y, cell_size, columns):
    iy = y
    for i in range(start, start + min(len(memory) - start, length)):
        ix = x + (i % columns) * cell_size
        iy = y + (i // columns) * cell_size
        b = memory[i]
        draw_byte(screen, font, color, ix, iy, cell_size, b)

def pad0 (num, zeroes):
    s = str(num)
    l = len(s)
    if l < zeroes:
        return '0' * (zeroes - l) + s
    else:
        return s

def mem_address (x):
    s = pad0(x * 10, zeroes=4)
    return '0x%s' % s

def draw_memory_view(screen, machine, x, y, color, fonts):
    draw_text(screen, fonts[20], color, "Memory", x, y)
    header = '0123456789ABCDEF'
    pad_x = 50
    cell_size = 20
    num_columns = 16
    for i, txt in enumerate(header):
        draw_text(screen, fonts[20], color, txt, pad_x + 4 + x + i * cell_size, y + 24)
    rows = len(machine.memory) // num_columns + 1
    for i in range(rows):
        draw_text(screen, fonts[14], color, mem_address(i), x, 3 + y + 48 + i * cell_size)
    draw_memory(machine.memory, 0, len(machine.memory), screen, fonts[14], color, pad_x + x, y + 48, columns=num_columns, cell_size=cell_size)

def render (machine, screen, fonts):
    screen.fill((0, 0, 0))

    # Machine state
    state = machine.state
    if state == 'running':
        state = 'compiling' if machine.is_compiling else 'interpretting'
    x, y = 10, 5
    color = (0, 255, 255)
    draw_text(screen, fonts[20], color, 'State', x, y)
    draw_text(screen, fonts[20], color, state, x, y + 20)

    # Instruction pointer
    color = (255, 0, 0)
    x, y = 10, 80
    draw_text(screen, fonts[20], color, "Instruction Pointer", x, y)
    draw_text(screen, fonts[20], color, str(machine.ip), x, y + 20)

    # Parameter Stack
    color = (255, 255, 0)
    x, y = 410, 5
    draw_text(screen, fonts[20], color, "Parameter Stack", x, y)
    draw_stack(screen, fonts[20], color, machine.stack, x, y + 24, 150, 24)

    # Return stack
    color = (255, 100, 10)
    x, y = 615, 5
    draw_text(screen, fonts[20], color, "Return Stack", x, y)
    draw_stack(screen, fonts[20], color, machine.returns, x, y + 24, 150, 24)

    # Memory
    draw_memory_view(screen, machine, x=10, y=140, color=(255, 255, 255), fonts=fonts)

def loop (machine, screen, fonts):
    keep_going = True
    do_redraw = True
    while keep_going:
        if do_redraw:
            render(machine, screen, fonts)
        keep_going, do_redraw = poll(machine, screen)
        pygame.display.update()

def cleanup ():
    pygame.quit()

def init_fonts (fontname, sizes):
    pygame.font.init()
    fonts = {size: pygame.font.SysFont(fontname, size) for size in sizes}
    return fonts

def init_machine ():
    machine = VM()
    machine.memory = [0 for x in range(100)]
    machine.memory[0] = machine.primitive('?')
    machine.memory[1] = machine.primitive('.')
    machine.ip = 0
    return machine

def do_step (machine):
    if machine.state == 'reset':
        machine.state = 'stepping'
    else:
        machine.next()

def main ():
    try:
        screen = init_screen('Virtual Machine Visualizer', 800, 600)
        fonts = init_fonts('ibm3270,Courier New,monospace', (20, 14))
        machine = init_machine()
        loop(machine, screen, fonts)
    finally:
        cleanup()

if __name__ == '__main__':
    main()
