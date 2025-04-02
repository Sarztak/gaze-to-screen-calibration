import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set fixed screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Set dynamic ball radius based on screen size
dot_radius = int(min(WIDTH, HEIGHT) * 0.03)  # 1% of the smallest dimension

# Set speed and movement characteristics
speed = min(WIDTH, HEIGHT) * 0.005  # Scales with screen size
amplitude = min(WIDTH, HEIGHT) * 1  # Size of the oscillation curve

# Initial position (center of screen)
x, y = WIDTH // 2, HEIGHT // 2

# Time variable for smooth movement (to create continuous motion)
time = 0
direction_angle = random.uniform(0, 2 * math.pi)

# Clock for frame rate
clock = pygame.time.Clock()
running = True

# Main loop
while running:
    screen.fill((50, 50, 50))  # Dark grey background

    # Smooth, curvy movement based on random direction and continuous time-based curves
    direction_angle += random.uniform(
        -0.08, 0.08
    )  # Change direction slightly over time
    x += speed * math.cos(direction_angle)  # Moving in x-direction (curved)
    y += speed * math.sin(direction_angle)  # Moving in y-direction (curved)

    # Make sure the ball stays within screen boundaries, bounce if out of bounds
    if x - dot_radius <= 0 or x + dot_radius >= WIDTH:
        direction_angle += math.pi  # Reverse x-direction
    if y - dot_radius <= 0 or y + dot_radius >= HEIGHT:
        direction_angle += math.pi  # Reverse y-direction

    # Draw the dot at the new position
    pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), dot_radius)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS

    # Handle exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

pygame.quit()
