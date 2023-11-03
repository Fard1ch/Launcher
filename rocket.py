import pygame
import sys
import random
import math
from screeninfo import get_monitors

# Get information about available monitors
monitors = get_monitors()

# Choose the first monitor (index 0)
monitor = monitors[0]

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = monitor.width, monitor.height
PLAYER_RADIUS = 20
PLAYER_COLOR = (0, 128, 255)
ENEMY_SIZE = 15
ENEMY_COLOR = (255, 0, 0)
ENEMY_SPEED = 1
BACKGROUND_COLOR = (255, 255, 255)

# Function to create a new enemy
def create_enemy():
    x = random.randint(-ENEMY_SIZE, WIDTH + ENEMY_SIZE)
    y = random.randint(-ENEMY_SIZE, HEIGHT + ENEMY_SIZE)
    direction = random.uniform(0, 2 * math.pi)
    speed = random.uniform(0.5, ENEMY_SPEED)
    return [x, y, direction, speed]

# Score counter
score = 0

# List of enemies (squares)
enemies = [create_enemy() for _ in range(10)]

# Initial player (circle) position
player_x, player_y = WIDTH // 2, HEIGHT // 2

# Time for score increment
score_timer = pygame.time.get_ticks()
score_increment_interval = 3000  # 3000 milliseconds (3 seconds)

# Flags to control game state
game_over = False
show_death_screen = False
final_score = 0

# Font for text
font = pygame.font.Font(None, 36)

# Game menu options
game_menu_options = ["Restart", "Menu", "Quit"]
selected_game_menu_option = 0  # 0 - Restart, 1 - Menu, 2 - Quit

# Color for the highlighted menu item
highlight_color = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Function to display the menu
def display_menu():
    selected_option = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(game_menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(game_menu_options)
                elif event.key == pygame.K_RETURN:
                    if game_menu_options[selected_option] == "Restart":
                        return False
                    elif game_menu_options[selected_option] == "Menu":
                        # Implement the logic for going back to the main menu
                        pass
                    elif game_menu_options[selected_option] == "Quit":
                        pygame.quit()
                        sys.exit()

        screen.fill(BACKGROUND_COLOR)
        for i, option in enumerate(game_menu_options):
            color = (highlight_color if i == selected_option else (0, 0, 0))
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + i * 50))
            screen.blit(text, text_rect)

        pygame.display.flip()

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if not game_over and not show_death_screen:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            # Pause the game and display the menu
            show_death_screen = display_menu()

        # Get mouse cursor position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Update player (circle) position to the cursor position
        player_x, player_y = mouse_x, mouse_y

        # Move enemies and create new ones
        new_enemies = []
        for enemy in enemies:
            enemy_x, enemy_y, direction, speed = enemy
            enemy_x += math.cos(direction) * speed
            enemy_y += math.sin(direction) * speed
            enemy[0] = enemy_x
            enemy[1] = enemy_y

            # Check if the enemy is within the window, otherwise create a new one
            if 0 <= enemy_x <= WIDTH and 0 <= enemy_y <= HEIGHT:
                new_enemies.append(enemy)
            else:
                new_enemies.append(create_enemy())

        enemies = new_enemies

        # Remove enemies that go out of the window

        # Check collision between player and enemies and update scores
        for enemy in enemies:
            if (abs(player_x - enemy[0]) < (PLAYER_RADIUS + ENEMY_SIZE) / 2 and
                    abs(player_y - enemy[1]) < (PLAYER_RADIUS + ENEMY_SIZE) / 2):
                show_death_screen = True
                final_score = score
                break
            else:
                current_time = pygame.time.get_ticks()
                if current_time - score_timer >= score_increment_interval:
                    score += 1
                    score_timer = current_time

        # Update the window
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.circle(screen, PLAYER_COLOR, (int(player_x), int(player_y)), PLAYER_RADIUS)

        for enemy in enemies:
            enemy_x, enemy_y, _, _ = enemy
            # Ось ваша подальша обробка ворогів

            enemy_color = ENEMY_COLOR
            if enemy == game_menu_options[selected_game_menu_option]:
                enemy_color = highlight_color
            pygame.draw.rect(screen, enemy_color, (int(enemy_x), int(enemy_y), ENEMY_SIZE, ENEMY_SIZE))

        # Display the score counter
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    if show_death_screen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_menu_options[selected_game_menu_option] == "Restart":
                        show_death_screen = False
                        game_over = False
                        score = 0
                        enemies = [create_enemy() for _ in range(10)]
                    elif game_menu_options[selected_game_menu_option] == "Menu":
                        # Implement logic to go back to the main menu
                        pass
                    elif game_menu_options[selected_game_menu_option] == "Quit":
                        pygame.quit()
                        sys.exit()

        screen.fill(BACKGROUND_COLOR)
        death_text = font.render("You lose", True, (255, 0, 0))
        score_text = font.render(f"Score: {final_score}", True, (0, 0, 0))
        for i, option in enumerate(game_menu_options):
            text = font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(monitor.width / 2, (monitor.height / 2) + i * 50))
            screen.blit(text, text_rect)
        highlight_rect = pygame.Rect(
            (monitor.width / 2) - 100, (monitor.height / 2) - 25 + selected_game_menu_option * 50, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), highlight_rect, 2)
        screen.blit(death_text, (monitor.width / 2 - 50, 300))
        screen.blit(score_text, (675, 390))
        pygame.display.flip()

