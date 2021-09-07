import pygame.draw
import os
from random import randint
from sys import exit

pygame.init()

def score(obsicale_score):
    if obsicale_score:
        for obsicale_score_rect in obsicale_score:
            obsicale_score_rect.x -= 5

            pygame.draw.rect(screen, (0, 0, 0), (600, 50, 5, 400))


def obsticale_movment(obsticale_list):
    if obsticale_list:
        for obsticale_rect in obsticale_list:
            obsticale_rect.x -= 5

            screen.blit(snail_img, obsticale_rect)
        obsticale_list = [obsticale for obsticale in obsticale_list if obsticale.x > -100]
        return obsticale_list
    else:
        return []


def collisions(player, obsticales):
    if obsticales:
        for obsticale_rect in obsticales:
            if player.colliderect(obsticale_rect):
                return False
    return True


# Screen Variables
screen_width = 800
screen_height = 400
display_surface_height = 200
display_serface_width = 100

# OS file loading/importing images(Without this i cant load files its kinda dumb but ya know)
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
sky_img = os.path.join(sourceFileDir, "PygameGraphics/Sky.png")
ground_img = os.path.join(sourceFileDir, "PygameGraphics/ground.png")
font_txt = os.path.join(sourceFileDir, "PygameGraphics/Font/Pixeltype.ttf")
snail_enemy_img = os.path.join(sourceFileDir, "PygameGraphics/Snail/snail1.png")
player_img = os.path.join(sourceFileDir, "PygameGraphics/Player_Charicter/player_stand.png")
player_walk_img = os.path.join(sourceFileDir, "PygameGraphics/Player_Charicter/player_walk_1.png")

# Acual game variables
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jumper Man")
timer = pygame.time.Clock()
font = pygame.font.Font(font_txt, 50)
game_active = False
player_gravity = 0
count = 0

# Screen/Surface rendering stuff
# Centering the Score Text with rectangles
score_img = font.render('Score: ' + str(count), False, (64, 64, 64))
score_rect = score_img.get_rect(center=(400, 50))
start_btn_img = font.render('Press Space To Start', False, (64, 64, 64))
start_btn_rect = score_img.get_rect(center=(320, 350))

# Terrain stuff
sky_surface = pygame.image.load(sky_img).convert_alpha()
ground_surface = pygame.image.load(ground_img).convert_alpha()

# Drawing a rectangle around the snail
snail_img = pygame.image.load(snail_enemy_img).convert_alpha()
# snail_rect = snail_img.get_rect(midbottom=(600, 300))
snail_rect_score = pygame.draw.rect(screen, (0, 255, 0), (100, 50, 5, 400))

obstical_rect_list = []

# Drawing a rectangle around the player
player_walking_img = pygame.image.load(player_walk_img).convert_alpha()
player_rect = player_walking_img.get_rect(midbottom=(80, 300))

player_stand = pygame.image.load(player_img).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Timer
obsticle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obsticle_timer, 1500)

# rotate_img = pygame.transform.rotate(player_img, 180)

run = True
# game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # makeing the player jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and player_rect.right <= 800:
                player_rect.x += 50
            if event.key == pygame.K_LEFT and player_rect.left >= 0:
                player_rect.x += -50
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                game_active = True
                player_gravity = -20

        if event.type == obsticle_timer and game_active:
            obstical_rect_list.append(snail_img.get_rect(midbottom=(randint(900, 1100), 300)))
            snail_rect_score = pygame.draw.rect(screen, (0, 0, 0), (20, 50, 800, 800))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        pygame.draw.rect(screen, '#c0e8ec', score_rect)
        pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        screen.blit(score_img, score_rect)
        ######################################################
        #pygame.draw.rect(screen, 'Blue', snail_rect, 10)
        #pygame.draw.rect(screen, 'Red', snail_rect_score, 10)
        # pygame.draw.rect(screen, 'Green', player_rect, 10)
        ######################################################

        # player gravity
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_walking_img, player_rect)

        obstical_rect_list = obsticale_movment(obstical_rect_list)
        # snail_score = score(snail_rect_score)

        game_active = collisions(player_rect, obstical_rect_list)
        # Making the snail enemy move from the right to the left
        # snail_rect.x -= 4
        # snail_rect_score.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        #     # resetting the score box
        #     snail_rect_score = pygame.draw.rect(screen, (0, 0, 0), (600, 50, 5, 400))
        #     snail_rect_score.left = snail_rect.left + 40
        # if snail_rect_score.right <= 0:
        #     snail_rect_score.left = snail_rect.left + 40
        # screen.blit(snail_img, snail_rect)

        # getting a score
        if player_rect.colliderect(snail_rect_score):
            score_img = font.render('Score: ' + str(count + 1), True, (64, 64, 64))
            count += 1
            snail_rect_score = pygame.draw.rect(screen, (0, 255, 0), (0, 0, 0, 0))
            print(count)

        # restaring the game when the player hits the snail
    # if snail_rect.colliderect(player_rect):
    # game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(start_btn_img, start_btn_rect)
        screen.blit(score_img, score_rect)
        screen.blit(player_stand, player_stand_rect)
    # Updating the game screen
    pygame.display.update()
    # Frame rate
    timer.tick(60)
