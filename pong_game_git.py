import pygame
import random

pygame.init()
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horizontal Pong - Player vs Computer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 7
FPS = 60
WINNING_SCORE = 5


SCORE_FONT = pygame.font.SysFont("comicsans", 50)

class Paddle:
    COLOR = WHITE
    VEL = 6

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, left=True):
        if left:
            self.x -= self.VEL
        else:
            self.x += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = random.choice([-1, 1]) * random.randint(2, self.MAX_VEL)
        self.y_vel = random.choice([-1, 1]) * random.randint(3, self.MAX_VEL)

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.__init__(self.original_x, self.original_y, self.radius)


def draw(win, paddles, ball, player_score, ai_score):
    win.fill(BLACK)

    player_text = SCORE_FONT.render(f"{player_score}", 1, WHITE)
    ai_text = SCORE_FONT.render(f"{ai_score}", 1, WHITE)
    win.blit(player_text, (WIDTH // 4 - player_text.get_width() // 2, 20))
    win.blit(ai_text, (WIDTH * (3 / 4) - ai_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, bottom_paddle, top_paddle):
    if ball.x - ball.radius <= 0 or ball.x + ball.radius >= WIDTH:
        ball.x_vel *= -1

    
    if ball.y_vel > 0:
        if bottom_paddle.y <= ball.y + ball.radius <= bottom_paddle.y + bottom_paddle.height:
            if bottom_paddle.x <= ball.x <= bottom_paddle.x + bottom_paddle.width:
                ball.y_vel *= -1.1
                ball.x_vel += random.choice([-1, 1])


    else:
        if top_paddle.y <= ball.y - ball.radius <= top_paddle.y + top_paddle.height:
            if top_paddle.x <= ball.x <= top_paddle.x + top_paddle.width:
                ball.y_vel *= -1.1
                ball.x_vel += random.choice([-1, 1])

def ai_move(ball, ai_paddle):
    if ai_paddle.x + ai_paddle.width / 2 < ball.x:
        if ai_paddle.x + ai_paddle.width < WIDTH:
            ai_paddle.move(left=False)
    elif ai_paddle.x + ai_paddle.width / 2 > ball.x:
        if ai_paddle.x > 0:
            ai_paddle.move(left=True)

def handle_player_movement(keys, paddle):
    if keys[pygame.K_LEFT] and paddle.x - paddle.VEL >= 0:
        paddle.move(left=True)
    if keys[pygame.K_RIGHT] and paddle.x + paddle.width + paddle.VEL <= WIDTH:
        paddle.move(left=False)


def main():
    run = True
    clock = pygame.time.Clock()

    bottom_paddle = Paddle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    top_paddle = Paddle(WIDTH // 2 - PADDLE_WIDTH // 2, 10, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    player_score = 0
    ai_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [bottom_paddle, top_paddle], ball, player_score, ai_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_player_movement(keys, bottom_paddle)
        ai_move(ball, top_paddle)

        ball.move()
        handle_collision(ball, bottom_paddle, top_paddle)

    
        if ball.y < 0:
            player_score += 1
            ball.reset()
        elif ball.y > HEIGHT:
            ai_score += 1
            ball.reset()

        
        winner_text = ""
        if player_score >= WINNING_SCORE:
            winner_text = "You Win!"
        elif ai_score >= WINNING_SCORE:
            winner_text = "Computer Wins!"

        if winner_text:
            text = SCORE_FONT.render(winner_text + " Press ENTER", 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        waiting = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        player_score = 0
                        ai_score = 0
                        ball.reset()
                        bottom_paddle.reset()
                        top_paddle.reset()
                        waiting = False

    pygame.quit()

if __name__ == "__main__":
    main()

