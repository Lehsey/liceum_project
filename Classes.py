import pygame
import os

tile_width = tile_height = 50
UP = 273
LEFT = 276
RIGHT = 275
ATTACK = pygame.K_a
GRAVITY = 0.15
PLAYER_ATTACKED = False
FPS = 200

def load_image(name, quantity=None, collorkey=None, rever=None):
    fullname = os.path.join('data\\sprites', name)
    if quantity:
        sprites = []
        for i in range(quantity):
            sprites.append(pygame.image.load(fullname + f'{i}.png'))
            sprites[i] = pygame.transform.scale(sprites[i], (sprites[i].get_width(
            ) + tile_width//2, sprites[i].get_height() + tile_height//2))
        if rever:
            sprites.reverse()
        return sprites
    else:
        image = pygame.image.load(fullname)
        if collorkey:
            if collorkey == -1:
                collorkey = image.get_at((0, 0))
            image.set_colorkey(collorkey)
        else:
            image = image.convert_alpha()
        return image

all_sprite = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bakcground_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tile_images = {'grass': load_image(
    'jungle_test.png'), 'dirt': load_image('jungle_dirt.png'), 'long': load_image('jungle_test_long.png')}
player_images = {'run_r': load_image('player_run_r_', 8), 'run_l': load_image('player_run_l_', 8, rever=True), 'idle_r': load_image(
    'player_idle_r_', 15), 'idle_l': load_image('player_idle_l_', 15, rever=True), 'attack_r': load_image('player_attack_r_', 19),
    'attack_l': load_image('player_attack_l_', 19, rever=True)}
enemy_images = {'run_r': load_image('skel_run_r_', 13), 'run_l': load_image(
    'skel_run_l_', 13, rever=True), 'attack_r': load_image('skel_attack_r_', 18), 'attack_l': load_image('skel_attack_l_', 18, rever=True),
    'dead_r': load_image('skel_dead_r_', 15), 'dead_l': load_image('skel_dead_l_', 15, rever=True)}



class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprite)
        self.cur_sprite = 0
        self.cur_sprite_attack = 0
        self.frames_run = [player_images['run_r'], player_images['run_l']]
        self.frame_idle = [player_images['idle_r'], player_images['idle_l']]
        self.frame_attack = [player_images['attack_r'], player_images['attack_l']]
        self.image = self.frame_idle[0][0]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.Right = False
        self.Left = False
        self.Up = False
        self.can_jump = True
        self.Attack = False
        self.DEAD = False
        self.last_direct = RIGHT
        self.speed_x = 300
        self.speed_y = 0

    def action_on(self, *sides):

        for el in sides:
            if el == LEFT:
                self.Left = True

            elif el == RIGHT:
                self.Right = True

            if el == UP:
                self.Up = True

            if el == ATTACK:
                self.Attack = True

    def action_Off(self, *sides):
        for el in sides:
            if el == LEFT:
                self.Left = False

            elif el == RIGHT:
                self.Right = False

            if el == UP:
                self.Up = False

            if el == ATTACK:
                self.Attack = False

    def update(self):
        for el in pygame.sprite.groupcollide(enemy_group, player_group, False, False, pygame.sprite.collide_mask):
            if self.Attack:
                if (self.cur_sprite_attack >= 6 and self.cur_sprite_attack <= 8) or \
                        (self.cur_sprite_attack >= 1 and self.cur_sprite_attack <= 12) or (self.cur_sprite_attack >= 18 and self.cur_sprite_attack <= 19):
                    el.dead = True
            if el.cur_sprite_attack >= 8 and el.cur_sprite_attack <= 10 and el.Attack:
               self.DEAD = True

        if self.Right:
            self.rect = self.rect.move(-(-self.speed_x // FPS), 0)
            self.last_direct = RIGHT
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(-self.speed_x // FPS, 0)

        elif self.Left:
            self.rect = self.rect.move(-self.speed_x // FPS, 0)
            self.last_direct = LEFT
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(-(-self.speed_x // FPS), 0)

        if not self.can_jump:
            self.Up = False

        if self.Up and self.can_jump:
            self.speed_y = -6.2
            self.Up = False
            self.can_jump = False

        if not self.Up:
            self.rect = self.rect.move(0, self.speed_y)
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect = self.rect.move(0, -self.speed_y)
                if self.speed_y >= 0:
                    self.can_jump = True
                    self.speed_y = 1
                if self.speed_y < 0:
                    self.speed_y = 0
            self.speed_y += GRAVITY
            if self.speed_y > 5:
                self.speed_y = 5

    def animation(self):
        if self.Right or self.Left:
            self.cur_sprite = (self.cur_sprite + 1) % len(self.frames_run[0])
            if self.Right:
                self.image = self.frames_run[0][self.cur_sprite]
            elif self.Left:
                self.image = self.frames_run[1][self.cur_sprite]

        else:
            self.cur_sprite = (self.cur_sprite + 1) % len(self.frame_idle[0])
            if self.last_direct == RIGHT:
                self.image = self.frame_idle[0][self.cur_sprite]
            else:
                self.image = self.frame_idle[1][self.cur_sprite]

        if self.Attack:
            self.cur_sprite_attack = (
                self.cur_sprite_attack + 1) % len(self.frame_attack[0])
            if self.last_direct == RIGHT:
                self.image = self.frame_attack[0][self.cur_sprite_attack]
            if self.last_direct == LEFT:
                self.image = self.frame_attack[1][self.cur_sprite_attack]
        else:
            self.cur_sprite_attack = 0
        prev_bot_cent = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = prev_bot_cent
        self.mask = pygame.mask.from_surface(self.image)


class Skelet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprite)
        self.cur_sprite = 0
        self.cur_sprite_attack = 0
        self.dead_spr = 0
        self.frames_run = [enemy_images['run_r'], enemy_images['run_l']]
        self.frames_attack = [enemy_images['attack_r'], enemy_images['attack_l']]
        self.dead_frames = [enemy_images['dead_r'], enemy_images['dead_l']]
        self.image = self.frames_run[0][0]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.frames_run[0][0])
        self.Right = False
        self.Left = True
        self.dead = False
        self.can_move = True
        self.Attack = False
        self.speed_x = 80
        self.speed_y = 0

    def animation(self):
        if not self.dead:
            if self.Attack:
                if self.Right:
                    self.image = self.frames_attack[0][self.cur_sprite_attack]
                    self.cur_sprite_attack = (
                        self.cur_sprite_attack + 1) % len(self.frames_attack[0])
                else:
                    self.image = self.frames_attack[1][self.cur_sprite_attack]
                    self.cur_sprite_attack = (
                        self.cur_sprite_attack + 1) % len(self.frames_attack[0])

            else:
                self.cur_sprite_attack = 0
                self.cur_sprite = (self.cur_sprite +
                                   1) % len(self.frames_run[0])
                if self.Right:
                    self.image = self.frames_run[0][self.cur_sprite]
                elif self.Left:
                    self.image = self.frames_run[1][self.cur_sprite]
        else:
            if self.dead_spr < 15:
                if self.Right:
                    self.image = self.dead_frames[0][self.dead_spr]
                else:
                    self.image = self.dead_frames[1][self.dead_spr]
                self.dead_spr += 1
        prev_bot_cent = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = prev_bot_cent
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, player):
        if self.dead:
            self.cur_sprite_attack = 0
            pass

        else:
            rast_x = self.rect.centerx - player.rect.centerx
            rast_y = self.rect.centery - player.rect.centery
            self.can_move = True
            self.Attack = False

            if abs(rast_x) <= 50 and abs(rast_y) <= 50:
                if rast_x <= 0 and self.Right:
                    self.can_move = False
                    self.Attack = True

                elif rast_x >= 0 and self.Left:
                    self.can_move = False
                    self.Attack = True

            if self.can_move:
                self.Attack = False

                if self.Right:
                    self.rect = self.rect.move(-(-self.speed_x // FPS), 0)
                    if pygame.sprite.spritecollideany(self, tiles_group):
                        self.rect = self.rect.move(-self.speed_x // FPS, 0)
                        self.Right = False
                        self.Left = True

                elif self.Left:
                    self.rect = self.rect.move(-self.speed_x // FPS, 0)
                    if pygame.sprite.spritecollideany(self, tiles_group):
                        self.rect = self.rect.move(-(-self.speed_x // FPS), 0)
                        self.Right = True
                        self.Left = False

                self.rect = self.rect.move(0, self.speed_y)
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect = self.rect.move(0, -self.speed_y)
                    if self.speed_y < 0:
                        self.speed_y = 0
                self.speed_y += GRAVITY
                if self.speed_y > 5:
                    self.speed_y = 5


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, long=1):
        super().__init__(tiles_group, all_sprite)
        self.image = pygame.transform.smoothscale(
            tile_images[tile_type], (tile_width * long, tile_height))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj, player):
        if obj in player_group:
            if player.Attack and (player.cur_sprite_attack > 12 and player.cur_sprite_attack < 17):
                x, y = obj.rect.center
                if player.last_direct == RIGHT:
                    x += 1
                    obj.rect.center = (x, y)
                else:
                    x -= 1
                    obj.rect.center = (x, y)
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, width, height):
        x, y = target.rect.midbottom
        self.dx = -(x - width // 2)
        self.dy = -(y - tile_height // 2 - height // 2)