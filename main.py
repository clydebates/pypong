import pygame
from sys import exit
import random

pygame.init()
pygame.display.set_caption('PyPong')

def show_score():
    global player_score, opponent_score, screen
    score_surf = default_font.render(f'{player_score} - {opponent_score}', False, 'White')
    score_rect = score_surf.get_rect(center = (screen_x/2,30))
    screen.blit(score_surf, score_rect)

def add_score():
    global opponent_score, player_score, ball_speed_x, ball_speed_y
    if ball_rect.right <= 0:
        # print('opponent scores')
        opponent_score += 1
    if ball_rect.left >= screen_x:
        # print('player scores')
        player_score += 1
    #reset ball to center
    ball_rect.center = (screen_x/2,screen_y/2)
    #randomize starting direction
    ball_speed_x *= random.choice((1,-1))
    ball_speed_y *= random.choice((1, -1))

def opponent_ai():
    global opponent_speed
    if ball_rect.top <= opponent_rect.bottom - 200:
        opponent_rect.top -= opponent_speed
    if ball_rect.bottom >= opponent_rect.top + 200:
        opponent_rect.top += opponent_speed
    # keep opponent on screen
    if opponent_rect.bottom >= screen_y:
        opponent_rect.bottom = screen_y
        opponent_speed = 0
    if opponent_rect.top <= 0:
        opponent_rect.top = 0
        opponent_speed = 0

def ball_animation():
    global ball_speed_x, ball_speed_y
    ball_rect.y += ball_speed_y
    ball_rect.x += ball_speed_x
    # keep ball on screen
    if ball_rect.bottom >= screen_y or ball_rect.top <= 0:
        ball_speed_y = -ball_speed_y
    # collision detection
    if ball_rect.colliderect(player_rect) or ball_rect.colliderect(opponent_rect):
        ball_speed_x = -ball_speed_x

def player_animation():
    global player_speed, screen_x, screen_y
    # move player
    player_rect.y += player_speed
    # keep player on screen
    if player_rect.bottom >= screen_y:
        player_rect.bottom = screen_y
        player_speed = 0
    if player_rect.top <= 0:
        player_rect.top = 0
        player_speed = 0

def draw_shapes():
    pygame.draw.rect(screen, 'White', player_rect)
    pygame.draw.rect(screen, 'White', opponent_rect)
    pygame.draw.ellipse(screen, 'White', ball_rect)
    pygame.draw.aaline(screen, 'White', (screen_x / 2, 0), (screen_x / 2, screen_y))

screen_x = 1280
screen_y = 900
screen = pygame.display.set_mode((screen_x, screen_y))

framerate_clock = pygame.time.Clock()
game_active = False
score = 0

player_rect = pygame.Rect(10, screen_y / 2 - 70, 10, 140)
player_speed = 0
opponent_rect = pygame.Rect(screen_x - 20, screen_y / 2 - 70, 10, 140)
opponent_speed = 7
ball_rect = pygame.Rect(screen_x / 2 - 15, screen_y / 2 - 15, 30, 30)
ball_speed_x = 7
ball_speed_y = 7

default_font = pygame.font.Font(None, 50)
opponent_score = 0
player_score = 0

bg_color = pygame.Color('grey12')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            player_speed = 0

    screen.fill(bg_color) # this is SUPER important, because it overwrites old drawings

    opponent_ai()
    player_animation()
    ball_animation()
    show_score()

    if ball_rect.right <= 0 or ball_rect.left >= screen_x:
        add_score()

    draw_shapes()
    pygame.display.update()
    framerate_clock.tick(60)