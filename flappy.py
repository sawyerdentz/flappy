import pygame
import random

pygame.init()
pygame.font.init()

# screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Game")

# initialize clock
clock = pygame.time.Clock()

# initialize player
player = pygame.Rect((SCREEN_WIDTH//2.5-25, SCREEN_HEIGHT//2-25, 25, 25))
player_velocity = 0
player_alive = False
player_score = 0

# initialize font and text surface
font = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = font.render(f"Score: {player_score}", True, (255, 255, 255))

# gravity scale
GRAVITY = 0.98

class Pipe:
    def __init__(self, top_length: int = 0, bottom_length: int = 0, velocity: int = -5):
        self.top_length = top_length
        self.bottom_length = bottom_length
        self.velocity = velocity
        self.scored = False

        # if the length of either the top or bottom is 0, randomize the length of both top and bottom
        if self.top_length == 0 or self.bottom_length == 0:
            self.top_length = random.randint(SCREEN_HEIGHT//4, SCREEN_HEIGHT//4*3)
            self.bottom_length = SCREEN_HEIGHT - (self.top_length + SCREEN_HEIGHT//4)

        # initialize the rectangles
        self.top = pygame.Rect(SCREEN_WIDTH, 0, 30, self.top_length)
        self.bottom = pygame.Rect(SCREEN_WIDTH, SCREEN_HEIGHT-self.bottom_length, 30, self.bottom_length)

    def update(self, dt: float):
        """
        Function that updates the top and bottom rectangles and updates positions
        """
        pygame.draw.rect(screen, (0, 166, 0), self.top)
        pygame.draw.rect(screen, (0, 166, 0), self.bottom)
        self.top.x += self.velocity * dt
        self.bottom.x += self.velocity * dt

# create list of pipes and pipe interval settings
pipes = []
pipe_interval = 1500

# create first pipe
pipes.append(Pipe())

# game loop
run = True
start = False
while run:
    # draw background
    screen.fill((112, 197 , 206))
    # draw player
    pygame.draw.rect(screen, (248, 240, 35), player)
    # get time since last frame and multiply it by constant
    dt = clock.tick(60)/1000 * 50

    # wait to start until player presses space
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] and not start:
        start = True
        player_alive = True
        last_pipe_time = pygame.time.get_ticks()

    if player_alive:
        # get current time
        current_time = pygame.time.get_ticks()
        # create pipes and add to list
        if current_time - last_pipe_time >= pipe_interval:
            pipes.append(Pipe())
            last_pipe_time = current_time

        # check for jump and update velocity
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            player_velocity = -10

        # update player velocity and pipes
        player_velocity += GRAVITY * dt
        for pipe in pipes:
            pipe.update(dt)

        # handle player position
        player.y += player_velocity * dt

        # check if player out of bounds
        if player.y > SCREEN_HEIGHT + 50 or player.y < -50: 
            player_alive = False

        # loop through pipes
        for pipe in pipes:
            # remove pipe if off the screen
            if pipe.top.x < -(pipe.top.width):
                pipes.remove(pipe)

            # check for pipe collision with player
            if player.colliderect(pipe.top) or player.colliderect(pipe.bottom):
                player_alive = False

            # check if player passed through pipe and update score
            if pipe.top.x + pipe.top.width < player.x and not pipe.scored:
                player_score += 1
                pipe.scored = True

    # if player not alive
    else: 
        # freeze player
        player_velocity = 0
        for pipe in pipes:
            # freeze pipes
            pipe.update(0)       

    # draw score
    text_surface = font.render(f"Score: {player_score}", True, (255, 255, 255))
    screen.blit(text_surface, (0, 0))

    # check for exit out of window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

# quit game
pygame.quit()