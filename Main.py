import pygame
import os
import sys

pygame.init()

# Первостепенные константы

size = width, height = 800, 600
Display = pygame.display.set_mode(size)
tile_width = tile_height = 50
UP = 273
LEFT = 276
RIGHT = 275
GRAVITY = 0.2

# Первостепенные функции


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, collorkey=None, transform=None):
    fullname = os.path.join('data\\for test', name)
    image = pygame.image.load(fullname).convert()
    if collorkey:
        if collorkey == -1:
            collorkey = image.get_at((0, 0))
        image.set_colorkey(collorkey)
    else:
        image = image.convert_alpha()

    if transform:
        if transform == 'p':
            image = pygame.transform.scale(image, (image.get_width(
            ) + tile_width // 2, image.get_height() + tile_height // 2))
    return image

# группы


all_sprite = pygame.sprite.Group()
all_sprite_without_player = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_images = {'grass': load_image('jungle_test.png')}
player_image = load_image('knight_test_l.png', transform='p')

# классы


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprite)
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.Right = False
        self.Left = False
        self.Up = False
        self.stand = False
        self.speed_x = 150
        self.speed_y = 0

    def direct_on(self, *sides):

        for el in sides:
            if el == LEFT:
                self.Left = True

            elif el == RIGHT:
                self.Right = True

            if el == UP:
                self.Up = True

    def direct_Off(self, *sides):
        for el in sides:
            if el == LEFT:
                self.Left = False

            elif el == RIGHT:
                self.Right = False

            if el == UP:
                self.Up = False

    def update(self):

        if self.Right:
            self.rect = self.rect.move(-(-self.speed_x // FPS), 0)
            if pygame.sprite.groupcollide(player_group, tiles_group, False, False, pygame.sprite.collide_mask):
                self.rect = self.rect.move(-self.speed_x // FPS, 0)

        elif self.Left:
            self.rect = self.rect.move(-self.speed_x // FPS, 0)
            if pygame.sprite.groupcollide(player_group, tiles_group, False, False, pygame.sprite.collide_mask):
                self.rect = self.rect.move(-(-self.speed_x // FPS), 0)

        if self.Up:
            self.speed_y = -8
            self.Up = False

        if not self.Up:
            self.rect = self.rect.move(0, self.speed_y)
            if pygame.sprite.groupcollide(player_group, tiles_group, False, False, pygame.sprite.collide_mask):
                self.rect = self.rect.move(0, -self.speed_y)
                if self.speed_y < 0:
                    self.speed_y = 0

            self.speed_y += GRAVITY
            if self.speed_y > 5:
                self.speed_y = 5
            


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprite, all_sprite_without_player)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
    
    def apply(self, obj):
        #print(obj)
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        #print(obj.rect)
        

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)




# второстепенные функции (вспомогательные)


def load_level(filname):
    filname = 'data/levels/' + filname
    with open(filname, 'r') as MapFile:
        level_map = [line.strip() for line in MapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('grass', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x, y


FPS = 120
Clock = pygame.time.Clock()
camera = Camera()

player, level_x, level_y = generate_level(load_level('level_1.txt'))
camera.update(player)


Is_game_on = True
Time_count = 0

while Is_game_on:
    Display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            index = [index for index, value in enumerate(
                pygame.key.get_pressed()) if value == 1]
            player.direct_on(*index)

        elif event.type == pygame.KEYUP:
            up_keys = []
            if event.key == UP:
                up_keys.append(UP)
            if event.key == LEFT:
                up_keys.append(LEFT)
            elif event.key == RIGHT:
                up_keys.append(RIGHT)
            player.direct_Off(*up_keys)

    player_group.update()
    player_group.draw(Display)
    tiles_group.draw(Display)
    pygame.display.flip()
    camera.update(player)
    for el in all_sprite:
        camera.apply(el)
    Time_count += Clock.tick(FPS)
