import pygame
import os

# setting the width and height as constants to the size of the game window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# set the game display name
pygame.display.set_caption(("Harry Potter Duels"))
# predefine a color for the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# Setting a border for the players to not be able to cross (Rect = rectangle)
# WIDTH/2 - 5 put's it right in the middle horizontally
BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)
# i want to define how fast i want my main loop to update (Frames Per Second):
FPS = 60
# VEL IS THE SPEED OF THE CHARACTERS
VEL = 5
# speed of the bullets
BULLET_VEL = 7
# Limit of bullets
MAX_BULLETS = 3
PLAYER_WIDTH, PLAYER_HEIGHT = 200, 150

# EVENTS in case they get hit. It may look strange but the 1 and 2 is to make them unique, they can't both be 1.
HARRY_HIT = pygame.USEREVENT + 1
HERMIONE_HIT = pygame.USEREVENT + 2

HARRY_IMAGE = pygame.image.load(os.path.join("players", "lego_harry.png"))
HARRY_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    HARRY_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0)


HERMIONE_IMAGE = pygame.image.load(os.path.join("players", "IMG_2286.PNG"))
HERMIONE_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    HERMIONE_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 180)


def draw_window(harry, hermione, harry_bullets, hermione_bullets):

    # NOTE DRAW things in order, otherwise they stack on top of each other
    # we set the window color.
    # pygame uses RGB and takes it as a tuple:
    WIN.fill(WHITE)
    # DRAW THE MIDDLE BORDER to the WIN for window, BLACK for color and BORDER for my pre defined rectangle
    pygame.draw.rect(WIN, BLACK, BORDER)
    # we use the .blit() to add an image or text to the window
    # image, and then it's position on the window
    WIN.blit(HARRY_IMAGE, (harry.x, harry.y))
    WIN.blit(HERMIONE_IMAGE, (hermione.x, hermione.y))

    # DRAW the bullets for each character
    for bullet in harry_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in hermione_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # The new display setting white will not update unless we do the following update code:
    pygame.display.update()

def handle_harry_movement(keys_pressed, harry):
    # moving the players around which will update it's position every time it loops
    if keys_pressed[pygame.K_a] and harry.x - VEL > 0:  # left key AND prevent him from moving past the left screen border
        harry.x -= VEL
    if keys_pressed[pygame.K_d] and harry.x + VEL + harry.width < BORDER.x: # right key AND prevent him from moving past the center screen border
        harry.x += VEL
    if keys_pressed[pygame.K_w] and harry.y - VEL > 0:  # up key
        harry.y -= VEL
    if keys_pressed[pygame.K_s] and harry.y + VEL + harry.height < HEIGHT:  # down key
        harry.y += VEL

def handle_hermione_movement(keys_pressed, hermione):
    # moving the players around which will update it's position every time it loops
    if keys_pressed[pygame.K_LEFT] and hermione.x - VEL > BORDER.x + BORDER.width:  # left key
        hermione.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and hermione.x + VEL + hermione.width < WIDTH:  # right key
        hermione.x += VEL
    if keys_pressed[pygame.K_UP] and hermione.y - VEL > 0:  # up key
        hermione.y -= VEL
    if keys_pressed[pygame.K_DOWN] and hermione.y + VEL + hermione.height < HEIGHT:  # down key
        hermione.y += VEL

def handle_bullets(harry_bullets, hermione_bullets, harry, hermione):
    for bullet in harry_bullets:
        # make the bullets go RIGHT towards the WIDTH, or right of the screen
        bullet.x += BULLET_VEL
        # if the bullet collides, then make the bullet disappear
        if hermione.colliderect(bullet):
            pygame.event.post(pygame.event.Event(HERMIONE_HIT))
            harry_bullets.remove(bullet)

    for bullet in hermione_bullets:
        # make the bullets go LEFT towards 0, or the left of the screen
        bullet.x -= BULLET_VEL
        # if the bullet collides, then make the bullet disappear
        if harry.colliderect(bullet):
            pygame.event.post(pygame.event.Event(HARRY_HIT))
            hermione_bullets.remove(bullet)

# the game will run until x on the window
def main():
    harry = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    hermione = pygame.Rect(700, 300, PLAYER_WIDTH, PLAYER_HEIGHT)

    harry_bullets = []
    hermione_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        # The speed of the while loop:
        clock.tick(FPS)
        # if i hit x, the loop will break and end the game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # checking for the bullet shooting event button AND only doing it if they have enough bullets
                if event.key == pygame.K_e and len(harry_bullets) < MAX_BULLETS:
                    # Where the bullet will come out of the character, the width of the bullet is 10 and height is 5
                    bullet = pygame.Rect(harry.x + harry.width, harry.y + harry.height//2 - 2, 10, 5)
                    harry_bullets.append(bullet)
                if event.key == pygame.K_m and len(hermione_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(hermione.x, hermione.y + hermione.height//2 - 2, 10, 5)
                    hermione_bullets.append(bullet)

        print(harry_bullets, hermione_bullets)
        # Movement function for harry and hermione
        keys_pressed = pygame.key.get_pressed()
        handle_harry_movement(keys_pressed, harry)
        handle_hermione_movement(keys_pressed, hermione)

        handle_bullets(harry_bullets, hermione_bullets, harry, hermione)

        draw_window(harry, hermione, harry_bullets, hermione_bullets)

    pygame.quit()

# if the actual "name" of the file is "main" then it will run
# instead of this running if we're running something else in
# the same project. If so, then run the main function:


if __name__ == "__main__":
    main()