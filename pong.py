import pygame, sys
pygame.init()

WIDTH = 512
HEIGHT = 384
FPS = 60

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("OH_MY_PONG")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

BALL_SIZE = 16

class Ball:
    def __init__(self):
        self.rect = pygame.Rect((WIDTH-BALL_SIZE)//2, (HEIGHT-BALL_SIZE)//2,BALL_SIZE, BALL_SIZE)
        self.dx = 5
        self.dy = -5

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, 'white', self.rect)

class Paddle:
    def __init__(self):
        pass
    









ball = Ball()

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
    # update
    ball.update()
    # collisions

    # draw
    ball.draw(screen)

    pygame.display.flip()

# exit
pygame.quit()
sys.exit()
