import pygame
import sys
import random
import os
import subprocess

# Initialize Pygame
pygame.init()


GRAVITY = 0.5
FPS = 60
JUMP_HEIGHT = 10

# Set up display
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Game states
WELCOME_SCREEN = "welcome_screen"
GAME_SCREEN = "game_screen"
current_state = WELCOME_SCREEN

# Load and resize background image for the welcome screen
background_image_welcome = pygame.image.load("flappy-background.jpeg")
background_image_welcome = pygame.transform.scale(background_image_welcome, (width, height))

# Load and resize Flappy Bird logo for the welcome screen
flappy_bird_logo = pygame.image.load("flappy-bird-logo-png-transparent.png")
logo_width, logo_height = 375, 100
flappy_bird_logo = pygame.transform.scale(flappy_bird_logo, (logo_width, logo_height))

# Load and resize images for the game screen
bird_image = pygame.image.load("bird.png")
pipe_image = pygame.image.load("pipe.png")
background_image_game = pygame.image.load("flappy-background.jpeg")
ground_image = pygame.image.load("floor-sprite.png")

bird_image = pygame.transform.scale(bird_image, (50, 50))
pipe_image = pygame.transform.scale(pipe_image, (50, 300))
ground_image = pygame.transform.scale(ground_image, (width, 100))

# Function to start the Flappy Bird game
def draw_button():
    button_rect = pygame.Rect(width // 2 - 50, height // 2, 100, 50)
    pygame.draw.rect(screen, white, button_rect)
    
    text = font.render("Start", True, black)
    text_rect = text.get_rect(center=button_rect.center)
    
    screen.blit(text, text_rect)
def start_game():
    # Constants
    global screen
    FPS = 60
    GRAVITY = 0.5
    JUMP_HEIGHT = 10

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Create the game window
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flappy Bird")

    # Create sprites
    bird = Bird()
    pipes = pygame.sprite.Group()
    grounds = pygame.sprite.Group()

    # Add initial pipes and grounds
    for i in range(3):
        pipes.add(Pipe(width + i * 300))
        grounds.add(Ground(height - 100))

    # Clock to control the frame rate
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update
        bird.update()
        pipes.update()
        grounds.update()

        # Check for collisions
        if pygame.sprite.spritecollide(bird, pipes, False):
            pygame.quit()
            sys.exit()

        # Draw
        screen.blit(background_image_game, (0, 0))
        screen.blit(bird.image, bird.rect)
        pipes.draw(screen)
        grounds.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

# Bird class for the game screen
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, height // 2)
        self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_HEIGHT

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

# Pipe class for the game screen
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, random.randint(150, 300))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = width
            self.rect.topleft = (self.rect.x, random.randint(150, 300))

# Ground class for the game screen
class Ground(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, y)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = width

# Event handler function
def handle_events(events):
    global current_state
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            button_rect = pygame.Rect(width // 2 - 50, height // 2 - 25, 100, 50)
            if button_rect.collidepoint(mouse_x, mouse_y):
                current_state = GAME_SCREEN
                start_game()

# Game loop
running = True
while running:
    events = pygame.event.get()
    handle_events(events)

    if current_state == WELCOME_SCREEN:
        screen.blit(background_image_welcome, (0, 0))
        screen.blit(flappy_bird_logo, ((width - logo_width) // 2, (height - logo_height) // 2))
        draw_button()  # Draw the button on the welcome screen
        pygame.display.flip()
    elif current_state == GAME_SCREEN:
        start_game()  # Call the function to start the game

    pygame.time.Clock().tick(60)
