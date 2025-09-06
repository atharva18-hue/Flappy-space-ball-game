import pygame
import random
import sys

# --- Initialize pygame ---
pygame.init()

# --- Fullscreen setup ---
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("🚀 Flappy Space Ball 🔥")

# --- Clock ---
clock = pygame.time.Clock()
FPS = 60

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 200, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)  # Footer color

# --- Fonts ---
title_font = pygame.font.SysFont("Arial", 72, bold=True)
small_font = pygame.font.SysFont("Arial", 28)
footer_font = pygame.font.SysFont("Arial", 20, bold=True)  # Smaller footer

# --- Gradient Background ---
def draw_gradient_background(surface, top_color, bottom_color):
    for y in range(HEIGHT):
        color = (
            top_color[0] + (bottom_color[0] - top_color[0]) * y // HEIGHT,
            top_color[1] + (bottom_color[1] - top_color[1]) * y // HEIGHT,
            top_color[2] + (bottom_color[2] - top_color[2]) * y // HEIGHT,
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

# --- Stars ---
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(50)]
def draw_stars(surface):
    for star in stars:
        pygame.draw.circle(surface, WHITE, star, 2)
        star[1] += 1
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0

# --- Player & Pipes Setup ---
player_radius = 15
gravity = 0.5
jump_strength = -8
pipe_width = 70
pipe_gap = 320  # bigger gap for easier gameplay
pipe_vel = 3

def create_pipe():
    y = random.randint(150, HEIGHT - 150)
    return {"x": WIDTH, "top": y - pipe_gap // 2, "bottom": y + pipe_gap // 2}

def show_intro():
    intro = True
    while intro:
        screen.fill(BLACK)
        draw_gradient_background(screen, (10, 10, 50), (0,0,0))
        draw_stars(screen)
        title_text = title_font.render("🚀 FLAPPY SPACE BALL 🔥", True, GOLD)
        enter_text = small_font.render("Press SPACE or UP arrow to start", True, WHITE)
        footer_text = footer_font.render("Built by @Atharva Chavhan", True, YELLOW)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
        screen.blit(enter_text, (WIDTH//2 - enter_text.get_width()//2, HEIGHT//2))
        screen.blit(footer_text, (WIDTH//2 - footer_text.get_width()//2, HEIGHT - 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    intro = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

def show_game_over(score):
    over = True
    while over:
        screen.fill(BLACK)
        draw_gradient_background(screen, (10, 10, 50), (0,0,0))
        draw_stars(screen)
        game_over_text = title_font.render("💀 GAME OVER 💀", True, GOLD)
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        option_text = small_font.render("SHIFT to Try Again | ESC to Exit", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(option_text, (WIDTH//2 - option_text.get_width()//2, HEIGHT//2 + 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    over = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

def game_loop():
    player_x = 50
    player_y = HEIGHT // 2
    player_vel = 0
    pipes = []
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_vel = jump_strength

        draw_gradient_background(screen, (10, 10, 50), (0,0,0))
        draw_stars(screen)

        player_vel += gravity
        player_y += player_vel

        if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - 300:  # more horizontal spacing
            pipes.append(create_pipe())

        for pipe in pipes:
            pipe["x"] -= pipe_vel

        pipes = [pipe for pipe in pipes if pipe["x"] + pipe_width > 0]

        # Collision detection
        for pipe in pipes:
            if player_x + player_radius > pipe["x"] and player_x - player_radius < pipe["x"] + pipe_width:
                if player_y - player_radius < pipe["top"] or player_y + player_radius > pipe["bottom"]:
                    running = False

        if player_y - player_radius <= 0 or player_y + player_radius >= HEIGHT:
            running = False

        # Scoring
        for pipe in pipes:
            if pipe["x"] + pipe_width == player_x:
                score += 1

        # Draw Player
        pygame.draw.circle(screen, GOLD, (player_x, int(player_y)), player_radius)

        # Draw Pipes
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))
            pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], pipe_width, HEIGHT))

        # Draw Score
        text = small_font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10,10))
        pygame.display.flip()

    show_game_over(score)

# --- Run Game ---
while True:
    show_intro()
    game_loop()
