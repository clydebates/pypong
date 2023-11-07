import pygame, asyncio
from sys import exit
import random

pygame.init()
pygame.display.set_caption('PyPong')

def show_score():
    score_surf = game.default_font.render(f'{game.player_score} - {game.opponent_score}', False, 'White')
    score_rect = score_surf.get_rect(center = (game.screen_x/2,30))
    game.screen.blit(score_surf, score_rect)

def add_score():
    if game.ball_rect.right <= 0:
        # print('opponent scores')
        game.opponent_score += 1
    if game.ball_rect.left >= game.screen_x:
        # print('player scores')
        game.player_score += 1
    #reset ball to center
    game.ball_rect.center = (game.screen_x/2,game.screen_y/2)
    #randomize starting direction
    game.ball_speed_x *= random.choice((1,-1))
    game.ball_speed_y *= random.choice((1, -1))

def opponent_ai():
    # global opponent_speed
    if game.ball_rect.top <= game.opponent_rect.bottom - 200:
        game.opponent_rect.top -= game.opponent_speed
    if game.ball_rect.bottom >= game.opponent_rect.top + 200:
        game.opponent_rect.top += game.opponent_speed
    # keep opponent on screen
    if game.opponent_rect.bottom >= game.screen_y:
        game.opponent_rect.bottom = game.screen_y
        game.opponent_speed = 0
    if game.opponent_rect.top <= 0:
        game.opponent_rect.top = 0
        game.opponent_speed = 0

def ball_animation():
    game.ball_rect.y += game.ball_speed_y
    game.ball_rect.x += game.ball_speed_x
    # keep ball on screen
    if game.ball_rect.bottom >= game.screen_y or game.ball_rect.top <= 0:
        game.ball_speed_y = -game.ball_speed_y
    # collision detection
    if game.ball_rect.colliderect(game.player_rect) or game.ball_rect.colliderect(game.opponent_rect):
        game.ball_speed_x = -game.ball_speed_x

def player_animation():
    # global player_speed, screen_x, screen_y
    # move player
    game.player_rect.y += game.player_speed
    # keep player on screen
    if game.player_rect.bottom >= game.screen_y:
        game.player_rect.bottom = game.screen_y
        game.player_speed = 0
    if game.player_rect.top <= 0:
        game.player_rect.top = 0
        game.player_speed = 0

def draw_shapes():
    pygame.draw.rect(game.screen, 'White', game.player_rect)
    pygame.draw.rect(game.screen, 'White', game.opponent_rect)
    pygame.draw.ellipse(game.screen, 'White', game.ball_rect)
    pygame.draw.aaline(game.screen, 'White', (game.screen_x / 2, 0), (game.screen_x / 2, game.screen_y))
class GAME:
    def __init__(self) -> None:
        self.screen_x = 1280
        self.screen_y = 900
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.framerate_clock = pygame.time.Clock()
        self.game_active = False
        self.score = 0
        self.player_rect = pygame.Rect(10, self.screen_y / 2 - 70, 10, 140)
        self.player_speed = 0
        self.opponent_rect = pygame.Rect(self.screen_x - 20, self.screen_y / 2 - 70, 10, 140)
        self.opponent_speed = 7
        self.ball_rect = pygame.Rect(self.screen_x / 2 - 15, self.screen_y / 2 - 15, 30, 30)
        self.ball_speed_x = 7
        self.ball_speed_y = 7
        self.default_font = pygame.font.Font(None, 50)
        self.opponent_score = 0
        self.player_score = 0
        self.bg_color = pygame.Color('grey12')
game = GAME()

async def main():
  while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              exit()
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_DOWN:
                  game.player_speed += 7
              if event.key == pygame.K_UP:
                  game.player_speed -= 7
          if event.type == pygame.KEYUP:
              game.player_speed = 0

      game.screen.fill(game.bg_color) # this is SUPER important, because it overwrites old drawings

      opponent_ai()
      player_animation()
      ball_animation()
      show_score()

      if game.ball_rect.right <= 0 or game.ball_rect.left >= game.screen_x:
          add_score()

      draw_shapes()
      pygame.display.update()
      game.framerate_clock.tick(60)
      await asyncio.sleep(0)
asyncio.run(main())