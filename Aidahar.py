import pygame, random

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Aidahardy Tamaqtandyru")

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)

# variables
BUFFER_DISTANCE = 100
HEADER_HEIGHT = 80
PLAYER_STARTING_SCORE = 0
PLAYER_STARTING_LIVE = 5
BIRD_STARTING_VELOCITY = 5

player_score = PLAYER_STARTING_SCORE
player_live = PLAYER_STARTING_LIVE
bird_velocity = BIRD_STARTING_VELOCITY
acceleration = 0.5
dragon_velocity = 5

# sounds & musics
pygame.mixer.music.load('music.wav')
sound1 = pygame.mixer.Sound('sound_1.wav')
sound2 = pygame.mixer.Sound('sound_2.wav')
sound2.set_volume(0.2)

# images
background_image = pygame.image.load("background.png")

dragon_image = pygame.image.load('dragon.png').convert_alpha()
dragon_image = pygame.transform.rotate(dragon_image, 90)
dragon_rect = dragon_image.get_rect()
dragon_rect.center = (80, WINDOW_HEIGHT//2)

bird_image = pygame.image.load('bird.png').convert_alpha()
bird_rect = bird_image.get_rect()
bird_rect.centerx = WINDOW_WIDTH + BUFFER_DISTANCE
bird_rect.centery = random.randint(HEADER_HEIGHT+25, WINDOW_HEIGHT-25)

score_background = pygame.image.load('score_background.png').convert_alpha()
score_background_rect = score_background.get_rect()
score_background_rect.x = 10
score_background_rect.y = 10

live_background = pygame.image.load('score_background.png').convert_alpha()
live_background_rect = score_background.get_rect()
live_background_rect.x = WINDOW_WIDTH-(live_background_rect.width+10)
live_background_rect.y = 10

# font & texts
main_font = pygame.font.Font('AttackGraffiti.ttf', 32)

score_text = main_font.render("Upai: " + str(player_score), True, GREEN)
score_rect = score_text.get_rect()
score_rect.x = score_background_rect.x+10
score_rect.y = score_background_rect.y+10

game_name = main_font.render("Aidahardy tamaqtandyru", True, RED, WHITE)
game_name_rect = game_name.get_rect()
game_name_rect.centerx = WINDOW_WIDTH//2
game_name_rect.centery = HEADER_HEIGHT//2

live_text = main_font.render("Jany: " + str(player_live), True, GREEN)
live_rect = live_text.get_rect()
live_rect.x = live_background_rect.x + 10
live_rect.y = live_background_rect.y + 10

game_over_text = main_font.render("GAMEOVER", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

game_continue_text = main_font.render("press any key", True, GREEN)
game_continue_rect = game_continue_text.get_rect()
game_continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2+100)

FPS = 60
clock = pygame.time.Clock()

pygame.mixer.music.play(-1, 0.0)
fl_pause = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # dragon moves
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and dragon_rect.top > HEADER_HEIGHT:
        dragon_rect.y -= dragon_velocity
    elif keys[pygame.K_DOWN] and dragon_rect.bottom < WINDOW_HEIGHT:
        dragon_rect.y += dragon_velocity

    # bird moves
    bird_rect.x -= bird_velocity
    if bird_rect.x < -10:
        bird_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        bird_rect.centery = random.randint(HEADER_HEIGHT+25, WINDOW_HEIGHT-25)
        sound2.play()
        player_live -= 1

    if dragon_rect.colliderect(bird_rect):
        bird_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        bird_rect.centery = random.randint(HEADER_HEIGHT+25, WINDOW_HEIGHT-25)
        sound1.play()
        player_score += 1
        bird_velocity += acceleration

    if player_live == 0:
        fl_pause = True
        pygame.mixer.music.stop()
        live_text = main_font.render("Jany: " + str(player_live), True, GREEN)
        display_surface.blit(live_text, live_rect)
        pygame.display.update()
        while fl_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    fl_pause = False
                elif event.type == pygame.KEYDOWN:
                    fl_pause = False
                    player_live = PLAYER_STARTING_LIVE
                    player_score = PLAYER_STARTING_SCORE
                    bird_velocity = BIRD_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)

            display_surface.blit(game_over_text, game_over_rect)
            display_surface.blit(game_continue_text, game_continue_rect)
            pygame.display.update()


    
    display_surface.blit(background_image, (0,0))
    display_surface.blit(dragon_image, dragon_rect)
    display_surface.blit(bird_image, bird_rect)
    display_surface.blit(score_background, score_background_rect)
    display_surface.blit(game_name, game_name_rect)
    display_surface.blit(live_background, live_background_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(live_text, live_rect)
    pygame.draw.line(display_surface, WHITE, (0, HEADER_HEIGHT), (WINDOW_WIDTH, HEADER_HEIGHT), 5)
    
    score_text = main_font.render("Upai: " + str(player_score), True, GREEN)
    live_text = main_font.render("Jany: " + str(player_live), True, GREEN)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()