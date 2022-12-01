import pygame
import os
import time
import random
import math

pygame.font.init()

WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('BACKGROUND.png')), (WIDTH, HEIGHT))
FPS = 60

MENU_FONT = pygame.font.SysFont('arial', 40)
MAIN_FONT = pygame.font.SysFont('arial', 40)
GROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join('GROUND.png')), (WIDTH, 650))
L_PLATFORM_IMG = pygame.transform.scale(pygame.image.load(os.path.join('L_PLATFORM.png')), (200, 200))
PLATFORM_IMG = pygame.transform.scale(pygame.image.load(os.path.join('PLATFORM_IMG.png')), (400, 200))
PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('CHICKEN.png')), (200, 200))
BABY_COYOTE_IMG = pygame.transform.scale(pygame.image.load(os.path.join('FOX.png')), (100, 100))
FARMER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('FARMER.png')), (150, 150))
EGG_IMG = pygame.transform.scale(pygame.image.load(os.path.join('EGG.png')), (50, 50))
FIREBALL_IMG = pygame.transform.scale(pygame.image.load(os.path.join('FIREBALL.png')), (100, 100))
BULLET_IMG = pygame.transform.scale(pygame.image.load(os.path.join('BULLET.png')), (200, 200))
# DASH_IMG = pygame.transform.scale(pygame.image.load(os.path.join('DASH2.png')), (200, 200))
GRAVITY = 9
FIREBALL_SPEED = 15
PLAYER_VEL = 15
PLATFORM_VEL = 5
COYOTE_VEL = 5
FARMER_VEL = 5
BULLET_VEL = 20
JUMP_VEL = 20

main_menu = True
lost = False

class Platform:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


class Player:

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.jump_time = 0

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def jump(self):
        if pygame.time.get_ticks() > self.jump_time + 100 and self.y >= 600:
            self.jump_time = pygame.time.get_ticks()
            self.y -= 150





class Egg:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

class Fireball:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

class Enemy:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()
    player_direction = 'right'
    egg_count = 0
    dash_time = 0
    player = Player(200, 600, PLAYER_IMG)
    platforms = []
    eggs = []
    coyotes = []
    fireballs = []
    farmers = []
    counter = 0
    def loss_screen():
        final_score = egg_count
        WIN.blit(BACKGROUND,(0,0))
        lost_label = MENU_FONT.render('GAME OVER',1,(0,0,0))
        lost_label_2 = MENU_FONT.render( 'Press SPACE to Play Again',1,(0,0,0))
        final_score_label = MENU_FONT.render(f"You Collected {final_score} Eggs",1,(0,0,0))
        WIN.blit(lost_label, (475, 200))
        WIN.blit(lost_label_2, (360, 400))
        WIN.blit(final_score_label, (400, 300))
        pygame.display.update()
    def menu():
        WIN.blit(BACKGROUND, (0, 0))
        menu_label_1 = MENU_FONT.render('Use "a" and "d" to move and "SPACE" to jump',1,(0,0,0))
        menu_label_2 = MENU_FONT.render('Collect as Many Eggs as You Can',1,(0,0,0))
        menu_label_3 = MENU_FONT.render('Press "SPACE" to Start', 1, (0,0,0))
        WIN.blit(menu_label_1, (230, 200))
        WIN.blit(menu_label_2, (305, 300))
        WIN.blit(menu_label_3, (390, 400))
        pygame.display.update()
    def gravity():
        for egg in eggs:
            egg.y += GRAVITY
        if player.y < 600:
            player.y += GRAVITY

    def collide(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    def create_plats():
        while len(platforms) <= 5:
            platform = Platform(1100, 50, PLATFORM_IMG)
            platforms.append(platform)
    def create_fireballs():
        if len(fireballs) < 4:
            fireball_x = random.randrange(0, WIDTH)
            fireball = Fireball(fireball_x, 0, FIREBALL_IMG)
            fireballs.append(fireball)
        for fireball in fireballs:
            if fireball.y > 700:
                fireballs.remove(fireball)
    def create_eggs():
        if len(eggs) < 1:
            egg_x = random.randrange(0, WIDTH)
            egg = Egg(egg_x, 0, EGG_IMG)
            eggs.append(egg)
        for egg in eggs:
            if egg.y > HEIGHT:
                eggs.remove(egg)

    def create_farmers():
        if len(farmers) < 1:
            farmer = Enemy(-20, 580, FARMER_IMG)
            farmers.append(farmer)
        for farmer in farmers:
            if farmer.x > 1200:
                farmers.remove(farmer)
    def create_coyotes():
        if len(coyotes) < 1:
            coyote = Enemy(1250, 600, BABY_COYOTE_IMG)
            coyotes.append(coyote)
        for coyote in coyotes:
            if coyote.x == -70:
                coyotes.remove(coyote)

    def drop_fireballs():
        for fireball in fireballs:
            fireball.y += FIREBALL_SPEED

    def move_coyotes():
        for coyote in coyotes:
            coyote.x -= COYOTE_VEL

    def move_farmers():
        for farmer in farmers:
            farmer.x += FARMER_VEL


    def controls():
        keys = pygame.key.get_pressed()


        if keys[pygame.K_a]:  # left
            player_direction = 'left'
            player.x -= PLAYER_VEL
        if keys[pygame.K_d]:  # right
            player_direction = 'right'
            player.x += PLAYER_VEL
        if keys[pygame.K_SPACE]:
            global main_menu
            if main_menu == True:
                main_menu = False
            global lost
            if lost == True:
                lost = False
                main()
            else:
                player.jump()

    def draw_window():

        WIN.blit(BACKGROUND, (0, 0))
        WIN.blit(GROUND_IMG, (0, 70))
        egg_label = MAIN_FONT.render(f'Eggs Collected:{egg_count}', 1, (0,0,0))
        WIN.blit(egg_label, (50, 50))

        for egg in eggs:
            egg.draw(WIN)
        for coyote in coyotes:
            coyote.draw(WIN)
        for fireball in fireballs:
            fireball.draw(WIN)
        for farmer in farmers:
            farmer.draw(WIN)

        # if pygame.time.get_ticks() > dash_time and pygame.time.get_ticks() < dash_time + 300 and dash_time > 0:
        #     if player_direction == 'left':
        #         WIN.blit(DASH_IMG, (player.x + 50, player.y - 50))
        #     if player_direction == 'right':
        #         WIN.blit(DASH_IMG, (player.x - 50, player.y - 50))
        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        counter += 1
        controls()
        if main_menu == True:
            menu()
        elif main_menu == False:
            global lost
            if lost == True:
                loss_screen()
            elif lost == False:
                create_farmers()
                create_fireballs()
                create_coyotes()
                create_eggs()
                draw_window()
                gravity()
                move_farmers()
                drop_fireballs()
                move_coyotes()



        for egg in eggs:
            if collide(egg, player):
                egg_count += 1
                eggs.remove(egg)
        for coyote in coyotes:
            if collide(coyote, player):
                lost = True

        for fireball in fireballs:
            if collide(fireball, player):
                lost = True

        for farmer in farmers:
            if collide(farmer, player):
                lost = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


if __name__ == '__main__':
    main()
