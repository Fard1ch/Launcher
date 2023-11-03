import pygame
import sys
import math
import random
from screeninfo import get_monitors

# Отримати інформацію про доступні монітори
monitors = get_monitors()

# Вибрати перший монітор (індекс 0)
monitor = monitors[0]

# Ініціалізація Pygame
pygame.init()
# Колір
black = (0, 0, 0)
white = (255, 255, 255)
highlight_color = (150, 150, 150)

BACKGROUND = pygame.transform.scale(pygame.image.load("bk.png"), (monitor.width, monitor.height))

# Створення шрифту для тексту меню
font = pygame.font.Font(None, 36)

# Опції меню
menu_options = ["Games", "Settings", "Exit"]
game_options = ["Walking Dead", "Just Game", "Back"]
selected_option = 0
selected_game_option = None

class Game:
    def __init__(self):
        self.__screen__ = pygame.display.set_mode((monitor.width, monitor.height))
        self.__clock__ = pygame.time.Clock()

    def run(self):
        global selected_option, selected_game_option, monitor  # Додайте 'monitor' у список глобальних змінних
        while True:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if selected_game_option is None:
                        if event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % len(menu_options)
                        if event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % len(menu_options)
                        if event.key == pygame.K_RETURN:
                            if selected_option == 0:
                                selected_game_option = 0
                            elif selected_option == 1:
                                print("Settings selected")
                            elif selected_option == 2:
                                pygame.quit()
                                sys.exit()
                    else:
                        if event.key == pygame.K_DOWN:
                            selected_game_option = (selected_game_option + 1) % len(game_options)
                        if event.key == pygame.K_UP:
                            selected_game_option = (selected_game_option - 1) % len(game_options)
                        if event.key == pygame.K_RETURN:
                            if selected_game_option == 0:
                                self.start_game("Walking Dead")

                            elif selected_game_option == 1:
                                self.start_game("Just Game")
                            elif selected_game_option == 2:  # Додайте повернення до головного меню
                                selected_game_option = None

            self.__screen__.blit(BACKGROUND, (0, 0))

            if selected_game_option is None:
                highlight_rect = pygame.Rect((monitor.width / 2) - 100, (monitor.height / 2) - 25 + selected_option * 50, 200, 50)
                pygame.draw.rect(self.__screen__, highlight_color, highlight_rect, border_radius=10)
                for i, option in enumerate(menu_options):
                    text = font.render(option, True, white)
                    text_rect = text.get_rect(center=(monitor.width / 2, (monitor.height / 2) + i * 50))
                    self.__screen__.blit(text, text_rect)
            else:
                highlight_rect = pygame.Rect((monitor.width / 2) - 100, (monitor.height / 2) - 25 + selected_game_option * 50, 200, 50)
                pygame.draw.rect(self.__screen__, highlight_color, highlight_rect, border_radius=10)
                for i, option in enumerate(game_options):
                    text = font.render(option, True, white)
                    text_rect = text.get_rect(center=(monitor.width / 2, (monitor.height / 2) + i * 50))
                    self.__screen__.blit(text, text_rect)

            self.__clock__.tick(60)
            pygame.display.update()

    def start_game(self, game_name):
        if game_name == "Walking Dead":

            monitors = get_monitors()
            monitor = monitors[0]

            pygame.init()

            bg = pygame.transform.scale(pygame.image.load("images/bg7.xcf"), (monitor.width, monitor.height))
            screen = pygame.display.set_mode((monitor.width, monitor.height))

            pygame.display.set_caption("HZ")

            player = pygame.image.load("images/p1xcf.xcf").convert_alpha()

            numeric = random.randint(1300, 3000)

            enemy = pygame.transform.scale(pygame.image.load("images/zombie1.gif"), (144, 137)).convert_alpha()
            enemy_x = 1450
            enemy_list = []
            enemy_timer = pygame.USEREVENT + 1
            pygame.time.set_timer(enemy_timer, numeric)

            player_speed = 2
            player_x = 450
            player_y = 725

            label = pygame.font.Font("Domine-VariableFont_wght.ttf", 40)
            lose_label = label.render('Your dead', False, (1, 1, 1))

            restart_label = label.render('Restart', False, (255, 255, 255))
            restart_label_rect = restart_label.get_rect(topleft=(180, 200))

            bullet_r = pygame.transform.scale(pygame.image.load("images/bullet.png"), (15, 8)).convert_alpha()
            bullets_r = []
            bullets_left_r = 12
            text2 = pygame.font.Font("Domine-VariableFont_wght.ttf", 40)
            text_right = text2.render(f"Пулі в лівій зьрої: {bullets_left_r}", False, (255, 255, 255))

            bullet_l = pygame.transform.scale(pygame.image.load("images/bullet.png"), (15, 8)).convert_alpha()
            bullets_l = []
            bullets_left_l = 12
            text1 = pygame.font.Font("Domine-VariableFont_wght.ttf", 40)
            text_left = text1.render(f"Пулі в лівій зьрої: {bullets_left_l}", False, (255, 255, 255))

            gameplay = True

            game_over = False

            shot = pygame.mixer.Sound('sound/Внезапный отличный меткий выстрел из пистолета.mp3')
            shot.set_volume(0.1)

            while not game_over:
                if gameplay:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a] and player_x > 0:
                        player_x -= player_speed
                    elif keys[pygame.K_d] and player_x < monitor.width:
                        player_x += player_speed
                    screen.blit(bg, (0, 0))
                    screen.blit(player, (player_x, player_y))
                    screen.blit(text_right, (20, 20))
                    enemy_rect = enemy.get_rect(topleft=(enemy_x, 625))
                    player_rect = player.get_rect(topleft=(player_x, player_y))
                    if enemy_list:
                        for (i, enemy_rect) in enumerate(enemy_list):
                            screen.blit(enemy, enemy_rect)
                            enemy_rect.x -= 1
                            if enemy_rect.x < -10:
                                enemy_list.pop(i)
                            if player_rect.colliderect(enemy_rect):
                                gameplay = False
                    enemy_list = [e for e in enemy_list if e.x > -150]
                    if bullets_r:
                        for (i, el) in enumerate(bullets_r):
                            screen.blit(bullet_r, (el.x, el.y))
                            el.x -= 6
                            if el.x > 1450:
                                bullets_r.pop(i)
                            elif el.x < 10:
                                bullets_r.pop(i)
                            if enemy_list:
                                for (index, enemy_el) in enumerate(enemy_list):
                                    if el.colliderect(enemy_el):
                                        enemy_list.pop(index)
                                        bullets_r.pop(i)
                    if bullets_l:
                        for (i, l) in enumerate(bullets_l):
                            screen.blit(bullet_l, (l.x, l.y))
                            l.x += 6
                            if l.x > 1450:
                                bullets_l.pop(i)
                            elif l.x < 10:
                                bullets_l.pop(i)
                            if enemy_list:
                                for (index, enemy_el) in enumerate(enemy_list):
                                    if l.colliderect(enemy_el):
                                        enemy_list.pop(index)
                                        bullets_l.pop(i)
                else:
                    screen.fill((255, 0, 0))
                    screen.blit(lose_label, (180, 100))
                    screen.blit(restart_label, restart_label_rect)
                    mouse = pygame.mouse.get_pos()
                    if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                        gameplay = True
                        player_x = 450
                        enemy_list.clear()
                        bullets_r.clear()


                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    if event.type == enemy_timer:
                        enemy_list.append(enemy.get_rect(topleft=(enemy_x, 725)))
                    if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_LEFT and bullets_left_r > 0:
                        bullets_r.append(bullet_r.get_rect(topleft=(player_x + -10, player_y + 50)))
                        shot.play()
                        bullets_left_r -= 1
                    if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_RIGHT and bullets_left_l > 0:
                        bullets_l.append(bullet_l.get_rect(topleft=(player_x + 120, player_y + 50)))
                        shot.play()
                        bullets_left_l -= 1
                    if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_r:
                        bullets_left_r = 12
                        bullets_left_l = 12
            pygame.quit()
        elif game_name == "Just Game":
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
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

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


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
