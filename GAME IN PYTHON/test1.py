import pygame
from screeninfo import get_monitors
import random

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
lose_label = label.render('Your dead', False, (255, 0, 0))
restart_label = label.render('Restart', False, (255, 255, 255))
restart_label_rect = restart_label.get_rect(topleft=(630, 400))

bullet_r = pygame.transform.scale(pygame.image.load("images/bullet.png"),(15, 8)).convert_alpha()
bullets_r = []
bullets_left_r = 12
text2 = pygame.font.Font("Domine-VariableFont_wght.ttf", 40)
text_right = text2.render(f"Пулі в лівій зьрої: {bullets_left_r}", False, (255, 255, 255))

bullet_l = pygame.transform.scale(pygame.image.load("images/bullet.png"),(15, 8)).convert_alpha()
bullets_l = []
bullets_left_l = 12
text1 = pygame.font.Font("Domine-VariableFont_wght.ttf", 40)
text_left = text1.render(f"Пулі в лівій зьрої: {bullets_left_l}", False, (255, 255, 255))

gameplay = True

game_over = False

while not game_over:
    if gameplay:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 1300:
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
                el.x -= 10

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
                l.x += 10

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
        screen.fill((128, 128, 128))
        screen.blit(lose_label, (600, 300))
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
        if event.type == enemy_timer:
            enemy_list.append(enemy.get_rect(topleft=(enemy_x, 625)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_LEFT and bullets_left_r > 0:
            bullets_r.append(bullet_r.get_rect(topleft=(player_x + -10, player_y + 50)))
            bullets_left_r -= 1
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_RIGHT and bullets_left_l > 0:
            bullets_l.append(bullet_l.get_rect(topleft=(player_x + 120, player_y + 50)))
            bullets_left_l -= 1
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_r:
            bullets_left_r = 12
            bullets_left_l = 12

pygame.quit()
