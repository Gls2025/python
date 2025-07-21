import pygame
import random
import sys

# ---------- CONFIG -------------------------------------------------
CELL_SIZE   = 20         # pixels per grid square
GRID_WIDTH  = 30         # number of columns
GRID_HEIGHT = 20         # number of rows
FPS         = 10         # frames per second (speed)
# -------------------------------------------------------------------

# Derived constants
WINDOW_WIDTH  = GRID_WIDTH  * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 200,   0)
RED   = (200,   0,   0)

# Directions (dx, dy)
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow_pending = 0

    def head(self):
        return self.body[0]

    def turn(self, dir):
        # Prevent 180‑degree reversal
        if (dir[0] * -1, dir[1] * -1) != self.direction:
            self.direction = dir

    def move(self):
        x, y = self.head()
        dx, dy = self.direction
        new_head = (x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT
        # Collision with self
        if new_head in self.body:
            return False  # game over
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()  # remove tail
        return True

    def grow(self):
        self.grow_pending += 1

class Food:
    def __init__(self, snake):
        self.position = self.random_pos(snake)

    def random_pos(self, snake):
        choices = [(x, y) for x in range(GRID_WIDTH)
                          for y in range(GRID_HEIGHT)
                          if (x, y) not in snake.body]
        return random.choice(choices)

def draw_rect(screen, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                       CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    snake = Snake()
    food = Food(snake)
    score = 0
    running = True

    while running:
        # ---- Event handling ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)
                elif event.key == pygame.K_r and not running:
                    # not reached; placeholder for restart hotkey
                    pass

        # ---- Game logic ----
        alive = snake.move()
        if not alive:
            running = False

        # Check for food collision
        if snake.head() == food.position:
            snake.grow()
            score += 1
            food = Food(snake)

        # ---- Drawing ----
        screen.fill(BLACK)
        # Draw snake
        for segment in snake.body:
            draw_rect(screen, segment, GREEN)
        # Draw food
        draw_rect(screen, food.position, RED)
        # Draw score
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))
        pygame.display.flip()

        clock.tick(FPS)

    # ---- Game Over Screen ----
    game_over(screen, font, score)
    pygame.quit()

def game_over(screen, font, score):
    txt1 = font.render("Game Over!", True, WHITE)
    txt2 = font.render(f"Final Score: {score}", True, WHITE)
    txt3 = font.render("Press SPACE to play again", True, WHITE)
    screen.blit(txt1, txt1.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 40)))
    screen.blit(txt2, txt2.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)))
    screen.blit(txt3, txt3.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 40)))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                main()  # restart the game

if __name__ == "__main__":
    main()
