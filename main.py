import random
import sys
import time

import pygame
clock = pygame.time.Clock()

pygame.init()

screen_width = 360
screen_height = 570
screen = pygame.display.set_mode((360, 570))
pygame.display.set_caption('Камень, Ножницы, Бумага')  # # # Название приложения # # #
icon = pygame.image.load('images/icon.png')  # # # Иконка приложения # # #
pygame.display.set_icon(icon)
window = pygame.Surface((360, 570))
bg = pygame.image.load('images/gray-gold.jpg')  # # # Фон(обои) # # #
lose = pygame.image.load('images/game-over1.jpg')
info_game = pygame.Surface((300, 270))
info_string = pygame.Surface((360, 30))
info_string.fill((45, 80, 40))
info_string_fonts = pygame.font.Font(None, 50)
info_string_font = pygame.font.Font(None, 35)
info_strings_font = pygame.font.Font(None, 25)
label = pygame.font.Font(None, 40)
restart_label = label.render('НАЧАТЬ ЗАНОВО', False, (255, 255, 255))
restart_label1 = label.render('НАЧАТЬ ЗАНОВО', False, (41, 29, 82))
quit_label = label.render('ВЫХОД ИЗ ИГРЫ', False, (255, 255, 255))
quit_label1 = label.render('ВЫХОД ИЗ ИГРЫ', False, (41, 29, 82))
restart_label_rect = restart_label.get_rect(topleft=(60, 360))
quit_label_rect = quit_label.get_rect(topleft=(60, 450))
# Определяем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (0, 100, 200)

# Создаем шрифт для текста на кнопке
fonts = pygame.font.Font(None, 20)
# звук кнопки
sound_button = pygame.mixer.Sound('sounds/click.mp3')

# Определяем размеры и позицию кнопки "Ножницы"
button_width = 80
button_height = 50
button_x = (screen_width - button_width) // 2
button_y = 300

# Определяем размеры и позицию кнопки "камень"
button_width1 = 80
button_height1 = 50
button_x1 = 50
button_y1 = 300

# Определяем размеры и позицию кнопки "Бумага"
button_width2 = 80
button_height2 = 50
button_x2 = 230
button_y2 = 300

bg_menu = pygame.mixer.Sound('sounds/89a80930c240b92.mp3')



# # # Игроки в игре # # #
walk_player = [
    pygame.image.load('images/player_robot1.png'),
    pygame.image.load('images/player_robot2.png'),
    pygame.image.load('images/player_robot3.png'),
    pygame.image.load('images/player_robot4.png'),
    pygame.image.load('images/player_robot5.png'),
    pygame.image.load('images/player_robot6.png'),
    pygame.image.load('images/player_robot7.png'),
]
walk_computer = [
    pygame.image.load('images/бот1.png'),
    pygame.image.load('images/бот2.png'),
    pygame.image.load('images/бот3.png'),
    pygame.image.load('images/бот4.png'),
    pygame.image.load('images/бот5.png'),
    pygame.image.load('images/бот6.png'),
    pygame.image.load('images/бот7.png'),
]

class Menu:
    def __init__(self, punkts=None):
        if punkts is None:
            punkts = [120, 140, u'Punkt', (250, 250, 30), (250, 30, 250), 0]
        self.punkts = punkts

    def render(self, powerhnost, font, num_punkts):
        for i in self.punkts:
            if num_punkts == i[5]:
                powerhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                powerhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.Font('font/Aguante-Regular.otf', 50)
        punkt = 0
        while done:
            screen.fill((0, 100, 200))
            bg_menu.play()
            bg_menu.set_volume(0.3)
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] <= i[0] or mp[0] >= i[0] + 155 or mp[1] <= i[1] or mp[1] >= i[1] + 50:
                    continue
                punkt = i[5]
            self.render(window, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.type == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                        pygame.mixer.stop()
                    elif punkt == 1:
                        sys.exit()


            screen.blit(window, [0, 0])
            pygame.display.flip()


# # # создаем меню # # #
punkts = [(110, 140, u'Game', (250, 250, 30), (250, 30, 250), 0),
          (120, 210, u'Quit', (250, 250, 30), (250, 30, 250), 1)]
game = Menu(punkts)
game.menu()

# Список
actions = ['Камень', 'Ножницы', 'Бумага']

# # # фоновая музыка в игре!!! # # #
bg_sounds = pygame.mixer.Sound('sounds/b19fd19cd041148.mp3')
bg_sounds.play()

answer = pygame.font.Font(None, 50)

playgame = True

score_play = 0
score_computer = 0
player_anim_count = 0
computer_anim_count = 0
result = ''
# запуск игры
running = True
while running:
    if playgame:
        clock.tick(20)
        info_string.fill((41, 29, 82))
        info_string.blit(info_string_font.render('Счет:', True, (WHITE)), (10, 4))
        info_string.blit(info_strings_font.render('Игрок: ' + str(score_play), True, (WHITE)), (100, 10))
        info_string.blit(info_strings_font.render('Компьютер: ' + str(score_computer), True, (WHITE)), (200, 10))
        screen.blit(info_string, (0, 0))
        screen.blit(bg, (0, 30))
        screen.blit(walk_player[player_anim_count], (140, 440))
        screen.blit(walk_computer[computer_anim_count], (140, 20))
        text_surface = answer.render(result, True, WHITE)
        if result == 'Ничья':
            screen.blit(text_surface, (130, 150))
        else:
            screen.blit(text_surface, (80, 150))

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        if computer_anim_count == 3:
            computer_anim_count = 0
        else:
            computer_anim_count += 1



        # Получаем позицию мыши и состояние кнопок мыши
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        mouse_click1 = pygame.MOUSEBUTTONUP

        # Рисуем кнопку "Ножницы"
        pygame.draw.rect(screen, (41, 29, 82), rect=(button_x, button_y, button_width, button_height))

        # Проверяем, наведена ли мышь на кнопку и нажата ли кнопка мыши

        if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
            if mouse_click[0] == 1:
                if sound_button:
                    sound_button.play()
                comp = random.choice(actions)
                time.sleep(0.3)

                # Действие при нажатии на кнопку
                if comp == 'Ножницы':
                    result = 'Ничья'

                if comp == 'Бумага':
                    result = 'Ты выиграл'
                    score_play += 1
                if comp == 'Камень':
                    result = 'Ты проиграл'
                    score_computer += 1

            pygame.draw.rect(screen, (89, 81, 117), (button_x, button_y, button_width, button_height))

        #Рисуем текст на кнопке
        text = fonts.render('Ножницы', True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (button_x + button_width // 2, button_y + button_height // 2)
        screen.blit(text, text_rect)

        # Рисуем кнопку "Камень"
        pygame.draw.rect(screen, (41, 29, 82), rect=(button_x1, button_y1, button_width1, button_height1))

        # Проверяем, наведена ли мышь на кнопку и нажата ли кнопка мыши
        if button_x1 < mouse_pos[0] < button_x1 + button_width1 and button_y1 < mouse_pos[1] < button_y1 + button_height1:
            if mouse_click[0] == 1:
                if sound_button:
                    sound_button.play()
                # Действие при нажатии на кнопку
                comp = random.choice(actions)
                time.sleep(0.3)
                if comp == 'Камень':
                    result = 'Ничья'
                if comp == 'Ножницы':
                    result = 'Ты выиграл'
                    score_play += 1
                if comp == 'Бумага':
                    result = 'Ты проиграл'
                    score_computer += 1

            pygame.draw.rect(screen, (89, 81, 117), (button_x1, button_y1, button_width1, button_height1))

        # Рисуем текст на кнопке
        text = fonts.render('Камень', True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (button_x1 + button_width1 // 2, button_y1 + button_height1 // 2)
        screen.blit(text, text_rect)

        # Рисуем кнопку "Бумагу"
        pygame.draw.rect(screen, (41, 29, 82), rect=(button_x2, button_y2, button_width2, button_height2))

        # Проверяем, наведена ли мышь на кнопку и нажата ли кнопка мыши
        if button_x2 < mouse_pos[0] < button_x2 + button_width2 and button_y2 < mouse_pos[1] < button_y2 + button_height2:
            if mouse_click[0] == 1:
                if sound_button:
                    sound_button.play()
                # Действие при нажатии на кнопку
                comp = random.choice(actions)
                time.sleep(0.3)
                if comp == 'Бумага':
                    result = 'Ничья'
                if comp == 'Камень':
                    result = 'Ты выиграл'
                    score_play += 1
                if comp == 'Ножницы':
                    result = 'Ты проиграл'
                    score_computer += 1

            pygame.draw.rect(screen, (89, 81, 117), (button_x2, button_y2, button_width2, button_height2))

        # Рисуем текст на кнопке
        text = fonts.render('Бумага', True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (button_x2 + button_width2 // 2, button_y2 + button_height2 // 2)
        screen.blit(text, text_rect)
        if score_play == 5 or score_computer == 5:
            bg_sounds.stop()
            playgame = False

        pygame.display.update()

    else:
        bg_menu.play()
        screen.blit(lose, (0, 0))
        screen.blit(restart_label, restart_label_rect)
        screen.blit(quit_label, quit_label_rect)
        screen.blit(info_string_font.render('Счет:', True, (WHITE)), (150, 30))
        screen.blit(info_strings_font.render('Игрок: ' + str(score_play), True, (WHITE)), (70, 80))
        screen.blit(info_strings_font.render('Компьютер: ' + str(score_computer), True, (WHITE)), (180, 80))
        if score_play > score_computer:
            screen.blit(info_string_fonts.render('Ты выиграл', True, (137, 13, 13)), (70, 150))
        else:
            screen.blit(info_string_fonts.render('Ты проиграл', True, (137, 13, 13)), (70, 150))

        mouse = pygame.mouse.get_pos()
        # mouse_click = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                if sound_button:
                    sound_button.play()
                playgame = True
                score_play = 0
                score_computer = 0
                result = ''
                bg_menu.stop()
                bg_sounds.play()
            screen.blit(restart_label1, restart_label_rect)

        if quit_label_rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                if sound_button:
                    sound_button.play()
                running = False
            screen.blit(quit_label1, quit_label_rect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
