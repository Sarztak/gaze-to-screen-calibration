import pygame as pm

width, height = 800, 600
pm.init()
clock = pm.time.Clock()
screen = pm.display.set_mode((width, height))


x0, y0 = 100, 200
x, y = x0, y0
radius = 10
length, breath = 300, 200
dx, dy = 5, 5

running = True
while running:
    screen.fill((23, 11, 42))
    if x < x0 + breath:
        x += dx
        pm.draw.circle(screen, (255, 0, 0), (x, y), radius)
    elif y < y0 + length:
        y += dy
        pm.draw.circle(screen, (255, 0, 0), (x, y), radius)
    elif x > x0:
        x -= dx
        pm.draw.circle(screen, (255, 0, 0), (x, y), radius)
    elif y > y0:
        y -= dy
        pm.draw.circle(screen, (255, 0, 0), (x, y), radius)

    for event in pm.event.get():
        if event.type == pm.QUIT:
            running = False

    pm.display.flip()
    clock.tick(60)

pm.quit()
