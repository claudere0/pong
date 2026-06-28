import pygame, random
from settings import WIDTH, HEIGHT, WIN_SCORE

class Ball:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
        self.dx = 267 * random.choice((1, -1))
        self.dy = 267 * random.choice((1, -1))
        self.bounce_multiplier = 1
        self.spawn_x = x
        self.spawn_y = y

    def update(self, dt):
        self.rect.x += self.dx * self.bounce_multiplier * dt
        self.rect.y += self.dy * self.bounce_multiplier * dt

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
        self.dx = 267 * random.choice((1, -1))
        self.dy = 267 * random.choice((1, -1))
        self.bounce_multiplier = 1

    def draw(self, screen):
        pygame.draw.ellipse(screen, 'white', self.rect)

class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, WIDTH//32, HEIGHT//6)
        self.speed = 267
        self.color = color

    def update(self):
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move_up(self, dt):
        self.rect.y -= self.speed * dt
    
    def move_down(self, dt):
        self.rect.y += self.speed * dt

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
    
    def input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pygame.draw.rect(self.screen, 'white', (0,0, WIDTH, HEIGHT))
        if keys[pygame.K_UP]:
            self.player.move_up(dt)
        if keys[pygame.K_DOWN]:
            self.player.move_down(dt)

    def update_ai(self,dt):
        if self.enemy.rect.centery > self.ball.rect.centery:
            self.enemy.move_up(dt)
        else:
            self.enemy.move_down(dt)

    def update_objects(self, dt):
        self.ball.update(dt)
        self.player.update()
        self.enemy.update()

    def update_score(self):
        goal = self.ball.goal()
        if goal == 'player':
            self.player_score += 1
            self.ball.reset()
        if goal == 'simple_ai':
            self.simple_ai_score += 1
            self.ball.reset()

    def check_winner(self):
        if self.player_score >= WIN_SCORE:
            print('player wins')
            self.running = False

        if self.simple_ai_score >= WIN_SCORE:
            print('player lost')
            self.running = False

    def update(self, dt):
        self.update_ai(dt)
        self.update_objects(dt)
        self.update_score()
        self.check_winner()

    def collisions(self):
        if self.ball.dx < 0 and self.ball.rect.colliderect(self.enemy.rect):
            self.ball.bounce()
            self.ball.rect.left = self.enemy.rect.right

        if self.ball.dx > 0 and self.ball.rect.colliderect(self.player.rect):
            self.ball.bounce()
            self.ball.rect.right = self.player.rect.left

    def draw_score(self):
        player_text = self.font.render(str(self.player_score), False, (255, 255, 255))
        enemy_text = self.font.render(str(self.simple_ai_score), False, (255, 255, 255))
        self.screen.blit(player_text, (WIDTH // 2 + 16, 16))
        self.screen.blit(enemy_text, (WIDTH // 2 - 32, 16))

    def draw(self):
        self.ball.draw(self.screen)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        self.draw_score()
        pygame.display.flip()

    def run(self):
        while self.running:
            # time
            dt = self.clock.tick(self.FPS)/1000
            self.screen.fill('black')

            self.events()
            self.input(dt)
            self.update(dt)
            self.collisions()
            self.draw()

def main():
    pygame.init()

    game = Game()
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()