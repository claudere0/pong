import pygame, sys, random
from settings import WIDTH, HEIGHT
pygame.init()

class Ball:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
        self.dx = 4 * random.choice((1, -1))
        self.dy = 4 * random.choice((1, -1))
        self.bounce_multiplier = 1
        self.spawn_x = x
        self.spawn_y = y

    def update(self):
        self.rect.x += self.dx * self.bounce_multiplier
        self.rect.y += self.dy * self.bounce_multiplier

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

    def bounce(self):
        self.dx *= -1
        self.bounce_multiplier += 0.0625

    def goal(self):
        if self.rect.left <= 0:
            return "player"
        if self.rect.right >= WIDTH:
            return "simple_ai"

        return None

    def reset(self):
        self.rect.x, self.rect.y = self.spawn_x, self.spawn_y
        self.dx = 4 * random.choice((1, -1))
        self.dy = 4 * random.choice((1, -1))
        self.bounce_multiplier = 1

    def draw(self, screen):
        pygame.draw.ellipse(screen, 'white', self.rect)

class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, WIDTH//32, HEIGHT//6)
        self.speed = 4
        self.color = color

    def update(self):
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move_up(self):
        self.rect.y -= self.speed
    
    def move_down(self):
        self.rect.y += self.speed

class Game:
    def __init__(self):
        BALL_SIZE = 16
        self.FPS = 60

        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.ball = Ball((WIDTH-BALL_SIZE)//2, (HEIGHT-BALL_SIZE)//2,BALL_SIZE, BALL_SIZE)
        self.player = Paddle(WIDTH-(WIDTH//16),(HEIGHT-(HEIGHT//6))//2, (0,0,255))
        self.enemy = Paddle(WIDTH//32,(HEIGHT-(HEIGHT//6))//2, (255,0,0))
        self.player_score = 0
        self.simple_ai_score = 0
        self.running = True
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pygame.draw.rect(self.screen, 'white', (0,0, WIDTH, HEIGHT))
        if keys[pygame.K_UP]:
            self.player.move_up()
        if keys[pygame.K_DOWN]:
            self.player.move_down()

    def update(self):
        self.ball.update()
        self.player.update()

        if self.enemy.rect.centery > self.ball.rect.centery:
            self.enemy.move_up()
        else:
            self.enemy.move_down()
        
        self.enemy.update()

        if self.ball.goal() == 'player':
            self.player_score += 1
            self.ball.reset()
        if self.ball.goal() == 'simple_ai':
            self.simple_ai_score += 1
            self.ball.reset()

        if self.player_score == 5:
            print('player wins')
            self.running = False

        if self.simple_ai_score == 5:
            print('player lost')
            self.running = False

    def collisions(self):
        if self.ball.rect.colliderect(self.player.rect):
            self.ball.bounce()
        if self.ball.rect.colliderect(self.enemy.rect):
            self.ball.bounce()

    def draw(self):
        self.ball.draw(self.screen)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        player_text = self.font.render(str(self.player_score), False, (255, 255, 255))
        enemy_text = self.font.render(str(self.simple_ai_score), False, (255, 255, 255))
        self.screen.blit(player_text, (WIDTH // 2 + 16, 16))
        self.screen.blit(enemy_text, (WIDTH // 2 - 32, 16))
        pygame.display.flip()

    def run(self):
        while self.running:
            # time
            dt = self.clock.tick(self.FPS)/1000
            self.screen.fill('black')

            self.events()
            self.input()
            self.update()
            self.collisions()
            self.draw()
    
        pygame.quit()
        sys.exit()

game = Game()

game.run()

pygame.quit()
sys.exit()
