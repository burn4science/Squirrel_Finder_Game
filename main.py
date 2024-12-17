import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 640, 480
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squirrel Finder")

# Load images
koala_img = pygame.image.load('koala.png')
koala_img = pygame.transform.scale(koala_img, (40, 40))

strawberry_img = pygame.image.load('strawberry.png')
strawberry_img = pygame.transform.scale(strawberry_img, (40, 40))

squirrel_img = pygame.image.load('squirrel.png')
squirrel_img = pygame.transform.scale(squirrel_img, (40, 40))

# Define colors
DARK_BG = (15, 15, 15)
RETRO_GREEN = (0, 255, 0)
RETRO_RED = (255, 0, 0)

# Set up fonts
FONT = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

def display_instructions():
    WINDOW.fill(DARK_BG)
    instructions = [
        "Instructions:",
        "You are the koala.",
        "Use the arrow keys to move.",
        "Avoid the strawberries.",
        "After 3 seconds, find the squirrel to win.",
        "Press any key to start."
    ]
    y_offset = HEIGHT // 2 - 100
    for line in instructions:
        text = FONT.render(line, True, RETRO_GREEN)
        text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
        WINDOW.blit(text, text_rect)
        y_offset += 40
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main():
    while True:
        run_game()

def run_game():
    # Game variables
    koala_pos = [WIDTH // 2, HEIGHT // 2]
    koala_speed = 5

    strawberries = []
    strawberry_spawn_timer = 0

    squirrel = None
    squirrel_spawned = False

    start_time = pygame.time.get_ticks()

    game_over = False
    win = False

    display_instructions()

    while not game_over:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000  # in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            koala_pos[0] -= koala_speed
        if keys[pygame.K_RIGHT]:
            koala_pos[0] += koala_speed
        if keys[pygame.K_UP]:
            koala_pos[1] -= koala_speed
        if keys[pygame.K_DOWN]:
            koala_pos[1] += koala_speed

        # Keep koala on screen
        koala_pos[0] = max(0, min(WIDTH - 40, koala_pos[0]))
        koala_pos[1] = max(0, min(HEIGHT - 40, koala_pos[1]))

        # Spawn strawberries every second
        if current_time - strawberry_spawn_timer > 1000:
            strawberry_spawn_timer = current_time
            strawberry_pos = [random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
            strawberry_vel = [random.choice([-3, 3]), random.choice([-3, 3])]
            strawberries.append({'pos': strawberry_pos, 'vel': strawberry_vel})

        # Update strawberries
        for strawberry in strawberries:
            strawberry['pos'][0] += strawberry['vel'][0]
            strawberry['pos'][1] += strawberry['vel'][1]

            # Bounce off walls
            if strawberry['pos'][0] <= 0 or strawberry['pos'][0] >= WIDTH - 40:
                strawberry['vel'][0] *= -1
            if strawberry['pos'][1] <= 0 or strawberry['pos'][1] >= HEIGHT - 40:
                strawberry['vel'][1] *= -1

        # Check collision with strawberries
        koala_rect = pygame.Rect(koala_pos[0], koala_pos[1], 40, 40)
        for strawberry in strawberries:
            strawberry_rect = pygame.Rect(strawberry['pos'][0], strawberry['pos'][1], 40, 40)
            if koala_rect.colliderect(strawberry_rect):
                game_over = True

        # Spawn squirrel after 3 seconds
        if elapsed_time >= 3 and not squirrel_spawned:
            squirrel_spawned = True
            squirrel_pos = [random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
            squirrel_vel = [random.choice([-3, 3]), random.choice([-3, 3])]
            squirrel = {'pos': squirrel_pos, 'vel': squirrel_vel}

        # Update squirrel
        if squirrel_spawned:
            squirrel['pos'][0] += squirrel['vel'][0]
            squirrel['pos'][1] += squirrel['vel'][1]

            # Bounce off walls
            if squirrel['pos'][0] <= 0 or squirrel['pos'][0] >= WIDTH - 40:
                squirrel['vel'][0] *= -1
            if squirrel['pos'][1] <= 0 or squirrel['pos'][1] >= HEIGHT - 40:
                squirrel['vel'][1] *= -1

            # Check collision with squirrel
            squirrel_rect = pygame.Rect(squirrel['pos'][0], squirrel['pos'][1], 40, 40)
            if koala_rect.colliderect(squirrel_rect):
                game_over = True
                win = True

        # Draw everything
        WINDOW.fill(DARK_BG)
        WINDOW.blit(koala_img, koala_pos)
        for strawberry in strawberries:
            WINDOW.blit(strawberry_img, strawberry['pos'])
        if squirrel_spawned:
            WINDOW.blit(squirrel_img, squirrel['pos'])

        # Draw "openai" and timer
        openai_text = FONT.render("openai", True, RETRO_GREEN)
        WINDOW.blit(openai_text, (10, 10))
        timer_text = FONT.render(f"Time: {int(elapsed_time)}", True, RETRO_GREEN)
        WINDOW.blit(timer_text, (WIDTH - 150, 10))

        pygame.display.flip()

        if game_over:
            if win:
                display_end_message("You Win!")
            else:
                display_end_message("Game Over!")
            break

def display_end_message(message):
    WINDOW.fill(DARK_BG)
    text = FONT.render(message, True, RETRO_RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WINDOW.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()
