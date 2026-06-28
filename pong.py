import pygame, sys, random
pygame.init()

WIDTH = 512
HEIGHT = 384
FPS = 60

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pong")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
player_score = 0
simple_ai_score = 0

BALL_SIZE = 16

class Ball:
    def __init__(self, x, y, width, height,):
        self.rect = pygame.Rect(x,y,width,height)
        self.dx = 4 * random.choice((1, -1))
        self.dy = 4 * random.choice((1, -1))
        self.bounce_multiplier = 1

    def update(self):
        self.rect.x += self.dx * self.bounce_multiplier
        self.rect.y += self.dy * self.bounce_multiplier

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

        # if self.rect.left <= 0 or self.rect.right >= WIDTH:
        #     self.dx *= -1

    def collisions(self, player, simple_ai):
        if self.rect.colliderect(player.rect) or self.rect.colliderect(simple_ai.rect):
            self.dx *= -1
            self.bounce_multiplier += 0.0625
        

    def round_result(self):
        if self.rect.left <= 0:
            return "player"
        if self.rect.right >= WIDTH:
            return "simple_ai"
        
        return None
    
    def reset(self, x, y):
        self.rect.x, self.rect.y = x, y
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

    def move(self, direction):
        if direction == 'up' and self.rect.top > 0:
            self.rect.y -= self.speed
        if direction == 'down' and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def simple_ai(self, ball):
        if self.rect.centery < ball.rect.centery:
            self.move('down')
        if self.rect.centery > ball.rect.centery:
            self.move('up')
    
    def score_count(self, point):
        pass



ball = Ball((WIDTH-BALL_SIZE)//2, (HEIGHT-BALL_SIZE)//2,BALL_SIZE, BALL_SIZE)
player = Paddle(WIDTH-(WIDTH//16),(HEIGHT-(HEIGHT//6))//2, (0,0,255))
enemy = Paddle(WIDTH//32,(HEIGHT-(HEIGHT//6))//2, (255,0,0))

running = True
while running:
    # time
    dt = clock.tick(FPS)/1000
    screen.fill('black')

    # event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pygame.draw.rect(screen, 'white', (0,0, WIDTH, HEIGHT))
    if keys[pygame.K_UP]:
        player.move('up')
    if keys[pygame.K_DOWN]:
        player.move('down')
    
    # update
    ball.update()
    player.update()
    enemy.update()
    enemy.simple_ai(ball)

    if ball.round_result() == 'player':
        player_score += 1
        ball.reset((WIDTH-BALL_SIZE)//2, (HEIGHT-BALL_SIZE)//2)
    if ball.round_result() == 'simple_ai':
        simple_ai_score += 1
        ball.reset((WIDTH-BALL_SIZE)//2, (HEIGHT-BALL_SIZE)//2)

    # collisions
    ball.collisions(player, enemy)

    # draw
    ball.draw(screen)
    player.draw(screen)
    enemy.draw(screen)
    player_text = font.render(str(player_score), False, (200, 200, 200))
    opponent_text = font.render(str(simple_ai_score), False, (200, 200, 200))
    screen.blit(player_text, (WIDTH // 2 + 20, 20))
    screen.blit(opponent_text, (WIDTH // 2 - 40, 20))

    pygame.display.flip()

# exit
pygame.quit()
sys.exit()
