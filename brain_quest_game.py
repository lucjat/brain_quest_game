import pygame
from level_data import *

# Game made using the pygame library
# This is the main file that will run the game
# Icons made by Freepik from www.flaticon.com
# https://www.flaticon.com/free-icon/brain_3743319
# Assets from https://www.kenney.nl/assets

# Initializations
pygame.init()
clock = pygame.time.Clock()

# Game window
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('BrainQuest Game')

# Global variables
tile_size = 50
fps = 60

# Game states
MAIN_MENU = 0
LEVEL_1 = 1
FUN_FACT_1 = 2
LEVEL_2 = 3
FUN_FACT_2 = 4
TRANSITION_TO_LEVEL_2 = 5
END_GAME = 6

current_state = MAIN_MENU

# Image paths
bg_img = pygame.image.load('img/windows/bckg.png')
main_menu_img = pygame.image.load('img/windows/menu.png')
fun_fact_img = pygame.image.load('img/windows/ff1.png')    # Add the path to your fun fact image
end_game_img = pygame.image.load('img/windows/end.png')

WHITE = (255, 255, 255)

exit_group = pygame.sprite.Group()


# For checking the correct grid
def make_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, WHITE, (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, WHITE, (line * tile_size, 0), (line * tile_size, screen_height))


def reset_level():
    player.reset(100, screen_height - 130)
    exit_group.empty()


class Level:
    def __init__(self, data):
        self.tile_list = []
        tile_img = pygame.image.load('img/assets/tile.png')
        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(tile_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 9:
                    exit_level = Exit(column_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit_level)
                column_count += 1
            row_count += 1

    def draw_level(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    # This function will update the player's position
    def update(self, current_level):
        global current_state
        dx = 0
        dy = 0

        # This will check if the player is pressing the arrow keys
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped is False:
            self.vel_y = -10
            self.jumped = True
        if key[pygame.K_SPACE] is False:
            self.jumped = False
        if key[pygame.K_a]:
            dx -= 3
        if key[pygame.K_d]:
            dx += 3

        # This will add gravity to the player
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        # This will check if the player is colliding with the tiles
        self.in_air = True
        for tile in current_level.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        if pygame.sprite.spritecollide(self, exit_group, False):
            if current_state == LEVEL_1:
                reset_level()
                current_state = FUN_FACT_1
            elif current_state == LEVEL_2:
                current_state = END_GAME

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)    # Uncomment this line to see the player's hitbox

    def reset(self, x, y):
        img = pygame.image.load('img/assets/brain_character.png')
        self.image = pygame.transform.scale(img, (45, 45))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False

        if pygame.sprite.spritecollide(self, exit_group, False):
            pass
            #if current_state == LEVEL_1:
                #reset_level()
                #current_state = TRANSITION_TO_LEVEL_2
            #elif current_state == LEVEL_2:
                #current_state = END_GAME


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/assets/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(100, screen_height - 130)

run = True
while run:
    clock.tick(fps)
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if current_state == MAIN_MENU:
        screen.blit(main_menu_img, (0, 0))
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            current_state = LEVEL_1
            reset_level()
            level1 = Level(level1_data)

    elif current_state == LEVEL_1:
        level1.draw_level()
        player.update(level1)    # Pass the current level to player.update

    elif current_state == FUN_FACT_1:
        screen.blit(fun_fact_img, (0, 0))
        key = pygame.key.get_pressed()

        if key[pygame.K_RETURN]:
            current_state = LEVEL_2
            reset_level()
            level2 = Level(level2_data)

    elif current_state == LEVEL_2:
        level2.draw_level()
        player.update(level2)    # Pass the current level to player.update

    elif current_state == END_GAME:
        screen.blit(end_game_img, (0, 0))
        key = pygame.key.get_pressed()

        if key[pygame.K_RETURN]:
            current_state = MAIN_MENU

    exit_group.draw(screen)

    pygame.display.update()

pygame.quit()
