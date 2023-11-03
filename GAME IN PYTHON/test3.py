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

            bg = pygame.transform.scale(pygame.image.load("images/bg7.xcf"), (1400, 800))
            screen = pygame.display.set_mode((1400, 800))

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
            player_y = 625

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
            hits = pygame.mixer.Sound("sound/Попадание точно в цель.mp3")
            zombie = pygame.mixer.Sound("sound/inecraft_zombie_.mp3")
            sound_walk = pygame.mixer.Sound("sound/byistraya-hodba-po-betonnoy-poverhnosti-26128.mp3")
            sound_walki = False
            sound_walk.set_volume(0.2)
            sound_walk_r = pygame.mixer.Sound("sound/hodba-v-myagkoy-obuvi-po-syiroy-trave-25280.mp3")
            sound_walki_r = False
            sound_walk_r.set_volume(0.2)
            sound_fon = pygame.mixer.Sound("sound/75db3693d2ffc38.mp3")
            sound_fon.set_volume(0.1)







            from pydub import AudioSegment

            # Завантаження аудіофайлу з PyDub
            audio = AudioSegment.from_file('sound/75db3693d2ffc38.mp3')

            # Змінити швидкість відтворення (1.5 - це множник швидкості)
            new_speed = 1.5
            changed_audio = audio.speedup(playback_speed=new_speed)

            # Зберегти змінений аудіофайл
            changed_audio.export('змінений_звук.wav', format='wav')

            # Завантаження зміненого аудіофайлу в Pygame
            soundsd = mixer.Sound('змінений_звук.wav')






            while not game_over:
                if gameplay:
                    sound_fon.play()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a] and player_x > 0:
                        player_x -= player_speed
                        sound_walk.play()
                        sound_walki = True
                    elif not keys[pygame.K_a] and sound_walki:
                        sound_walk.stop()
                        sound_walki = False
                        if keys[pygame.K_a] == pygame.KEYUP:
                            sound_walk.stop()
                    elif keys[pygame.K_d] and player_x < 1300:
                        player_x += player_speed
                        sound_walk_r.play()
                        sound_walki_r = True
                    elif not keys[pygame.K_d] and sound_walki_r:
                        sound_walk_r.stop()
                        sound_walki_r = False
                        if keys[pygame.K_d] == pygame.KEYUP:
                            sound_walk_r.stop()
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
                    sound_walk.stop()
                    sound_walk_r.stop()
                    if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                        gameplay = True
                        player_x = 450
                        enemy_list.clear()
                        bullets_r.clear()


                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    if event.type == enemy_timer:
                        enemy_list.append(enemy.get_rect(topleft=(enemy_x, 625)))
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
            print("Запуск гри Просто Гейм")
            # Отримання інформації про доступні монітори
            monitors = get_monitors()

            # Вибір першого монітора (індекс 0)
            monitor = monitors[0]

            # Ініціалізація Pygame
            pygame.init()

            # Константи для гри "Just Game"
            WIDTH, HEIGHT = monitor.width, monitor.height
            PLAYER_SIZE = 20
            PLAYER_COLOR = (0, 128, 255)
            ENEMY_SIZE = 15
            ENEMY_COLOR = (255, 0, 0)
            ENEMY_SPEED = 1
            BACKGROUND_COLOR = (255, 255, 255)

            # Створення окремого об'єкта screen для гри "Just Game"
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Уникайте фігури!")


            # Початкова позиція гравця (круга)
            player_x, player_y = WIDTH // 2, HEIGHT // 2

            # Створення списку ворогів (квадратів)
            enemies = []

            # Функція для створення нового ворога
            def create_enemy():
                x = random.randint(-ENEMY_SIZE, WIDTH + ENEMY_SIZE)
                y = random.randint(-ENEMY_SIZE, HEIGHT + ENEMY_SIZE)
                direction = random.uniform(0, 2 * math.pi)
                speed = random.uniform(0.5, ENEMY_SPEED)
                enemies.append([x, y, direction, speed])

            # Лічильник балів
            score = 0

            # Флаг для визначення, чи гравець вже зіткнувся з ворогом
            collision = False

            # Час для додавання балів
            score_timer = pygame.time.get_ticks()
            score_increment_interval = 3000  # 3000 мілісекунд (3 секунди)

            # Основний цикл гри
            game_over = False
            while not game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True

                if not game_over:
                    # Отримання позиції курсора миші
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Оновлення позиції гравця (круга) на позицію курсора
                    player_x, player_y = mouse_x, mouse_y

                    # Створення нового ворога з інтервалом
                    if len(enemies) < 10:
                        create_enemy()

                    # Рух ворогів
                    for enemy in enemies:
                        enemy_x, enemy_y, direction, speed = enemy
                        enemy_x += math.cos(direction) * speed
                        enemy_y += math.sin(direction) * speed
                        enemy[0] = enemy_x
                        enemy[1] = enemy_y

                    # Видалення ворогів, які виходять за межі вікна
                    enemies = [enemy for enemy in enemies if 0 <= enemy[0] <= WIDTH and 0 <= enemy[1] <= HEIGHT]

                    # Перевірка зіткнення гравця з ворогами і оновлення балів
                    if not collision:
                        for enemy in enemies:
                            if (abs(player_x - enemy[0]) < (PLAYER_SIZE + ENEMY_SIZE) / 2 and
                                    abs(player_y - enemy[1]) < (PLAYER_SIZE + ENEMY_SIZE) / 2):
                                game_over = True  # Гра закінчилася
                                break
                            else:
                                current_time = pygame.time.get_ticks()
                                if current_time - score_timer >= score_increment_interval:
                                    score += 1  # Збільшуємо балл кожні 3 секунди
                                    score_timer = current_time

                    # Оновлення вікна
                    screen.fill(BACKGROUND_COLOR)
                    pygame.draw.circle(screen, PLAYER_COLOR, (int(player_x), int(player_y)), PLAYER_SIZE)

                    for enemy in enemies:
                        pygame.draw.rect(screen, ENEMY_COLOR, (int(enemy[0]), int(enemy[1]), ENEMY_SIZE, ENEMY_SIZE))

                    # Відображення лічильника балів
                    score_text = font.render(f"Бали: {score}", True, (0, 0, 0))
                    screen.blit(score_text, (10, 10))

                    pygame.display.update()

            pygame.quit()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
