import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
GROUND_HEIGHT = 50
GRAVITY = 0.25
JUMP_HEIGHT = 3.5
SUPER_JUMP_HEIGHT = 6.5 
PIPE_WIDTH = 50
PIPE_GAP = 200
PIPE_SPEED = 2
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))

bg_img = pygame.image.load('background.png').convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

#bird_images = [pygame.image.load(f'plane{i}.png').convert_alpha() for i in range(1, 3)]
bird_images = [pygame.image.load(f'bird{i}.png').convert_alpha() for i in range(1, 3)]
bird_index = 0
bird_img = bird_images[bird_index]

#pipe_img = pygame.image.load('tower.png').convert_alpha()
pipe_img = pygame.image.load('pipe.png').convert_alpha()
ground_img = pygame.image.load('base.png').convert()
ground_img = pygame.transform.scale(ground_img, (WIDTH, GROUND_HEIGHT))

#game_over_img = pygame.image.load('911.jpg').convert_alpha() 
game_over_img = pygame.image.load('gameover.png').convert_alpha() 
game_over_rect = game_over_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

instructions_img = pygame.image.load('message.png').convert_alpha()
instructions_rect = instructions_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

font = pygame.font.SysFont(None, 36)

class Bird:
    def __init__(self):
        self.x = WIDTH // 3
        self.y = HEIGHT // 2
        self.vel_y = 0
        self.width = bird_img.get_width()
        self.height = bird_img.get_height()
        self.dead = False
        self.jump_animation_timer = 0

    def jump(self):
        self.vel_y = -JUMP_HEIGHT
        self.jump_animation_timer = FPS // 2  # Half a second for the jump animation

    def super_jump(self):
        self.vel_y = -SUPER_JUMP_HEIGHT
        self.jump_animation_timer = FPS // 2

    def move(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        if self.jump_animation_timer > 0:
            self.jump_animation_timer -= 1

    def draw(self):
        if self.jump_animation_timer > 0:
            win.blit(bird_images[1], (self.x, self.y))
        else:
            win.blit(bird_img, (self.x, self.y))


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)
        self.top_pipe = pygame.transform.flip(pipe_img, False, True)
        self.bottom_pipe = pipe_img

    def move(self):
        self.x -= PIPE_SPEED

    def offscreen(self):
        return self.x < -PIPE_WIDTH

    def draw(self):
        win.blit(self.top_pipe, (self.x, self.height - self.top_pipe.get_height()))
        win.blit(self.bottom_pipe, (self.x, self.height + PIPE_GAP))


def draw_window(bird, pipes, score, game_over=False, show_instructions=False):
    win.blit(bg_img, (0, 0))
    bird.draw()
    for pipe in pipes:
        pipe.draw()
    win.blit(ground_img, (0, HEIGHT - GROUND_HEIGHT))
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))
    
    if show_instructions:
        win.blit(instructions_img, instructions_rect.topleft)
    
    if game_over:
        win.blit(game_over_img, game_over_rect.topleft)
        play_again_text = font.render("Play Again", True, WHITE)
        pygame.draw.rect(win, BLACK, (WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50))
        win.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2 + 80))
        
        quit_text = font.render("Quit", True, WHITE)
        pygame.draw.rect(win, BLACK, (WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 50))
        win.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 150))

    pygame.display.flip()



def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(WIDTH + i * 300) for i in range(3)]
    score = 0

    running = True
    game_over = False
    show_instructions = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not bird.dead:
                    bird.jump()
                elif event.key == pygame.K_x and not bird.dead:  # Super jump when X is pressed
                    bird.super_jump()
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100:
                    if HEIGHT // 2 + 70 < mouse_y < HEIGHT // 2 + 120: 
                        main()
                    elif HEIGHT // 2 + 140 < mouse_y < HEIGHT // 2 + 190: 
                        pygame.quit()
                        sys.exit()


        if not bird.dead and not show_instructions:
            bird.move()
            for pipe in pipes:
                pipe.move()
                if pipe.offscreen():
                    pipes.remove(pipe)
                    pipes.append(Pipe(WIDTH))
                    score += 1
                if pipe.x < bird.x < pipe.x + PIPE_WIDTH:
                    if bird.y < pipe.height or bird.y + bird.height > pipe.height + PIPE_GAP:
                        bird.dead = True
                        game_over = True

        draw_window(bird, pipes, score, game_over, show_instructions)

        if show_instructions and pygame.mouse.get_pressed()[0]:
            show_instructions = False

    pygame.quit()


if __name__ == "__main__":
    main()
