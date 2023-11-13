import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
GRAVITY = 0.5
JUMP_HEIGHT = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.image.load("bird.png")
pipe_image = pygame.image.load("pipe.png")
background_image = pygame.image.load("flappy-background.jpeg")
ground_image = pygame.image.load("floor-sprite.png")

# Resize images
bird_image = pygame.transform.scale(bird_image, (50, 50))
pipe_image = pygame.transform.scale(pipe_image, (50, 300))
ground_image = pygame.transform.scale(ground_image, (WIDTH, 100))

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_HEIGHT

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, random.randint(150, 300))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.topleft = (self.rect.x, random.randint(150, 300))

# Ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, y)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = WIDTH

# Create sprites
bird = Bird()
pipes = pygame.sprite.Group()
grounds = pygame.sprite.Group()

# Add initial pipes and grounds
for i in range(3):
    pipes.add(Pipe(WIDTH + i * 300))
    grounds.add(Ground(HEIGHT - 100))

# Clock to control the frame rate
clock = pygame.time.Clock()
running = False

def draw_button():
    button_rect = pygame.Rect(width // 2 - 50, height // 2 - 25, 100, 50)
    pygame.draw.rect(screen, white, button_rect)
    
    text = font.render("Start", True, black)
    text_rect = text.get_rect(center=button_rect.center)
    
    screen.blit(text, text_rect)

# Event handler function
def handle_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            button_rect = pygame.Rect(width // 2 - 50, height // 2 - 25, 100, 50)
            if button_rect.collidepoint(mouse_x, mouse_y):
                print("Start button clicked!")
                running=True

running=True
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
    screen.blit(background_image, (0, 0))
    screen.blit(bird.image, bird.rect)
    pipes.draw(screen)
    grounds.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
