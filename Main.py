
import pygame
import sys


pygame.init()

size = width, height = 800, 600

Display = pygame.display.set_mode(size)

from Classes import bakcground_group, player_group, tiles_group, all_sprite, enemy_group, FPS
from Classes import load_image, UP, LEFT, RIGHT, ATTACK
from Classes import Tile, Player, Skelet, Camera


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filname):
    filname = 'data/levels/' + filname
    with open(filname, 'r') as MapFile:
        level_map = [line.strip() for line in MapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    spr_2_long = 1

    for y in range(len(level)):
        for x in range(len(level[y])):
            if spr_2_long != 1:
                spr_2_long -= 1
                continue
            if level[y][x] == '#':
                if x != len(level[y]) - 1:
                    if level[y][x + 1] == '#':
                        spr_2_long += 1
                        for z in range(x + 2, len(level[y])):
                            if level[y][z] == '#':
                                spr_2_long += 1
                                if spr_2_long == 7:
                                    break
                            else:
                                break
                Tile('long', x, y, spr_2_long)

            elif level[y][x] == '@':
                new_player = Player(x, y - 1)

            elif level[y][x] == 's':
                Skelet(x, y)

    return new_player, x, y




Clock = pygame.time.Clock()
camera = Camera()
for i in range(5):
        back_sprit = pygame.sprite.Sprite(bakcground_group)
        back_sprit.image = pygame.transform.scale(
            load_image(f'plx-{i}.png'), size)
        back_sprit.rect = back_sprit.image.get_rect()
        back_sprit.rect.x = 0
        back_sprit.rect.y = 0


levels = [1, 2, 3]
zumbs = []
Is_game_on = False
Time_count = 0
Is_menu_on = True
scroll = 0

color_gr = pygame.Color(0, 179, 0)
color_bl = pygame.Color(0, 0, 0)

font = pygame.font.Font(None, 150)
while Is_menu_on:
    Display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:  # скролл в право
                if scroll >= -500:
                    scroll -= 100

            elif event.button == 5:  # скролл в лево:
                if scroll <= 200:
                    scroll += 100

            else:
                x_y = event.pos
                for el in zumbs:
                    if el.collidepoint(x_y):
                        level_num = zumbs.index(el) + 1
                        Is_game_on = True
                        break
        elif event.type == pygame.QUIT:
            terminate()
    bakcground_group.draw(Display)
    zumbs.clear()
    for el in levels:
        x, y = (width // 2 - 50) * el + scroll, height // 2 - 50
        text = font.render(f'{el}', 1, color_bl)
        rectt = pygame.draw.rect(Display, color_gr, (x, y, 100, 100), 0)
        zumbs.append(rectt)
        Display.blit(text, (x + 25, y + 5))

    pygame.display.flip()
    if Is_game_on:
        player_group.empty()
        tiles_group.empty()
        all_sprite.empty() 
        enemy_group.empty()
        player, level_x, level_y = generate_level(load_level(f'level_{level_num}.txt'))
        need_deads = len(enemy_group)
        time_to_understand = 0
        while Is_game_on:
            if player.DEAD == True:
                Is_game_on = False
            Display.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Is_game_on = False
                    index = [index for index, value in enumerate(
                        pygame.key.get_pressed()) if value == 1]
                    player.action_on(*index)

                elif event.type == pygame.KEYUP:
                    up_keys = []
                    if event.key == UP:
                        up_keys.append(UP)
                    if event.key == LEFT:
                        up_keys.append(LEFT)
                    elif event.key == RIGHT:
                        up_keys.append(RIGHT)
                    if event.key == ATTACK:
                        up_keys.append(ATTACK)
                    player.action_Off(*up_keys)
            if Time_count >= 70:
                Time_count = 0
                player.animation()
                for el in enemy_group:
                    el.animation()
            player_group.update()
            enemy_group.update(player)
            bakcground_group.draw(Display)
            all_sprite.draw(Display)
            pygame.display.flip()
            camera.update(player, width, height)
            for el in all_sprite:
                camera.apply(el, player)
            deads = 0
            for el in enemy_group:
                if el.dead:
                    deads += 1
                    if deads == need_deads:
                        time_to_understand += Time_count
                        if time_to_understand >= 10**4:
                            Is_game_on = False

            Time_count += Clock.tick(FPS)
