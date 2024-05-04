# Import the pygame module
import pygame
import random
import os

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()

# SET OF CLASSES: Player, Enemy, Explosion, Plasma_Ball, Shot

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("spacecraft.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(0,300))
        self.lives = 5
        self.score = 0

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define a Plasma_Ball object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'Plasma_Ball'
class Plasma_Ball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Plasma_Ball, self).__init__()
        self.surf = pygame.image.load("small_shot.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(60+x,25+y))

    # Move the sprite based on user keypresses
    def update(self,x,y):
        self.rect = self.surf.get_rect(center=(60+x,25+y))

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5,20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the Explosion class
class Explosion:
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.current_frame = 0
        self.animation_speed = 100
        self.image = explosion_images[self.current_frame]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.current_frame += 1
        if self.current_frame//self.animation_speed >= len(explosion_images):
            return True
        self.image = explosion_images[self.current_frame // self.animation_speed]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        return False

# Define the Shot class

class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.image.load("small_shot.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center=(60+x,25+y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

# The function that will draw the start menu.

def draw_start_menu():
    screen.fill((0,0,0))
    font = pygame.font.SysFont('arial',40)
    title = font.render('My Game', True,(255,255,255))
    start_playing = font.render('To start playing press <Space>',True,(255,255,255))
    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))
    screen.blit(start_playing, (SCREEN_WIDTH/2 - start_playing.get_width()/2, SCREEN_HEIGHT/2 + start_playing.get_height()/2))
    pygame.display.update()

# The function that will draw the end menu.

def draw_end_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    play_again = font.render('To play again press <y>', True, (255, 255, 255))
    end_program = font.render('To end program press <n> ', True, (255, 255, 255))
    screen.blit(play_again, (SCREEN_WIDTH/2 - play_again.get_width()/2, SCREEN_HEIGHT/2 - play_again.get_height()/2))
    screen.blit(end_program, (SCREEN_WIDTH/2 - end_program.get_width()/2, SCREEN_HEIGHT/2 + end_program.get_height()/2))
    pygame.display.update()

# The function that starts the game.

def start():
    global game_state, running
    while running and game_state == "start_menu":
        draw_start_menu()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                running = False
                pygame.quit()
                break
            
            if keys[pygame.K_SPACE]:
                game_state = "game"
                break

# The function that plays the game

def play():
    global running, game_state

    while running and game_state == "game":
        
        # font type.
        # labels for lives and score
        font = pygame.font.SysFont('arial',24)
        lives_label = font.render('lives: ' + str(player.lives), True,(255,255,255))
        score_label = font.render('score: ' + str(player.score), True, (255,255,255))

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                running = False
                break

            # Add a new enemy?
            if event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            # Shooting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    shot = Shot(player.rect.centerx, player.rect.top)
                    all_sprites.add(shot)
                    shots.add(shot)

        # Draw the background using the blit() function
        screen.blit(background,(0,0))

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)
        x = player.rect.x
        y = player.rect.y

        # Draw the score label using the blit() function
        screen.blit(score_label,(680,20))

        # Update enemy position
        enemies.update()

        # Update the plasma_ball sprite based on player position
        plasma_ball.update(x,y)

        # Update the shots based on player position
        shots.update()

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        # spritecollide(sprite, group, dokill)
        # "dokill" argument is a boolean argument.If it is true,
        # the function will call the call the kill() method on
        # all the sprites.
        if pygame.sprite.spritecollide(player, enemies,True):
            
            if player.lives >= 1:
                player.lives = player.lives - 1
                screen.blit(lives_label, (20, 20))
                game_state == "game"

            if player.lives == 0:
                y = player.rect.y + 25
                x = player.rect.x + 30
                print(x,y)
                blast = Explosion(x,y)
                blast_running = True

                while blast_running:

                    blast_finished = blast.update()

                    if blast_finished:
                        blast_running = False

                    # Draw
                    screen.blit(blast.image, blast.rect.topleft)
                    pygame.display.update()
                
                    game_state = "end"
                
                # If so, stop the loop
                running = False
    
                # Stop any moving sounds and play the collision sound
                move_up_sound.stop()
                move_down_sound.stop()
                collision_sound.play()

        # Check if any element in enemies collides with any shots element

        for enemy in  enemies:
            if pygame.sprite.spritecollide(enemy, shots,True):
                enemy.kill()
                player.score = player.score + 1

                break
                
        screen.blit(lives_label, (20, 20))
        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(30)

# The function to end or restart the game.

def end():
    global running, game_state
    move_up_sound.stop()
    move_down_sound.stop()
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    while running == False and game_state == "end":
        draw_end_menu()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                running = True
            
            if keys[pygame.K_n]:
                running = True

            if keys[pygame.K_y]:
                running = True
                game_state = "start_menu"

    return running, game_state
    
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spacecraft")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Instantiate player.
player = Player()
x = player.rect.x
y = player.rect.y

# Instantiate plasma ball
plasma_ball = Plasma_Ball(x,y)

# Instantiate shot
shot = Shot(x,y)

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
shots = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(plasma_ball)

# Load explosion images
explosion_images = []
for i in range(1,10):
    explosion_images.append(pygame.image.load(os.path.join('blast', 'blast_0{}.png'.format(i))).convert_alpha())

# Variable to control the state of the game
game_state = "start_menu"

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.wav")
move_down_sound = pygame.mixer.Sound("Falling_putter.wav")
collision_sound = pygame.mixer.Sound("Collision.wav")

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to control the state of the game
game_state = "start_menu"

# Variable to keep the main loop running
running = True

# Main loop

# A call to the function that starts the game

while running == True:

    if game_state == 'start_menu':
        start()
                    
    if game_state == "game":
        # Load background image
        background = pygame.image.load("space.png")

        # Load and play background music
        pygame.mixer.music.load("Apoxode_-_Electric_1.wav")
        pygame.mixer.music.play(loops=-1)

        play()

    if game_state == 'end':
        running, game_state = end()
        
        if running == True and game_state == "start_menu":

            # Define constants for the screen width and height
            SCREEN_WIDTH = 800
            SCREEN_HEIGHT = 600

            # Setup for sounds. Defaults are good.
            pygame.mixer.init()

            # Create the screen object
            # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Spacecraft")


            # Create a custom event for adding a new enemy
            ADDENEMY = pygame.USEREVENT + 1
            pygame.time.set_timer(ADDENEMY, 1000)

            # Instantiate player.
            player = Player()
            x = player.rect.x
            y = player.rect.y

            # Instantiate plasma ball.
            plasma_ball = Plasma_Ball(x,y)

            # Instantiate shot
            shot = Shot(x,y)

            # Load explosion images
            explosion_images = []
            for i in range(1,10):
                explosion_images.append(pygame.image.load(os.path.join('blast', 'blast_0{}.png'.format(i))).convert_alpha())

            # Instantite blast
            blast = Explosion(x,y)

            # Create groups to hold enemy sprites and all sprites
            # - enemies is used for collision detection and position updates
            # - all_sprites is used for rendering
            enemies = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            all_sprites.add(player)
            all_sprites.add(plasma_ball)

            # Load all sound files
            # Sound sources: Jon Fincher
            move_up_sound = pygame.mixer.Sound("Rising_putter.wav")
            move_down_sound = pygame.mixer.Sound("Falling_putter.wav")
            collision_sound = pygame.mixer.Sound("Collision.wav")

            # Setup the clock for a decent framerate
            clock = pygame.time.Clock()

            # Variable to keep the main loop running
            running = True
    
            start()
        else:
            break
    
pygame.quit()
# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
# Sound sources: Jon Fincher
