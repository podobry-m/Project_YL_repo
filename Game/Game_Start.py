import pygame

LABELS = ['Название', 'Новая игра', 'Продолжить', 'Достижения', 'Настройки', 'Выход']
Frases = ['Никто из нас уже не сможет сказать, как выглядят трава, деревья и реки.',
          'Раньше эти края были прекрасной зелёной долиной, в которой все жили в радости и достатке',
          '*Показываем картинку деревни*',
          'Но всё изменилось, когда один из нас, возомнивший себя всемогущим, назвал себя Повелителем этого мира и бросил вызов Титанам',
          'Он явно переоценил свои силы и за его надменность поплатились все мы...',
          '*Показываем картину пустоши, выжженной земли, разорённой деревни и тд*',
          'Звали его ..... (Надо придумать). После его поединка с Титанами никто из нашего племени больше не видел его, ',
          'Скорее всего его заточили в ... - тюрьму, откуда нет выхода. Ах, да. Забыл представиться.',
          'Меня зовут ... (Тут вылазит окно, пользователь вводит имя персонажа)',
          'Я его сын. (Вот это поворот)',
          'И я во что бы то ни стало должен найти своего отца и с его помощью восстановить мир в наших землях.',
          'Для этого мне нужно спуститься в подземелья ... и освободить его, чтобы после с его помощью выкрасть у Титанов',
          '... - древний, могущественный артефакт, дарующий владельцу власть над всем/всей ... (Название мира)',
          'Итак, да начнётся приключение.',
          '*Показываем вход в ту тюрьму, перс заходит в неё*']

pygame.init()
SCREENSIZE = WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode(SCREENSIZE)  # , pygame.FULLSCREEN
clock = pygame.time.Clock()
pygame.display.set_caption('Super Game')

#загрузка изображения
def load_image(name):
    return pygame.image.load('data/' + name)

#загрузка музыки: mp3 как фон, остальные аудио грузит как короткие эффекты
def music(name, volume=1):
    if name[-3:] == 'mp3':
        pygame.mixer.music.load('data/' + name)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(volume)
    elif name[-3:] == 'ogg' or name[-3:] == 'wav':
        return pygame.mixer.Sound('data/' + name)
    else:
        print('error sound')

#лейблы меню
def static_labels():
    font = pygame.font.Font(None, 25)
    screen.blit(font.render(LABELS[0], 1, (255, 255, 255), (0, 0, 0)), (450, 100))
    pygame.draw.rect(screen, (123, 0, 123), (435, 90, 150, 30), 1)
    screen.blit(font.render(LABELS[1], 1, (255, 255, 255), (0, 0, 0)), (100 + xl, 150 + yl))
    pygame.draw.rect(screen, (123, 0, 123), (90 + xl, 140 + yl, 130, 30), 1)
    if save:
        screen.blit(font.render(LABELS[2], 1, (255, 255, 255), (0, 0, 0)), (100 + xl, 200 + yl))
        pygame.draw.rect(screen, (123, 0, 123), (90 + xl, 190 + yl, 130, 30), 1)
    else:
        screen.blit(font.render(LABELS[2], 1, (100, 100, 100), (0, 0, 0)), (100 + xl, 200 + yl))
        pygame.draw.rect(screen, (123, 0, 123), (90 + xl, 190 + yl, 130, 30), 1)
    screen.blit(font.render(LABELS[3], 1, (255, 255, 255), (0, 0, 0)), (100 + xl, 250 + yl))
    pygame.draw.rect(screen, (123, 0, 123), (90 + xl, 240 + yl, 130, 30), 1)
    screen.blit(font.render(LABELS[4], 1, (255, 255, 255), (0, 0, 0)), (100 + xl, 300 + yl))
    pygame.draw.rect(screen, (123, 0, 123), (90 + xl, 290 + yl, 130, 30), 1)
    screen.blit(font.render(LABELS[5], 1, (255, 255, 255), (0, 0, 0)), (100 + xl, 350 + yl))
    pygame.draw.rect(screen, (123, 0, 123), (90 + xl, 340 + yl, 130, 30), 1)

#сохранение, загрузка и запись в файл saves.txt
def Saves(save='r'):
    global K, Flag, dialog, menu
    saves = open("saves.txt", save)
    if save == 'r':
        s = saves.readlines()
        if s == []:
            return False
        else:
            K, Flag, dialog, menu = int(s[0].split()[0]), *[bool(int(i)) for i in s[0].split()[1:]]
            return True
    if save == 'w':
        saves.write(str(K) + ' ' + str(int(Flag)) + ' ' + str(int(dialog)) + ' ' + str(int(menu)))


class MainHero(pygame.sprite.Sprite):
    """Класс главного героя. Что умеет:
    1. бегает
    2. стреляет фаерболлами"""
    image = load_image("hero.png", -1)

    def __init__(self, frames_right, frames_left, frames_stand_left, frames_stand_right, start_pos, *groups):
        super().__init__(*groups)
        self.frames_right = frames_right
        self.frames_left = frames_left
        self.frames_stand_left = frames_stand_left
        self.frames_stand_right = frames_stand_right
        self.cur_frame = 0
        self.frame_count = 0
        self.image = self.frames_right[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.vector = 1
        self.vector_left_right = 1
        self.vector_stand = 1
        # проверка на остановку
        self.stand = True
        # чтобы перс не застрявал в верхних стенах
        self.in_wall_prison = False

    def update(self, *args):
        buttons = pygame.key.get_pressed()
        if buttons[pygame.K_UP] and not pygame.sprite.collide_mask(self, walls):
            self.vector = 3
            self.rect.y -= 2
            #if pygame.sprite.collide_mask(self, walls):
                #self.rect.y += 2
            #else:
            self.stand = False
            #else:
                #self.in_wall_prison = True

        if buttons[pygame.K_DOWN] and not pygame.sprite.collide_mask(self, walls):
            self.vector = 4
            self.rect.y += 2
            #if pygame.sprite.collide_mask(self, walls): #or self.in_wall_prison:
                #self.rect.y -= 2
            #else:
            self.stand = False
        if buttons[pygame.K_RIGHT] and not pygame.sprite.collide_mask(self, walls):
            self.vector = 1
            self.vector_left_right = 1
            self.rect.x += 2
            #if pygame.sprite.collide_mask(self, walls): #or self.in_wall_prison:
                #self.rect.x -= 2
            #else:
            self.stand = False
        if buttons[pygame.K_LEFT] and not pygame.sprite.collide_mask(self, walls):
            self.vector = 2
            self.vector_left_right = 2
            self.rect.x -= 2
            #if pygame.sprite.collide_mask(self, walls): #or self.in_wall_prison:
                #self.rect.x += 2
            #else:
            self.stand = False

        # проверка на выход из "стенной тюрьмы"
        #if not pygame.sprite.collide_mask(self, walls):
            #self.in_wall_prison = False
        if self.frame_count % 5 == 0:
            if not self.stand:
                if self.vector_left_right == 1:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames_right)
                    self.image = self.frames_right[self.cur_frame]
                if self.vector_left_right == 2:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames_left)
                    self.image = self.frames_left[self.cur_frame]
            else:
                if self.vector_left_right == 1:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames_right)
                    self.image = self.frames_stand_right[self.cur_frame]
                if self.vector_left_right == 2:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames_left)
                    self.image = self.frames_stand_left[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
        if not (buttons[pygame.K_UP] or buttons[pygame.K_DOWN] or buttons[pygame.K_RIGHT] or buttons[pygame.K_LEFT]):
            self.stand = True
        self.frame_count += 1


class Walls(pygame.sprite.Sprite):
    """"Тупо стены"""
    image = load_image('стены_1.png', -1)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        # камон, это же стены
        pass


class Floor(pygame.sprite.Sprite):
    """"Тупо стены"""
    image = load_image('фон_1.png', -1)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = 23
        self.rect.y = 45
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        # камон, это же пол
        pass


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, *args):
        self.dx = -(args[0].rect.x + args[0].rect.w // 2 - WIDTH // 2)
        self.dy = -(args[0].rect.y + args[0].rect.h // 2 - HEIGHT // 2)


camera = Camera()

all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
fps = 60
K = -1
xl, yl = 0, 50#перемещение лейблов меню от начальной позиции
save = False#save = Saves('r') существует ли последнее сохранение
Flag = False#пока идёт диалог True
dialog = False#если True начинается диалог(другие переменные из списка должны быть False: dialog, menu, lvl, future)
gamerun = True#игровой цикл False завершение
menu = True#если True отображается меню(другие переменные из списка должны быть False: dialog, menu, lvl, future)
lvl = False#если True появляет уровень и управление персонажем(другие переменные из списка должны быть False: dialog, menu, lvl, future)
music('TownTheme.mp3')#фоновая музыка
x_fon, y_fon = 23, 45
x_walls, y_walls = 0, 0
fon = load_image('фон_1.png')
walls = load_image('стены_1.png')
future = False#диалоговае меню "в будущих версиях"(другие переменные из списка должны быть False: dialog, menu, lvl, future)
xl, yl = 0, 50
save = False
Flag = False
dialog = False
gamerun = True
menu = True
lvl = False
music('TownTheme.mp3')
fon = load_image('фон_1.png', -1)
walls = load_image('стены_1.png', -1)
# начальное положение фоновых объектов
x_fon, y_fon = 23, 45
x_walls, y_walls = 0, 0
# создаем маски стен и пола для проверки пересечений
future = False
is_hero = False
while gamerun:
    if dialog:
        font = pygame.font.Font(None, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if Flag == False and K < 14:
                        K += 1
                        Flag = True
                    elif Flag == True and K < 14:
                        K += 1
                    else:
                        Flag = False
                        lvl = True
                        dialog = False
        screen.fill((10, 10, 10))
        if Flag:
            if K not in [2, 5]:
                screen.blit(font.render(Frases[K], 1, (255, 0, 0), (0, 0, 0)), (0, 401))
            elif K == 2:
                screen.blit(font.render(Frases[K], 1, (255, 0, 0), (0, 0, 0)), (0, 401))
            elif K == 5:
                pass
        pygame.draw.line(screen, (123, 0, 123), [0, 400], [1000, 400], 1)
        pygame.display.flip()
    elif menu:
        screen.fill((10, 10, 10))
        static_labels()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1 and (90 < (x - xl) < 220) and (140 < (y - yl) < 170):
                    # dialog = True
                    lvl = True
                    menu = False
                if event.button == 1 and (90 < (x - xl) < 220) and (340 < (y - yl) < 370):
                    Saves('w')
                    gamerun = False
                if event.button == 1 and (90 < (x - xl) < 220) and ((290 < (y - yl) < 320) or (240 < (y - yl) < 270)):
                    future = True
                    menu = False
    elif lvl:
        if not is_hero:
            is_hero = True
            floor = Floor(all_sprites)
            walls = Walls(all_sprites)
            hero = MainHero([load_image("bomzh_vprapo_okonchat0.png", -1), load_image("bomzh_vprapo_okonchat1.png", -1),
                             load_image("bomzh_vprapo_okonchat2.png", -1), load_image("bomzh_vprapo_okonchat3.png", -1),
                             load_image("bomzh_vprapo_okonchat4.png", -1), load_image("bomzh_vprapo_okonchat5.png", -1),
                             load_image("bomzh_vprapo_okonchat6.png", -1),
                             load_image("bomzh_vprapo_okonchat7.png", -1)],
                            [load_image("bomzh_vlevo_okonchat0.png", -1), load_image("bomzh_vlevo_okonchat1.png", -1),
                             load_image("bomzh_vlevo_okonchat2.png", -1), load_image("bomzh_vlevo_okonchat3.png", -1),
                             load_image("bomzh_vlevo_okonchat4.png", -1), load_image("bomzh_vlevo_okonchat5.png", -1),
                             load_image("bomzh_vlevo_okonchat6.png", -1), load_image("bomzh_vlevo_okonchat7.png", -1)],
                            [load_image("stait_vlevo00.png", -1), load_image("stait_vlevo01.png", -1),
                             load_image("stait_vlevo02.png", -1),
                             load_image("stait_vlevo03.png", -1), load_image("stait_vlevo04.png", -1),
                             load_image("stait_vlevo14.png", -1),
                             load_image("stait_vlevo15.png", -1), load_image("stait_vlevo16.png", -1),
                             load_image("stait_vlevo17.png", -1)],
                            [load_image("stait_vpravo00.png", -1), load_image("stait_vpravo01.png", -1), load_image(
                                "stait_vpravo02.png", -1),
                             load_image("stait_vpravo03.png", -1), load_image("stait_vpravo04.png", -1), load_image(
                                "stait_vpravo14.png", -1),
                             load_image("stait_vpravo15.png", -1), load_image("stait_vpravo16.png", -1), load_image(
                                "stait_vpravo17.png", -1)], (800, 300),
                            all_sprites)
            # walls = Walls(all_sprites)
            # floor = Floor(all_sprites)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lvl = False
                gamerun = False
        # buttons = pygame.key.get_pressed()
        # if buttons[pygame.K_RIGHT]:
        #     x_walls -= 5
        #     x_fon -= 5
        # if buttons[pygame.K_LEFT]:
        #     x_walls += 5
        #     x_fon += 5
        # if buttons[pygame.K_UP]:
        #     y_walls += 5
        #     y_fon += 5
        # if buttons[pygame.K_DOWN]:
        #     y_fon -= 5
        #     y_walls -= 5
        screen.fill((0, 0, 0))
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)
        # x_fon += camera.dx
        # y_fon += camera.dy
        # x_walls += camera.dx
        # y_walls += camera.dy

        # screen.blit(fon, (x_fon, y_fon))
        # .blit(walls, (x_walls, y_walls))
        all_sprites.update(event)
        all_sprites.draw(screen)
    elif future:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 25)
        screen.blit(font.render('Эта опция появится в будущих версиях.', 1, (255, 0, 0), (0, 0, 0)), (100, 100))
        screen.blit(font.render('Вернуться в меню.', 1, (255, 0, 0), (0, 0, 0)), (420, 410))
        pygame.draw.rect(screen, (123, 0, 123), (400, 400, 200, 30), 1)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1 and (400 < x < 600) and (400 < y < 430):
                    future = False
                    menu = True
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
