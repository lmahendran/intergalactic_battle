## Logesh Mahendran
## Space Battle Modification - Summative Assignment
## Mr. Bratberg - ICD2O
## Last updated: January 23rd, 2024
# PLEASE PLAY ON 800x600.
## Description: This is my modification of the original "Space Battle" game. There are three levels you can play, as well as an option to see more details on how the game works and the option to switch controls. The goal is to eliminate all the enemies by shooting bullets at them. The 7 major modifications are:
# - Removing wait time for bullets
# - A starting screen with a play button
# - Options to replay or continue after winning or losing a battle
# - A second level with different sprites and backgrounds
# - A third level, which is a boss level with new attacks and movements
# - Three power ups that provide the player with boosts for some time
# - Additions to the starting screen (How to Play and Options)

## MODULES
import pygame
import math
import os
import sys
from time import sleep
from random import randint

# Initialize the pygame
pygame.init()
clock = pygame.time.Clock()
FPS = 300 # Speeds are in pixels per frame, so this sets how fast the game plays

# Image folder (found relative to this file, so the game runs from any directory)
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"assets","images")

# Image Loading Function (folder is backgrounds, sprites, powerups or ui)
def load_image(folder,name):
  return pygame.image.load(os.path.join(IMAGE_DIR,folder,name))

# Icon Cropping Function (removes empty space around the image, keeping it square)
def crop_icon(image):
  shipArea = image.get_bounding_rect() # Smallest rectangle containing visible pixels
  size = max(shipArea.width,shipArea.height)
  croppedIcon = pygame.Surface((size,size),pygame.SRCALPHA)
  croppedIcon.blit(image,((size-shipArea.width)//2,(size-shipArea.height)//2),shipArea)
  return croppedIcon

# Screen setup (screen, title and icon)
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Intergalactic Battle")
icon = crop_icon(load_image("ui","icon.png"))
pygame.display.set_icon(icon)

## FUNCTIONS

# Quit Function (closes the game if the window's X button is clicked)
def check_quit(event):
  if event.type == pygame.QUIT:
    pygame.quit()
    sys.exit()

# Starting Screen Function
def starting_screen():
  startingScreen = load_image("backgrounds","starting_screen.png")
  startingFont = pygame.font.Font('freesansbold.ttf',56)
  startingText = startingFont.render("INTERGALACTIC BATTLE",True,(255,255,255))
  howToPlayButton = load_image("ui","how_to_play.png") 
  optionsButton = load_image("ui","options.png")
  global keys
  keys = [pygame.K_LEFT,pygame.K_RIGHT,pygame.K_SPACE]
  started = False

  # Display the options on the menu
  while not started:
    screen.blit(startingScreen,(0,0))
    screen.blit(startingText,(45,90))
    pygame.draw.circle(screen,(255,255,255),(400,300),60,0)
    pygame.draw.circle(screen,(0,0,0),(400,300),60,5)
    pygame.draw.polygon(screen,(0,0,0),((380,275),(380,325),(430,300)))
    screen.blit(howToPlayButton,(300,420))
    screen.blit(optionsButton,(325,480))

    # Check if mouse is clicked
    for event in pygame.event.get():
      check_quit(event)
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouseClickX, mouseClickY = get_latest_click()
        if math.pow(mouseClickX-400,2) + math.pow(mouseClickY-300,2) <= 3600: #Equation of the play button circle
          started = True

        # If "How to Play" clicked
        elif mouseClickX > 300 and mouseClickX < 500 and mouseClickY > 420 and mouseClickY < 470:
          understood = False
          gameDescriptionText = []
          gameDescriptionFont = pygame.font.Font("freesansbold.ttf",24)
          gameDescriptionText.append("Welcome to Intergalactic Battle. In this game, you will travel")
          gameDescriptionText.append("through space to battle 3 different sets of enemies. You can only")
          gameDescriptionText.append("move right to left, and you can press space to shoot bullets.")
          gameDescriptionText.append("You may change these controls at the start, in the Options Menu.")
          gameDescriptionText.append("You unlock power ups as you progress through the levels, which")
          gameDescriptionText.append("must be clicked in order to activate their boost for 10 seconds.")
          gameDescriptionText.append("The power ups give boosts of speed, bullet speed and invincibility.")
          gameDescriptionText.append("The last level contains a great challenge, so goodluck!")
          gameDescriptionText.append("- Logesh")
          gameDescriptionText.append(" ")
          gameDescriptionText.append("[CLICK TO CONTINUE]")
          screen.fill((0,0,0))
          for i in range(len(gameDescriptionText)):
            text = gameDescriptionFont.render(gameDescriptionText[i],True,(255,255,255))
            screen.blit(text,(5,30*i+150))
          pygame.display.update()
          understood = False
          while not understood:
            clock.tick(FPS)
            for event in pygame.event.get():
              check_quit(event)
              if event.type == pygame.MOUSEBUTTONDOWN:
                understood = True

        # If "Options" clicked
        elif mouseClickX > 325 and mouseClickX < 475 and mouseClickY > 480 and mouseClickY < 530:
          optionsFont = pygame.font.Font("freesansbold.ttf",33)
          keys = []
          keySet = False
          while not keySet:
            if len(keys) == 0:
              text = optionsFont.render("Please press the key you would like to move left:",True,(255,255,255))
            elif len(keys) == 1:
              text = optionsFont.render("Please press the key you would like to move right:",True,(255,255,255))
            elif len(keys) == 2:
              text = optionsFont.render("Please press the key you would like to shoot:",True,(255,255,255))
            defaultControlsText = optionsFont.render("Click the screen for default controls",True,(255,255,255))
            screen.fill((0,0,0))
            screen.blit(text,(10,280))
            screen.blit(defaultControlsText,(100,320))
            pygame.display.update()
            clock.tick(FPS)
            keySet = False
            for event in pygame.event.get():
              check_quit(event)
              if event.type == pygame.KEYDOWN:
                keys.append(event.key)
              if event.type == pygame.MOUSEBUTTONDOWN:
                keys = [pygame.K_LEFT,pygame.K_RIGHT,pygame.K_SPACE]
            if len(keys) == 3:
              keySet = True
            
    pygame.display.update()
    clock.tick(FPS)
  return keys

# Battle End Function
def battle_end(status):
  gameEnd_font = pygame.font.Font('freesansbold.ttf',64)
  tryAgainImg = pygame.transform.scale(load_image("ui","try_again.png"),(150,75))
  playAgainImg = pygame.transform.scale(load_image("ui","play_again.png"),(150,75))
  continueImg = pygame.transform.scale(load_image("ui","continue.png"),(150,75))
  screen.fill((0,0,0))
  choice = "none"

  # Display the choices for either winning or losing
  while choice == "none":
    if status == "won":
      text = gameEnd_font.render("YOU WON",True,(255,255,255))
      screen.blit(text,(225,200))
      screen.blit(playAgainImg,(200,350))
      screen.blit(continueImg,(450,350))
    else:
      text = gameEnd_font.render("GAME OVER",True,(255,255,255))
      screen.blit(text,(200,200))
      screen.blit(tryAgainImg,(325,350))

    # Detect mouse clicks on the options
    for event in pygame.event.get():
      check_quit(event)
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouseClickX, mouseClickY = get_latest_click()
        if status == "won":
          if mouseClickX > 200 and mouseClickX < 350 and mouseClickY > 350 and mouseClickY < 425:
            choice = "play again"
          if mouseClickX > 450 and mouseClickX < 600 and mouseClickY > 350 and mouseClickY < 425:
            choice = "continue"
        else:
          if mouseClickX > 325 and mouseClickX < 475 and mouseClickY > 350 and mouseClickY < 425:
            choice = "play again"
            
    pygame.display.update()
    clock.tick(FPS)

  return choice
  
# Game End FUnction
def game_end():
  returnToMenu = False
  while not returnToMenu:
    thankYouFont = pygame.font.Font('freesansbold.ttf',48)
    thankYouMessage = thankYouFont.render("Thank you for playing!",True,(255,255,255))
    screen.fill((0,0,0))
    screen.blit(thankYouMessage,(150,260))
    for event in pygame.event.get():
      check_quit(event)
      if event.type == pygame.MOUSEBUTTONDOWN:
        returnToMenu = True

    pygame.display.update()
    clock.tick(FPS)

# Score and Enemy Count Function
def show_score(score,count,bossMode,health,boost,powerUpNum):
  scoreFont = pygame.font.Font('freesansbold.ttf',32)
  boostFont = pygame.font.Font('freesansbold.ttf',16)
  scoreText = scoreFont.render("Score: " + str(score),True,(255,255,255))
  countText = scoreFont.render("Enemies left: " + str(count),True,(255,255,255))
  screen.blit(scoreText,(10,10))
  if not bossMode:
    screen.blit(countText,(10,50))
  else:
    bossHPText = scoreFont.render("BOSS HP: " + str(health),True,(255,255,255))
    pygame.draw.rect(screen,(255,0,0),pygame.Rect(100,570,600,10))
    pygame.draw.rect(screen,(0,255,0),pygame.Rect(100,570,health*6,10))
    screen.blit(bossHPText,(300,530))
  if boost:
    if powerUpNum == 1:
      boostText = boostFont.render("Current boost: +50% Player Speed",True,(255,255,255))
    elif powerUpNum == 2:
      boostText = boostFont.render("Current boost: +50% Bullet Speed",True,(255,255,255))
    elif powerUpNum == 3:
      boostText = boostFont.render("Current boost: Invincibility",True,(255,255,255))
    screen.blit(boostText,(10,580))

# Block Events Function
def block_events(events):
  for i in range(len(events)):
    pygame.event.set_blocked(events[i])

# Player Function
def player(sprite,x,y):
  screen.blit(sprite,(x,y))

# Enemy Function
def enemy(sprite,x,y,i):
  screen.blit(sprite,(x,y))

# Bullet Function
def fire_bullet(sprite,x,y):
  screen.blit(sprite,(x+10,y+10))

# Boss Bullet Function
def boss_bullet(sprite,x,y):
  screen.blit(sprite,(x,y))

# Power Up Function
def power_up(sprite,x,y):
  screen.blit(sprite,(x,y))

# Collision Function
def is_collision(enemyX,enemyY,bulletX,bulletY,hitbox):
  distance = math.sqrt(math.pow((enemyX+(hitbox/2))-(bulletX-4),2) + math.pow(enemyY-bulletY,2)) #Length formula between two coordinates
  if distance < (hitbox/2):
    return True
  else:
    return False

# Player Collision Function (for the boss)
def player_collision(playerX,playerY,bossBulletX,bossBulletY):
  distance = math.sqrt(math.pow((playerX+16)-bossBulletX-6,2) + math.pow(playerY-bossBulletY,2))
  if distance < 16:
    return True
  else:
    return False

# Click Function
def get_latest_click():
  if pygame.mouse.get_pressed():
    mouseClickX,mouseClickY = pygame.mouse.get_pos() #Assigns the mouse's X and Y to two variables
    return mouseClickX, mouseClickY

# Battle Function
def battle(background,sprite,count,enemySpeed,spawnRange1,spawnRange2,bossMode,health,hitbox,battleNumber):
  
  # Startup
  score = 0
  font = pygame.font.Font('freesansbold.ttf',64)
  screen.fill((0,0,0))
  if battleNumber == 1:
    introText = font.render("UFO Mania",True,(128,128,128))
    screen.blit(introText,(210,200))
  elif battleNumber == 2:
    introText = font.render("Blimp Outbreak",True,(128,128,128))
    screen.blit(introText,(175,200))
  elif battleNumber == 3:
    introText = font.render("Weird Waveforms",True,(128,128,128))
    screen.blit(introText,(150,200))
  elif battleNumber == 4:
    introText = font.render("8-Bit Blaster",True,(128,128,128))
    screen.blit(introText,(200,200))
  pygame.display.update()
  sleep(2)
  
  # Player Setup
  playerSprite = load_image("sprites","player_1.png")
  playerSprite = pygame.transform.scale(playerSprite,(32,32))
  playerSprite = pygame.transform.rotate(playerSprite,180)
  playerX = 384
  playerY = 480
  playerX_change = 0
  mouseClickX = 0
  mouseClickY = 0
  
  # Enemy Setup
  enemySprite = []
  enemyX = []
  enemyY = []
  enemyX_change = []
  enemyY_change = []
  enemyHealth = []
  enemyState = []
  numEnemies = count
  enemyDirection = []
  enemyBaseY = []

  # Create all the enemies
  for i in range(numEnemies):
    enemySprite.append(sprite)
    enemyX.append(randint(2,670))
    enemyY.append(randint(spawnRange1,spawnRange2))
    enemyX_change.append(enemySpeed)
    enemyY_change.append(0)
    enemyHealth.append(health)
    enemyState.append("alive")
    enemyDirection.append(1)
    if battleNumber == 3:
      enemyBaseY.append(randint(spawnRange1,spawnRange2))
  
  # Bullet Setup
  # Moving - Bullet is currently moving
  # Hit - Bullet reached the edge or hit an enemy
  bulletSprite = []
  bulletX = []
  bulletY = []
  bulletY_change = []
  bullet_state = []
  numBullets = 0

  # Boss Bullet Setup
  if bossMode:

    # Create custom user events
    BOSSATTACK = pygame.USEREVENT + 1
    INCREASEBULLETS = pygame.USEREVENT + 2
    pygame.event.set_allowed(BOSSATTACK)
    pygame.event.set_allowed(INCREASEBULLETS)
    pygame.time.set_timer(BOSSATTACK,5000)
    pygame.time.set_timer(INCREASEBULLETS,10000)
    
    bossBulletSprite = []
    bossBulletX = []
    bossBulletY = []
    bossBulletY_change = []
    bossBulletState = []
    bossIndicator = pygame.transform.rotate(pygame.transform.scale(load_image("sprites","boss_bullet.png"),(8,8)),180)
    bossIndicatorX = [0,0]
    bossAttackPhase = 0
    numBossBullets = 1

  # Power Ups
  fasterSpeed = pygame.transform.scale(load_image("powerups","player_speed.png"),(40,40))
  fasterBullet = pygame.transform.scale(load_image("powerups","bullet_speed.png"),(40,40))
  tempShield = pygame.transform.scale(load_image("powerups","temp_shield.png"),(40,40))
  SPAWNPOWERUP = pygame.USEREVENT + 3
  ENDBOOST = pygame.USEREVENT + 4
  pygame.event.set_allowed(SPAWNPOWERUP)
  pygame.time.set_timer(SPAWNPOWERUP,30000)
  powerUpSpawned = False
  boost = False
  powerUpNum = 0
  playerXBoost = 1
  bulletYBoost = 1
  tempInvincible = False

  
  # Battle Loop
  running = True
  while running:
    
    # Draw Background Image
    screen.blit(background,(0,0))

    # Event Checking
    for event in pygame.event.get():
      check_quit(event)

      # Player events
      if event.type == pygame.KEYDOWN:
        if event.key == keys[0]:
          playerX_change = -0.8
        if event.key == keys[1]:
          playerX_change = 0.8
        if event.key == keys[2]:
          numBullets += 1
          bulletSprite.append(pygame.transform.rotate(pygame.transform.scale(load_image("sprites","bullet.png"),(20,8)),90))
          bulletX.append(0)
          bulletY.append(480)
          bulletY_change.append(3)
          bullet_state.append("moving")
          bulletX[-1] = playerX #len(bulletY) just represents the most recently added bullet
          bulletY[-1] = playerY
          fire_bullet(bulletSprite[-1],bulletX[-1],bulletY[-1])
  
      # When player lifts up a key
      if event.type == pygame.KEYUP:
        if event.key == keys[0] or event.key == keys[1]:
          playerX_change = 0

      # If mouse is clicked
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouseClickX, mouseClickY = get_latest_click()

      # Spawn power up
      if event.type == SPAWNPOWERUP:
        powerUpNum = randint(1,min(battleNumber,3)) # Only 3 power ups exist
        powerUpX = randint(100,760)
        powerUpY = randint(30,560)
        powerUpSpawned = True
        if powerUpNum == 1:
          powerUpSprite = fasterSpeed
        elif powerUpNum == 2:
          powerUpSprite = fasterBullet
        elif powerUpNum == 3:
          powerUpSprite = tempShield
        pygame.event.set_blocked(SPAWNPOWERUP)

      # End any power up boosts running
      if event.type == ENDBOOST:
        boost = False
        powerUpNum = 0
        pygame.event.set_allowed(SPAWNPOWERUP)
        pygame.time.set_timer(SPAWNPOWERUP,30000)
        pygame.event.set_blocked(ENDBOOST)
      
      # Boss Events
      if bossMode:

        # Increase Boss Bullets Event
        if event.type == INCREASEBULLETS:
          numBossBullets += 1
          pygame.time.set_timer(INCREASEBULLETS,10000)

        # Boss Special Attack Event
        if event.type == BOSSATTACK:
          if bossAttackPhase != 1 and ("moving" not in bossBulletState):
            bossBulletSprite.clear()
            bossBulletX.clear()
            bossBulletY.clear()
            bossBulletY_change.clear()
            bossBulletState.clear()
            bossAttackPhase = 1
            pygame.time.set_timer(BOSSATTACK,3000)
          elif bossAttackPhase == 1:
              bossAttackPhase = 2
              bossBulletCount = numBossBullets
              if bossBulletCount > 10:
                randomBulletSpeeds = True
              else:
                randomBulletSpeeds = False
              if bossBulletCount > 20:
                bossBulletCount = 20
              speedMultiplier = 1+(0.01*bossBulletCount)
              bossBulletX.append(playerX+10)
              for i in range(bossBulletCount):
                bossBulletSprite.append(pygame.transform.rotate(pygame.transform.scale(load_image("sprites","boss_bullet.png"),(12,32)),180))
                bossBulletY.append(0)
                if randomBulletSpeeds:
                  bossBulletY_change.append(round((randint(10,20))/10*speedMultiplier,4))
                else:
                  bossBulletY_change.append(1*speedMultiplier)
                bossBulletState.append("moving")
              for i in range(bossBulletCount-1):
                bossBulletX.append(randint(2,786))
          pygame.time.set_timer(BOSSATTACK,randint(1000,5000))

    # Enemy Movement
    for i in range(numEnemies):
      enemyX[i] += enemyX_change[i] * enemyDirection[i]
      enemyY[i] += enemyY_change[i]
      if battleNumber == 3:
        enemyY[i] =  20*math.cos(math.radians(2*enemyX[i])) + enemyBaseY[i]
        # enemyX_change[i] = randint(10,20)/10
      if bossMode:
        if enemyX[i]+32 > playerX:
          enemyX_change[i] = -0.5
        elif enemyX[i]+32 < playerX:
          enemyX_change[i] = 0.5
        elif enemyX[i]+32 == playerX:
          enemyX_change[i] = 0
      else:
        if enemyX[i] < 0 or enemyX[i] > (800-hitbox):
          enemyDirection[i] *= -1
          enemyY_change[i] = 30
          if battleNumber == 3:
            enemyBaseY[i] += 30
          enemySprite[i] = pygame.transform.flip(enemySprite[i],1,0)
        else:
          enemyY_change[i] = 0
      
      # Enemy Collision
      for j in range(numBullets):
        collision = is_collision(enemyX[i],enemyY[i],bulletX[j],bulletY[j],hitbox)
        if collision:
          bullet_state[j] = "hit"
          if bossMode:
            score += 10
          else:
            score += 1
          enemyHealth[i] -= 1
          enemyX[i] = randint(2,800-hitbox-2)
          if battleNumber == 3:
            enemyBaseY[i] -= 30
            if enemyBaseY[i] < 50:
              enemyBaseY[i] = 50
          else:
            enemyY[i] -= 30
            if enemyY[i] < 50:
              enemyY[i] = 50
            
      # Enemy Checking
      if enemyY[i] > 400:
        block_events([SPAWNPOWERUP,ENDBOOST])
        gameState = "lost"
        running = False
      if enemyHealth[i] < 1:
        enemyState[i] = "dead"
      enemy(enemySprite[i],enemyX[i],enemyY[i],i)
    
    # Check if enemies are dead, then entirely remove them from the game
    if "dead" in enemyState:
      deadEnemy = enemyState.index("dead")
      enemySprite.pop(deadEnemy)
      enemyX.pop(deadEnemy)
      enemyY.pop(deadEnemy)
      enemyX_change.pop(deadEnemy)
      enemyY_change.pop(deadEnemy)
      enemyHealth.pop(deadEnemy)
      enemyState.pop(deadEnemy)
      enemyDirection.pop(deadEnemy)
      if battleNumber == 3:
        enemyBaseY.pop(deadEnemy)
      numEnemies -= 1
  
    # Bullet Movement
    for i in range(numBullets):
      bulletY[i] -= round(bulletY_change[i]*bulletYBoost,2)
      if bulletY[i] < -5:
        bullet_state[i] = "hit"
      fire_bullet(bulletSprite[i],bulletX[i],bulletY[i])

    # Check if bullet hits the edge or an enemy, then delete the bullet
    if "hit" in bullet_state:
      deadBullet = bullet_state.index("hit")
      bulletSprite.pop(deadBullet)
      bulletX.pop(deadBullet)
      bulletY.pop(deadBullet)
      bulletY_change.pop(deadBullet)
      bullet_state.pop(deadBullet)
      numBullets -= 1

    # Power Up Collection
    if powerUpSpawned:
      if mouseClickX < powerUpX+40 and mouseClickX > powerUpX and mouseClickY < powerUpY+40 and mouseClickY > powerUpY:

        # Set boosts
        if powerUpNum == 1:
          playerXBoost = 1.5
        elif powerUpNum == 2:
          bulletYBoost = 1.5
        elif powerUpNum == 3:
          tempInvincible = True
        pygame.event.set_allowed(ENDBOOST)
        pygame.time.set_timer(ENDBOOST,10000)# Reset Boost Timer
        powerUpSpawned = False
        boost = True
      power_up(powerUpSprite,powerUpX,powerUpY)
      
    # Reset Boosts
    if not boost:
      playerXBoost = 1
      bulletYBoost = 1
      tempInvincible = False

    # Boss Bullet Movement
    if bossMode and ("alive" in enemyState):
      bossIndicatorX[0] = enemyX[0]+15
      bossIndicatorX[1] = enemyX[0]+77
      
      # Display an indicator on the boss saying it's about to attack
      if bossAttackPhase == 1:
        for i in range(2):
          screen.blit(bossIndicator,(bossIndicatorX[i],enemyY[0]+20))

      # Actual boss bullet movement
      if bossAttackPhase == 2:
        for i in range(bossBulletCount):
          boss_bullet(bossBulletSprite[i],bossBulletX[i],bossBulletY[i])
          if bossBulletY[i] > 600:
            bossBulletState[i] = "hit"

          # Check for player collision (boss only)
          playerCollision = player_collision(playerX,playerY,bossBulletX[i],bossBulletY[i])
          if playerCollision:
            if not tempInvincible:
              block_events([BOSSATTACK,INCREASEBULLETS,SPAWNPOWERUP,ENDBOOST])
              gameState = "lost"
              running = False
          
          bossBulletY[i] += bossBulletY_change[i]

    # Player Movement and boundaries
    playerX += round(playerX_change*playerXBoost,1)
    player(playerSprite,playerX,playerY)

    if playerX <= 0:
      playerX = 0
    elif playerX >= 768:
      playerX = 768
    
    # Score and mouse updating
    if len(enemyHealth) > 0:
      show_score(score,numEnemies,bossMode,enemyHealth[0],boost,powerUpNum)
    mouseClickX = -1
    mouseClickY = -1

    # Check if any enemies are still alive
    if numEnemies < 1:
      if bossMode:
        block_events([BOSSATTACK,INCREASEBULLETS])
      block_events([SPAWNPOWERUP,ENDBOOST])
      gameState = "won"
      running = False

    pygame.display.update()
    clock.tick(FPS)

  return gameState

## MAIN

def main():
  while True:
    # Display the starting screen
    starting_screen()
  
    # First Battle - UFO Mania
    background = load_image("backgrounds","background1.jpg")
    sprite = pygame.transform.scale(load_image("sprites","enemy1.png"),(64,64))
    choice = "play again"
    while choice == "play again":
      # Argument order: background,sprite,count,enemySpeed,spawnRange1,spawnRange2,bossMode,health,hitbox,battleNumber
      gameState = battle(background,sprite,10,0.75,50,50,False,10,64,1)
      choice = battle_end(gameState)
  
    # Second Battle - Blimp Outbreak
    background = load_image("backgrounds","background2.jpg")
    sprite = pygame.transform.scale(load_image("sprites","enemy2.webp"),(72,49))
    choice = "play again"
    while choice == "play again":
      gameState = battle(background,sprite,20,1.5,50,100,False,5,72,2)
      choice = battle_end(gameState)
    
    # Third Battle - Cosinial Waves
    background = load_image("backgrounds","background3.jpg")
    sprite = pygame.transform.rotate(pygame.transform.scale(load_image("sprites","enemy3.png"),(64,64)),270)
    choice = "play again"
    while choice == "play again":
      gameState = battle(background,sprite,15,1,50,100,False,10,64,3)
      choice = battle_end(gameState)
  
    # Fourth Battle - 8-bit Boss
    background = load_image("backgrounds","background4.jpg")
    sprite = pygame.transform.scale(load_image("sprites","enemy4.png"),(96,96))
    choice = "play again"
    while choice == "play again":
      gameState = battle(background,sprite,1,0.3,50,50,True,100,96,4)
      choice = battle_end(gameState)

    # Once the third battle is won
    game_end()
    

if __name__ == "__main__":
  main()