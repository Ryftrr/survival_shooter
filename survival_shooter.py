#Connor Ciccone
#Survival Shooter
#Description: requires pygame.  2d, on-rails, top-down shooter

'''
edits done by Ryan Cole -- ryftrr@gmail.com
version alpha 1.0.1
'''

import pygame, sys, math, random

#initialize game engine
pygame.init()

#Set up drawing surface
w = 800
h = 700
size = (w, h)
surface = pygame.display.set_mode(size)

#set window title bare
pygame.display.set_caption("Survive")

#game logic constants
NEWENEMY = 120
WALKERHEALTH = 3
SNIPERHEALTH = 1

SPEED = 4
ENEMYSPEED = 1

BULLETSPEED = 8
FIRERATE = 60
DAMAGE = 20

#Color Constants
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE = (  0,  0,255)
LTGREEN = (67, 189, 56)
CYAN = (89, 212, 234)
YELLOW = (255, 255, 0)
GREY = (40,40,40)
RED = (255,0,0)
BROWN = (244, 164, 96)
GRAY = (122, 122, 122)
BACKGROUND = (37,122,22)

'''
Images and other constants
'''
#player image came from https://dribbble.com/shots/1767480-Shooter-Shotgun-Boy-Game-Character-Sprites
unscaledplayerimage = pygame.image.load("player.png")
PLAYERIMAGE = pygame.transform.scale(unscaledplayerimage, (80,60))

#walker picture came from https://www.chupamobile.com/ui-graphic-asset/zombies-2d-game-character-sprites-14902
unscaledwalker = pygame.image.load("enemy.png")
WALKER = pygame.transform.scale(unscaledwalker, (64, 80))

#sniper picture came from https://www.traxx.shoes/science-service-results/oct-21-2nd-annual-zombies-coming-5k/
unscaledsniper = pygame.image.load("sniper.png")
SNIPER = pygame.transform.scale(unscaledsniper, (63, 75))

clock = pygame.time.Clock()

#-----------------Main Program Loop ----------------

#draws rails player moves on
def drawBackground():
    pygame.draw.rect(surface, BLACK, (0, h/2-h/6, w, h/3))
    pygame.draw.rect(surface, YELLOW, (0, h/2 - h/144, w, h/72), 0)
    

#draws the bullets that move up the screen
def drawBullets(bullets, possession):
    for bullet in bullets:
        if possession == False:
            pygame.draw.rect(surface, WHITE, bullet[0])
        else:
            pygame.draw.rect(surface, RED, bullet[0])
        
    

#draws out the enemies that the player targets
def drawEnemies(enemies):
    for enemy in enemies:
        if enemy[2] == "walker":
            surface.blit(WALKER, enemy[0])
        elif enemy[2] == "sniper":
            surface.blit(SNIPER, enemy[0])
        
    

#draws player health bar
def drawHealthBar(health):
    healthrect = pygame.Rect(0,0,health,h/20)
    healthtext, healthbounds = showMessage("Health", 24, "Arial", healthrect.centerx , healthrect.centery, WHITE)
    
    pygame.draw.rect(surface, WHITE, (0,0,w,h/18), 0)
    if health>0:
        pygame.draw.rect(surface, RED, healthrect, 0)
    surface.blit(healthtext, healthbounds)
    
#shows the score of the player
def drawScore(score):
    string = "Score: " + str(score)
    scoretext, scorebounds = showMessage(string, 24, "Arial", w/8, h/14, BLUE)
    return scoretext, scorebounds

#gives the bounds and text to display a message
def showMessage(words, size, font, x, y, color, bg = None):
    text_font = pygame.font.SysFont(font, size, True, False)
    text = text_font.render(words, True, color, bg)
    textBounds = text.get_rect()
    textBounds.center = (x, y)    
    
    #return bounding rectangle for click detection
    return text, textBounds

#draws entirety of the scene currently in play including enemies, bullets, the position and angle of the player, and the health bar
def drawScene(playerrect, playerimage, bullets, enemybullets, enemies, health, gameOver, initiated, score):

    drawBackground()
    drawBullets(bullets, False)
    drawBullets(enemybullets, True)
    drawEnemies(enemies)
    drawHealthBar(health)
    scoretext, scorebounds = drawScore(score)
    surface.blit(scoretext, scorebounds)
    surface.blit(playerimage, playerrect)
    if gameOver:
        if initiated:
            endtext, endbounds = showMessage("You Died.", 48, "Arial", w/2, h/2, BLUE)
            replaytext, replaybounds = showMessage("Press Enter to Play Again", 24, "Arial", w/2, 3 * h/4, BLUE)
            surface.blit(replaytext, replaybounds)
            surface.blit(endtext, endbounds)
        else:
            replaytext, replaybounds = showMessage("Press Enter to Play", 24, "Arial", w/2,h/4, RED, BLACK)
            instructline1, instructbounds1 = showMessage("Press Space To Shoot And The Arrows To Move", 24, "Arial", w/2, h/2, RED, BLACK)
            instructline2, instructbounds2 = showMessage("Press A To Rotate Clockwise And D To Rotate Counter Clockwise", 24, "Arial", w/2, 3*h/5, RED, BLACK)
            instructline3, instructbounds3 = showMessage("You lose whenever you run out of health.", 24, "Arial", w/2, 7 * h/10, RED, BLACK)
            instructline4, instructbounds4 = showMessage("You lose health by getting shot or touching enemies.", 24, "Arial", w/2, 8*h/10, RED, BLACK)
            surface.blit(instructline1, instructbounds1)
            surface.blit(instructline2, instructbounds2)
            
            surface.blit(instructline4, instructbounds4)
            surface.blit(instructline3, instructbounds3)
            surface.blit(replaytext, replaybounds)
        
    

#makes sure player isn't out of bounds
def collisionCheck(rectangle):
    
    if rectangle.right>w:
        rectangle.right = w
    elif rectangle.left<0:
        rectangle.left = 0
    
    if rectangle.top<h/19:
        rectangle.top = h/19 + 1
    elif rectangle.bottom>h:
        rectangle.bottom = h-1
    return rectangle

#moves player left and right along provided rails as long as player is not out of bounds of game
def movePlayer(keys, player):
    if keys[pygame.K_LEFT]:
        player.left -= SPEED
        player = collisionCheck(player)
    if keys[pygame.K_RIGHT]:
        player.left += SPEED
        player = collisionCheck(player)
    if keys[pygame.K_UP]:
        player.top -= SPEED
        player = collisionCheck(player)
    if keys[pygame.K_DOWN]:
        player.top += SPEED
        player = collisionCheck(player)

    return player

#creates a bullet to be added to the list of bullets currently on the screen
def makeBullet(playerrect, theta):
    #all bullets are defined as a list of their rectangle object followed by the trajectory/speed they have in each direction, x first then y
    #using vectors to angle the bullets properly
    thetarad = theta*math.pi/180
    #the addition and stuff for the starting point of the bullets is just to make bullet spawns look a bit nicer
    bullet = [pygame.Rect(playerrect.centerx+playerrect.width/2, playerrect.centery + playerrect.height/2, 10, 10), BULLETSPEED*math.sin(thetarad), BULLETSPEED*math.cos(thetarad)]
    return bullet

#moves all bullets based on their trajectory vector
def moveBullets(bullets):

    for bullet in bullets:
        bullet[0].top += bullet[2]
        bullet[0].right += bullet[1]

    return bullets

'''
when bullets fall off screen, so as to avoid an overload error, the bullets are removed
also removes bullets if they collide with an enemy
removes enemy bullets if they collide with player and damages player
based on if the bullets are from the player or the enemies
'''
def removeBullets(bullets, enemies, player, health, playerrect):
    #bullets are giving random errors, good way to try and see if this will fix the problem
    try:
        for bullet in bullets:
            
            if bullet[0].top>h or bullet[0].bottom<0:
                bullets.remove(bullet)
            
            if bullet[0].left>w or bullet[0].right<0:
                bullets.remove(bullet)
            if player:    
                for enemy in enemies:
                    
                    
                    if bullet[0].colliderect(enemy[0]):
                        bullets.remove(bullet)
                        enemy[1] -= 1
                        
                    
                        
            if not player:
                if bullet[0].colliderect(playerrect):
                    bullets.remove(bullet)
                    health -= DAMAGE
    except:
        removeBullets(bullets, enemies, player, health, playerrect)
    return bullets, enemies, health

#spawns a new enemy based on playerlocation
def createEnemy(player, radius):    
    
    sides = ["top", "bottom"]
    etype = random.choice(["sniper", "walker", "walker", "walker", "walker", "walker", "walker"])
    side = random.choice(sides)
    if side == "top":
        #to avoid having the player go up the screen, which leads an enemy to spawn in a negative range, use try except to change the side if this becomes a problem
        try:
            if etype == "walker":
                enemy = [pygame.Rect(random.randint(0, w-80), random.randint(h/19, player.top-radius), 64, 80), WALKERHEALTH, etype]
            if etype == "sniper":
                enemy = [pygame.Rect(random.randint(0, w-80), random.randint(h/19, player.top-radius), 63, 75), SNIPERHEALTH, etype]
        except:
            side = "bottom"
    if side == "bottom":
        #same situation as the above try except
        try:
            if etype == "walker":
                enemy = [pygame.Rect(random.randint(0, w-80), random.randint(0, player.bottom+radius), 64, 80), WALKERHEALTH, etype]
            if etype == "sniper":
                enemy = [pygame.Rect(random.randint(0, w-80), random.randint(0, player.bottom+radius), 63, 75), SNIPERHEALTH, etype]
       
        except:
            if etype == "walker":
                enemy = [pygame.Rect(random.randint(0, w-80), random.randint(h/19, player.top-radius), 64, 80), WALKERHEALTH, etype]
            if etype == "sniper":
                enemy = [pygame.Rect(random.randint(0, w-80), random.randint(h/19, player.top-radius), 63, 75), SNIPERHEALTH, etype]            
    return enemy

#removes enemies whenever their health (second number) is 0
def removeEnemies(enemies, score):
    for enemy in enemies:
        if enemy[1] == 0:
            enemies.remove(enemy)
            #logic for player score
            if enemy[2] == "sniper":
                score += 150
            else:
                score += 100
    return enemies, score

#AI for enemies to move towards player at all times
def moveEnemies(enemies, player):
    #loops through list of enemies and alters each x and y value to move it closer to the player's x and y values by a constant speed, making them collide so the life check function works properly
    for enemy in enemies:
        if enemy[2] == "walker":
            if enemy[0].centery>=player.centery:
                enemy[0].top -= ENEMYSPEED
            elif enemy[0].centery<=player.centery:
                enemy[0].bottom += ENEMYSPEED
            if enemy[0].left>=player.right:
                enemy[0].left -= ENEMYSPEED
            elif enemy[0].right<=player.left:
                enemy[0].right += ENEMYSPEED
    #preventing the enemies rectangles from being directly on top of each other to avoid glitching out the game
    for enemy in enemies:
        for enemy2 in enemies:
            if enemy2 != enemy:
                if enemy[0].top == enemy2[0].top and enemy[0].left == enemy2[0].left:
                    enemy2[0].left = enemy[0].right
    return enemies

#for the snipers, it fires a red bullet based on some trig to get the angle
def shootPlayer(shooters, player, enemybullets):
    bullet = []
    
    for i in range(len(shooters)):
        
        dx = player.centerx - shooters[i][0].centerx
        dy = player.centery - shooters[i][0].centery
        #have to make sure we don't divide by 0
        if dy != 0 and dx!=0:
            angle = math.atan(dy/dx)
    
        #if angle is in third quadrant
        if dx<0 and dy>0:
        
            angle += math.pi
        #if angle is in second quadrant fix it so the x and y components of the velocity register properly
        if dx<0 and dy<0:
       
            angle+= math.pi
        
        bullet = [pygame.Rect(shooters[i][0].centerx, shooters[i][0].centery, 10, 10), BULLETSPEED*math.cos(angle), BULLETSPEED*math.sin(angle)]
        enemybullets.append(bullet)
           
    return enemybullets

#since the shootPlayer function only returns a bullet if a sniper is on the screen, I check for whether or not a sniper is on the screen, and return that to run shootPlayer
def sniperCheck(enemies):
    for enemy in enemies:
        if enemy[2] == "sniper":
            return True
    return False

#there's a glitch in shootPlayer where only one sniper will fire at a given time, so to remedy that I'm adding this function
#purpose is to return a list of snipers to loop through and create bullets
def findSnipers(enemies):
    shooters = []
    #loops through all possible enemies that have the ability to fire and puts them in a list
    for enemy in enemies:
        if enemy[2] == "sniper":
            shooters.append(enemy)
    return shooters

#health counter, determining when the game ends based on how much health the player has
def healthCheck(health, player, enemies):
    for enemy in enemies:
        if enemy[0].colliderect(player):
            health -= 1
    return health

'''
rotation logic for rotating player image.
instead of using a point list because that's too long, I will use a rectangle separate from the one that I use to spawn the image to determine collisions
rotates player image
'''
def rotatePlayer(theta, keys):
    thetarad = theta*180/math.pi
    if keys[pygame.K_a]:
        theta -= 2     
    if keys[pygame.K_d]:
        theta += 2    
    playerimage = pygame.transform.rotate(PLAYERIMAGE, theta)
    theta = theta%360
   
    return theta, playerimage

#because it's nice to have a main function
def main():
    #important variables
    #playerrect is the rectangle used to check player collision
    playerrect = pygame.Rect(w/2, h/2-20, 80, 60)
    #theta is the value the playerimage is rotated by which is used to vector bullet velocity
    theta = 0
    #image of player that gets modified by angle
    playerimage = PLAYERIMAGE
    #list of bullets
    bullets = []
    #list of enemybullets
    enemybullets = []
    #list of enemies
    enemies = []
    gameOver = True
    #to check if the instructions have already been given
    initiated = False
    #how much health player has
    health = w
    #counters are great for checking things
    counter = 0
    #are snipers on the board?
    snipers = False
    #all the snipers on the board
    shooters = []
    score = 0
    while(True):
        if not gameOver:
            #movement and rotation logic for player as long as the game is not over
            keys = pygame.key.get_pressed()
            playerrect = movePlayer(keys, playerrect)
            theta, playerimage = rotatePlayer(theta, keys)
            
        for event in pygame.event.get():
            if( event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()
        # game logic goes here

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(makeBullet(playerrect, theta))
                if event.key == pygame.K_RETURN:
                    gameOver = True
            if gameOver:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        health = w
                        counter = 0
                        snipers = False
                        shooters = []
                        playerrect = pygame.Rect(w/2, h/2-20, 40, 40)
                        theta = 0
                        direction = "top"
                        playerimage = PLAYERIMAGE
                        bullets = []
                        enemybullets = []
                        enemies = []
                        gameOver = False 
                        score = 0
                        initiated = True

        if not gameOver:
            #bullet logic for enemies and player
            
            snipers = sniperCheck(enemies)
            
            if snipers:
                #in order to avoid just spawning a really long bullet, it only spawns them on intervals based on the enemy firerate
                if counter%FIRERATE == 0:
                    shooters = findSnipers(enemies)
                    
                    enemybullets = shootPlayer(shooters, playerrect, enemybullets)
            #so long as enemy bullets isn't empty move the bullets of the enemies
            if len(enemybullets) != 0:
                enemybullets = moveBullets(enemybullets)
            bullets = moveBullets(bullets)
            
            
            bullets, enemies, health = removeBullets(bullets, enemies, True, health, playerrect)
            #enemy spawns logic
            counter += 1
            if counter%NEWENEMY == 0:
                enemies.append(createEnemy(playerrect, h*.15))
            #player score goes up by 50 
            if counter%600 == 0:
                score += 50
            enemybullets, enemies, health = removeBullets(enemybullets, enemies, False, health, playerrect)
           #if enemies have no health remove them
            enemies, score = removeEnemies(enemies, score)
            #moves the walker enemy type across the screen
            enemies = moveEnemies(enemies, playerrect)
            #how long player has been colliding with the enemy affects how much health lost
            health = healthCheck(health, playerrect, enemies)
            #player health logic
            if health<=0:
                gameOver = True
        
        #SET BACKGROUND FILL
        surface.fill(BACKGROUND)        
        #drawing code goes here
        drawScene(playerrect, playerimage, bullets, enemybullets, enemies, health, gameOver, initiated, score)
        clock.tick(60)
        pygame.display.update()
main()