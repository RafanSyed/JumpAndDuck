import pygame
import random

pygame.init()
screen_width = 1500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

block_width = 85
block_height = 170
block_x = 30
block_y = screen_height - block_height
block_speed = 6

bullet_width = 100
bullet_height = 10
bullet_x = screen_width - bullet_width
bullet_speed = 8

block_jump_duration = 60  # Duration of the block jump animation in frames (0.5 seconds)
jump_distance = 60  # Distance the block moves up during the jump animation

block_shrink_duration = 70  # Duration of the block shrink animation in frames (0.5 seconds)
shrink_width = 170  # Width of the block during the shrink animation
shrink_height = 85  # Height of the block during the shrink animation

is_jumping = False
jump_frames = 0

is_shrinking = False
shrink_frames = 0
original_size = (block_width, block_height)

shoot_timer = 0
shoot_interval = 180  # Shoot bullet every 3 seconds (60 frames per second)

bullets = []  # List to store bullet instances

font = pygame.font.SysFont("Arial", 32)
score = 0
high_score = 0
game_started = False
game_over = False

# Timer variables
elapsed_time = 0
time_threshold = 120  # Increase bullet speed every 2 minutes
bullet_speed_increase = 1

def display_score():
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))


def display_start_screen():
    screen.fill((0, 0, 0))
    
    # Display game name
    game_name_surface = font.render("IMPOSSIBLE GAME", True, (255, 255, 255))
    game_name_rect = game_name_surface.get_rect(center=(screen_width/2, screen_height/2 - 50))
    screen.blit(game_name_surface, game_name_rect)

    # Display instructions
    instructions_surface = font.render("Press The UP KEY to jump and the DOWN KEY to duck. Avoid the bullets!", True, (255, 255, 255))
    instructions_rect = instructions_surface.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(instructions_surface, instructions_rect)

    # Display start button
    button_text_surface = font.render("START", True, (255, 255, 255))
    button_text_rect = button_text_surface.get_rect(center=(screen_width/2, screen_height/2 + 50))
    pygame.draw.rect(screen, (0, 255, 0), (button_text_rect.x - 10, button_text_rect.y - 10, button_text_rect.width + 20, button_text_rect.height + 20))
    screen.blit(button_text_surface, button_text_rect)

def display_end_screen():
    screen.fill((0, 0, 0))

    # Display "You Died" message
    game_over_surface = font.render("You Died", True, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect(center=(screen_width/2, screen_height/2 - 50))
    screen.blit(game_over_surface, game_over_rect)

    # Display score
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(score_surface, score_rect)


while running:
    if not game_started:
        display_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(screen_width/2 - 75, screen_height/2 + 40, 150, 50)
                if button_rect.collidepoint(mouse_pos):
                    game_started = True

    elif game_over:
        display_end_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score = 0
                    game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(screen_width/2 - 75, screen_height/2 + 40, 150, 50)
                if button_rect.collidepoint(mouse_pos):
                    score = 0
                    game_over = False

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not is_jumping and not is_shrinking:
                    is_jumping = True
                    jump_frames = block_jump_duration
                elif event.key == pygame.K_DOWN and not is_jumping and not is_shrinking:
                    is_shrinking = True
                    shrink_frames = block_shrink_duration

        if is_jumping:
            if jump_frames > 0:
                if jump_frames >= block_jump_duration / 2:
                    block_y -= block_speed
                else:
                    block_y += block_speed
                jump_frames -= 1
            else:
                is_jumping = False
                block_y = screen_height - block_height

        if is_shrinking:
            if shrink_frames > 0:
                if shrink_frames >= block_shrink_duration / 2:
                    block_width = shrink_width
                    block_height = shrink_height
                    block_y = screen_height - block_height  # Update block_y to ensure it touches the ground
                else:
                    block_width = original_size[0]
                    block_height = original_size[1]
                    block_y = screen_height - block_height  # Update block_y to ensure it touches the ground
                shrink_frames -= 1
            else:
                is_shrinking = False
                block_width = original_size[0]
                block_height = original_size[1]

        if shoot_timer == 0:
            bullet_y = random.choice([450, 570])  # Randomly select bullet height
            bullets.append([bullet_x, bullet_y])  # Add
            shoot_timer = shoot_interval
        else:
            shoot_timer -= 1

        # Update timer
        elapsed_time += 1

        if elapsed_time >= 120 and score < 25:  # Increase bullet speed every 2 minutes until score reaches 25
            bullet_speed += bullet_speed_increase
            elapsed_time = 0  # Reset the timer

        # Update bullet positions
        for bullet in bullets:
            bullet[0] -= bullet_speed

            # Check collision between bullet and block
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            block_rect = pygame.Rect(block_x, block_y, block_width, block_height)
            if bullet_rect.colliderect(block_rect):
                game_over = True  # Set game_over to True if collision occurs
            elif bullet[0] <= 0:
                score += 1  # Increase score if bullet is avoided

        # Remove bullets that go off-screen
        bullets = [bullet for bullet in bullets if bullet[0] > 0]

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (block_x, block_y, block_width, block_height))

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], bullet_width, bullet_height))

        display_score()  # Display the score 

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
