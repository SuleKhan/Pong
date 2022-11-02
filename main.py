import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 700, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong by SuleKhan")

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 80
BALL_SIZE = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_VEL = 5
ball_vel_x = 4
ball_vel_y = 4

FPS = 60

SCORE_FONT = pygame.font.SysFont("ocr-a extended", 40)

LEFT_SCORE = pygame.USEREVENT + 1
RIGHT_SCORE = pygame.USEREVENT + 2

WALL_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Soccer Ball Hit.wav"))


def draw_window(left_paddle, right_paddle, ball, score_left, score_right):
    WIN.fill(BLACK)

    score_text = SCORE_FONT.render("{} - {}".format(score_left, score_right), 1, WHITE)

    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 10))

    pygame.draw.rect(WIN, WHITE, left_paddle)
    pygame.draw.rect(WIN, WHITE, right_paddle)
    pygame.draw.rect(WIN, WHITE, ball)
    pygame.display.update()


def move_left_paddle(keys_pressed, left_paddle):
    if keys_pressed[pygame.K_w] and left_paddle.y > 0:  # UP
        left_paddle.y -= PADDLE_VEL
    if keys_pressed[pygame.K_s] and left_paddle.y + PADDLE_HEIGHT < HEIGHT:  # DOWN
        left_paddle.y += PADDLE_VEL


def move_right_paddle(keys_pressed, right_paddle):
    if keys_pressed[pygame.K_UP] and right_paddle.y > 0:  # UP
        right_paddle.y -= PADDLE_VEL
    if keys_pressed[pygame.K_DOWN] and right_paddle.y + PADDLE_HEIGHT < HEIGHT:  # DOWN
        right_paddle.y += PADDLE_VEL


def move_ball(ball, left_paddle, right_paddle):
    left_paddle_hitbox = pygame.Rect(left_paddle.x + PADDLE_WIDTH, left_paddle.y, 1, PADDLE_HEIGHT)
    right_paddle_hitbox = pygame.Rect(right_paddle.x, right_paddle.y, 1, PADDLE_HEIGHT)

    global ball_vel_x, ball_vel_y
    # TOP AND BOTTOM BORDERS
    if ball.y <= 0:  # TOP
        ball_vel_y *= -1
        WALL_HIT_SOUND.play()
    elif ball.y + BALL_SIZE >= HEIGHT:  # BOTTOM
        ball_vel_y *= -1
        WALL_HIT_SOUND.play()

    #  CHECK COLLISIONS
    if ball.colliderect(left_paddle_hitbox):
        ball_vel_x *= -1
        ball.x = 50 + PADDLE_WIDTH
    elif ball.colliderect(right_paddle_hitbox):
        ball_vel_x *= -1
        ball.x = WIDTH - PADDLE_WIDTH - 50 - BALL_SIZE

    # LEFT AND RIGHT BORDERS
    if ball.x <= 0:  # LEFT
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
        ball_vel_x *= -1
        pygame.event.post(pygame.event.Event(RIGHT_SCORE))
    elif ball.x >= WIDTH:  # RIGHT
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
        ball_vel_x *= -1
        pygame.event.post(pygame.event.Event(LEFT_SCORE))

    ball.x += ball_vel_x
    ball.y += ball_vel_y


def main():
    left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - PADDLE_WIDTH - 50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

    score_left = 0
    score_right = 0

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == LEFT_SCORE:
                score_left += 1
            if event.type == RIGHT_SCORE:
                score_right += 1

        move_ball(ball, left_paddle, right_paddle)
        keys_pressed = pygame.key.get_pressed()
        move_left_paddle(keys_pressed, left_paddle)
        move_right_paddle(keys_pressed, right_paddle)
        draw_window(left_paddle, right_paddle, ball, score_left, score_right)
    pygame.quit()


if __name__ == "__main__":
    main()
