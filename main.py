import pygame
import os

#have a font for the text in the game
pygame.font.init()
# load sound effects library
pygame.mixer.init()

# setting the width and height as constants to the size of the game window
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# set the game display name
pygame.display.set_caption(("The Office Snowball Fight"))

HEALTH_TEXT = pygame.font.SysFont("roboto", 55)
WINNER_TEXT = pygame.font.SysFont("roboto", 55)

# predefine a color for the game
# pygame uses RGB and takes it as a tuple:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



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
PLAYER_WIDTH, PLAYER_HEIGHT = 150, 150

# LAST THING TO DO ON PROJECT enter sounds that are mp3 files
# if you're doing wav, mp3 files, do pygame.mixer.Sound(then the path).
THROW_SOUND = pygame.mixer.Sound(os.path.join("sounds", "throw.wav"))
GAME_MUSIC = pygame.mixer.Sound(os.path.join("sounds", "office.mp3"))
INTRO_FIGHT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "ready_fight.wav"))
JIM_HIT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "jim_ouch.wav"))
DWIGHT_OUCH_SOUND = pygame.mixer.Sound(os.path.join("sounds", "dwight_ouch.wav"))
KO_SOUND = pygame.mixer.Sound(os.path.join("sounds", "KO.mp3"))


# EVENTS in case they get hit. It may look strange but the + 1 is to make them unique, they can't both be 1.
JIM_HIT = pygame.USEREVENT
DWIGHT_HIT = pygame.USEREVENT + 1

# assign images to jim and dwight
JIM_IMAGE = pygame.image.load(os.path.join("players", "jim.png"))
JIM_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    JIM_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0)


DWIGHT_IMAGE = pygame.image.load(os.path.join("players", "dwight.PNG"))
DWIGHT_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    DWIGHT_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0)

# scale so that the image will fit nicely
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("backgrounds", "office_background.png")), (WIDTH, HEIGHT))


def draw_window(jim, dwight, jim_bullets, dwight_bullets, jim_health, dwight_health):

    # NOTE DRAW things in order, otherwise they stack on top of each other
    # we set the window color.
    # FIRST USE THIS: WIN.fill(WHITE)
    # The (0, 0) is for the padding
    WIN.blit(BACKGROUND, (0, 0))

    # DRAW THE MIDDLE BORDER to the WIN for window, BLACK for color and BORDER for my pre defined rectangle
    pygame.draw.rect(WIN, BLACK, BORDER)
    # render some health stats.

    jim_health_text = HEALTH_TEXT.render(f"Health: {str(jim_health)}", 1, WHITE)
    dwight_health_text = HEALTH_TEXT.render(f"Health: {str(dwight_health)}", 1, WHITE)
    # 10, 10 and -10, 10 is just padding from where the text will be
    WIN.blit(dwight_health_text, (WIDTH - dwight_health_text.get_width() - 10, 10))
    WIN.blit(jim_health_text, (10, 10))

    # we use the .blit() to add an image or text to the window
    # image, and then it's position on the window
    WIN.blit(JIM_IMAGE, (jim.x, jim.y))
    WIN.blit(DWIGHT_IMAGE, (dwight.x, dwight.y))

    # DRAW the bullets for each character
    for bullet in jim_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)
        # pygame.draw.circle(WIN, WHITE, (jim.x, jim.y), 15, 15)

    for bullet in dwight_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)
        # pygame.draw.circle(WIN, WHITE, (dwight.x, dwight.y), 15, 15)

    # The new display setting white will not update unless we do the following update code:
    pygame.display.update()


def draw_winner(text):
    KO_SOUND.play()
    draw_text = WINNER_TEXT.render(text, 1, WHITE)
    # this will put the winner text over the center of the screen.
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    # update the display if someone wins
    pygame.display.update()
    # this pause will display for however many miliseconds
    pygame.time.delay(5000)

def handle_jim_movement(key_press, jim):
    # moving the players around which will update it's position every time it loops
    if key_press[pygame.K_a] and jim.x - VEL > 0:  # left key AND prevent him from moving past the left screen border
        jim.x -= VEL
    if key_press[pygame.K_d] and jim.x + VEL + jim.width < BORDER.x: # right key AND prevent him from moving past the center screen border
        jim.x += VEL
    if key_press[pygame.K_w] and jim.y - VEL > 0:  # up key
        jim.y -= VEL
    if key_press[pygame.K_s] and jim.y + VEL + jim.height < HEIGHT:  # down key
        jim.y += VEL

def handle_dwight_movement(key_press, dwight):
    # moving the players around which will update it's position every time it loops
    if key_press[pygame.K_LEFT] and dwight.x - VEL > BORDER.x + BORDER.width:  # left key
        dwight.x -= VEL
    if key_press[pygame.K_RIGHT] and dwight.x + VEL + dwight.width < WIDTH:  # right key
        dwight.x += VEL
    if key_press[pygame.K_UP] and dwight.y - VEL > 0:  # up key
        dwight.y -= VEL
    if key_press[pygame.K_DOWN] and dwight.y + VEL + dwight.height < HEIGHT:  # down key
        dwight.y += VEL

def handle_bullets(jim_bullets, dwight_bullets, jim, dwight):
    for bullet in jim_bullets:
        # make the bullets go RIGHT towards the WIDTH, or right of the screen
        bullet.x += BULLET_VEL
        # if the bullet collides, then make the bullet disappear
        if dwight.colliderect(bullet):
            pygame.event.post(pygame.event.Event(DWIGHT_HIT))
            jim_bullets.remove(bullet)
            DWIGHT_OUCH_SOUND.play()
            # elif so we don't remove it twice, this will remove the bullet if it's off the screen
            # otherwise it will stay in the list and not allow you to shoot anymore
        elif bullet.x > WIDTH:
            jim_bullets.remove(bullet)

    for bullet in dwight_bullets:
        # make the bullets go LEFT towards 0, or the left of the screen
        bullet.x -= BULLET_VEL
        # if the bullet collides, then make the bullet disappear
        if jim.colliderect(bullet):
            pygame.event.post(pygame.event.Event(JIM_HIT))
            dwight_bullets.remove(bullet)
        elif bullet.x < 0:
            dwight_bullets.remove(bullet)

# the game will run until x on the window
def main():
    # (x, y, width, height)
    jim = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    dwight = pygame.Rect(700, 300, PLAYER_WIDTH, PLAYER_HEIGHT)

    jim_bullets = []
    dwight_bullets = []

    jim_health = 12
    dwight_health = 12

    # clock will help the loop/game keep better track of time, FPS is in the while loop
    clock = pygame.time.Clock()
    run_game = True
    # This will play every time the game starts, even on a restart
    # preset the volume and how many times it will loop and fade is the amount of time for fading at start and end
    GAME_MUSIC.set_volume(0.1)
    GAME_MUSIC.play(loops=10, fade_ms=3000)
    INTRO_FIGHT_SOUND.play()

    while run_game:

        # The speed of the while loop:
        clock.tick(FPS)
        # if i hit the x on the window, the loop will break and end the game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                # add the following at the VERY END so that it quits instead of restarts when they click the x
                pygame.quit()

            # KEYDOWN allows you to hold down a key but we don't want them to while
            # shooting.
            if event.type == pygame.KEYDOWN:
                # checking for the bullet shooting event button AND only doing it if they have enough bullets
                if event.key == pygame.K_SPACE and len(jim_bullets) < MAX_BULLETS:
                    # Where the bullet will come out of the character, the width of the bullet is 10 and height is 5
                    bullet = pygame.Rect(jim.x + jim.width, jim.y + jim.height//2 - 2, 10, 5)
                    jim_bullets.append(bullet)
                    THROW_SOUND.play()
                if event.key == pygame.K_m and len(dwight_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(dwight.x, dwight.y + dwight.height//2 - 2, 10, 5)
                    dwight_bullets.append(bullet)
                    THROW_SOUND.play()

            # If hit, then minus a health point from the player
            if event.type == JIM_HIT:
                jim_health -= 1
                JIM_HIT_SOUND.play()
            if event.type == DWIGHT_HIT:
                dwight_health -= 1
                DWIGHT_OUCH_SOUND.play()


        end_game_text = ""
        if jim_health <= 0:
            end_game_text = "Dwight Wins!"

        if dwight_health <= 0:
            end_game_text = "Jim Wins!"

        if end_game_text != "":
            draw_winner(end_game_text)
            break

        # you can test the bullets and see if the list appends and removes
        print(jim_bullets, dwight_bullets)
        # Movement function for jim and dwight
        key_press = pygame.key.get_pressed()
        handle_jim_movement(key_press, jim)
        handle_dwight_movement(key_press, dwight)

        handle_bullets(jim_bullets, dwight_bullets, jim, dwight)

        draw_window(jim, dwight, jim_bullets, dwight_bullets, jim_health, dwight_health)

    # have this here until the very end to just restart instead of quit: pygame.quit()
    main()

# if the actual "name" of the file is "main" then it will run
# instead of this running if we're running something else in
# the same project. If so, then run the main function:


if __name__ == "__main__":
    main()