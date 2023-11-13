import pygame
import sys
import random

pygame.init()

# Set up display
width, height = 500, 500
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

# Load and resize background image
original_background = pygame.image.load("flappy-background.jpeg")  # Change the filename accordingly
background_image = pygame.transform.scale(original_background, (width, height))

# Load and resize Flappy Bird logo
original_logo = pygame.image.load("flappy-bird-logo-png-transparent.png")  # Change the filename accordingly
logo_width, logo_height = 375, 100  # Set the desired size for the logo
flappy_bird_logo = pygame.transform.scale(original_logo, (logo_width, logo_height))

def draw_welcome_screen():
    screen.blit(background_image, (0, 0))  # Blit the resized background image
    screen.blit(flappy_bird_logo, ((width - logo_width) // 2, (height - logo_height) // 2))  # Center the logo
def draw_button():
    button_rect = pygame.Rect(width // 2 - 50, (height // 2 + logo_height // 2) + 40, 100, 50)
    pygame.draw.rect(screen, white, button_rect)
    
    text = font.render("Start", True, black)
    text_rect = text.get_rect(center=button_rect.center)
    
    screen.blit(text, text_rect)

# Event handler function
def handle_events(events):
    global current_state
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            button_rect = pygame.Rect(width // 2 - 50, height // 2 + logo_height // 2, 100, 50)
            if button_rect.collidepoint(mouse_x, mouse_y):
                current_state = GAME_SCREEN
                start_game()

# Function to start the Flappy Bird game
def start_game():
    subprocess.Popen(["python", "flappy_bird_game.py"])

# Game loop
running = True
while running:
    events = pygame.event.get()
    handle_events(events)

    if current_state == WELCOME_SCREEN:
        draw_welcome_screen()
        draw_button()  # Draw the button on the welcome screen
        pygame.display.flip()
    elif current_state == GAME_SCREEN:
        screen.blit(background_image, (0, 0))  # Blit the resized background image
        draw_button()  # Draw the button on the game screen
        pygame.display.flip()

    pygame.time.Clock().tick(60)
