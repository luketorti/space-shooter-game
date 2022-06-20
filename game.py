# basic game elements
# set up pygame, random, and math
import pygame, random, math
pygame.init()

# caption
pygame.display.set_caption("Space Shooter Game")

# colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (220,20,60)
GREEN = (34,139,34)
PURPLE = (203, 0, 255)

# screen
size = (700,400)
screen = pygame.display.set_mode(size)

# start mixer
pygame.mixer.init()

# configure shooting sound
shoot_sound = pygame.mixer.Sound("shootingSound.wav")

# configure bomb sound
bomb_sound = pygame.mixer.Sound("bombDrop.wav")

# configure the clock
clock = pygame.time.Clock()

# background image
background_image = pygame.image.load("background.jpg").convert()

# classes
# player class
class Player(pygame.sprite.Sprite):
    # initialize player
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("playerSpaceship.png")
        self.rect = self.image.get_rect()
    # move player sprite with mouse    
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]-20
        self.rect.y = 340

# bullet class
class Bullet(pygame.sprite.Sprite):
    # initialize bullet
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 8])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
    # configure bullet movement
    def update(self):
        self.rect.y -= 6

# enemy bullet class
class EnemyBullet(pygame.sprite.Sprite):
    # initialize enemy bullet
    def __init__(self):
        super().__init__
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bomb.png") #(from https://simg.nicepng.com/png/small/154-1549731_pixel-bomb-pixel-monster-gif.png)
        self.rect = self.image.get_rect()
    # configure enemy bullet movement
    def update(self):
        self.rect.y +=2
       
# alien class
class Alien(pygame.sprite.Sprite):
    # initialize alien
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien.png") #(from https://opengameart.org/)
        self.rect = self.image.get_rect()
    # configure alien movement
    def update(self):
        self.rect.x += 1

# lists
allSprites = pygame.sprite.Group()
bulletList = pygame.sprite.Group()
enemyBulletList = pygame.sprite.Group()
alienList = pygame.sprite.Group()
alienHitList = []
playerHitList = pygame.sprite.Group()
player = Player()
allSprites.add(player)

# values
playerLives = 1
alienCounter = 0
count = 0
score = 0
bulletsFired = 1
aliensKilled = 1
alienBullet = 0
gameOver = False
gameOverCount = 0
done = False

# text
font = pygame.font.SysFont('Arial', 25, True, False)
gameOverFont = pygame.font.SysFont('Arial', 72, True, False)
gameOverText = gameOverFont.render("GAME OVER", True, WHITE)
thanksText = font.render("Thanks for playing!", True, WHITE)
creditText = font.render("Game made by Luke Torti", True, WHITE)

# main game loop
while done == False:

    # run clock at 60 fps
    clock.tick(60)

    # detect if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or playerLives == 0:
            done = True
        
        # bullet firing
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet()
            bullet.rect.x = player.rect.x+23
            bullet.rect.y = player.rect.y
            allSprites.add(bullet)
            bulletList.add(bullet)
            shoot_sound.play()
            bulletsFired += 1
            
    # alien deployment
    if alienCounter <= 199 and count == 80:
        alien = Alien()
        alien.rect.x = random.randrange(10)
        alien.rect.y = random.randrange(150)
        alienList.add(alien)
        allSprites.add(alien)
        alienCounter += 1
        count = 0 

    # alien bullet firing
    for alien in alienList:
        alienBullet += 0.5
        if alienBullet == 40:
            alien_bomb = EnemyBullet()
            alien_bomb.rect.x = alien.rect.x + 32
            alien_bomb.rect.y = alien.rect.y + 71
            allSprites.add(alien_bomb)
            enemyBulletList.add(alien_bomb)
            alienBullet = 0
            bomb_sound.play()

    # alien & player collision
    if pygame.sprite.spritecollide(player, enemyBulletList, True):
        playerHitList.add(player)
        for allies in playerHitList:
            gameOver = True
        

    # player shooting alien collision
    for bullet in bulletList:
        alienHitList = pygame.sprite.spritecollide(bullet, alienList, True)
        for alien in alienHitList:
            bulletList.remove(bullet)
            allSprites.remove(bullet)
            score += 1
            aliensKilled += 1
        
        # remove bullet from screen if alien is not hit
        if bullet.rect.y < -10:
            bulletList.remove(bullet)
            allSprites.remove(bullet)

    
    # make cursor invisible
    pygame.mouse.set_visible(False)
    
    # constantly update all sprites
    allSprites.update()

    # draw background
    screen.blit(background_image, [0,0])

    # draw sprites
    allSprites.draw(screen)

    # display score text
    scoreText = font.render("Score = "+str(score), 1, WHITE)
    screen.blit(scoreText, [580, 10])

    # display accuracy text
    accuracy = int((aliensKilled/bulletsFired)*100)
    accuracyText = font.render("Accuracy = "+str(accuracy), 1, WHITE)
    screen.blit(accuracyText, [490, 40])
    percent = font.render("%", 1, WHITE)
    screen.blit(percent, [675, 40])

    # update count
    count += 1

    # if gameOver, show end of game screen
    if gameOver == True:
        gameOverCount += 1
        screen.blit(background_image, [0,0])
        screen.blit(gameOverText, [128, 100])
        screen.blit(thanksText, [235, 180])
        screen.blit(creditText, [195, 360])
        screen.blit(scoreText, [290, 240])
        screen.blit(accuracyText, [250, 270])
        screen.blit(percent, [435, 270])

        pygame.mixer.stop()
        
        # close end of game screen and exit game after a few seconds 
        if gameOverCount == 200:
            playerLives = 0

    # update screen
    pygame.display.flip()

# quit when done is true
pygame.quit()