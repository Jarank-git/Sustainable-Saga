
import pygame
import math
from random import randint, randrange
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# Constants
TEXT_BOX_HEIGHT = 100
TEXT_MARGIN = 20
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
GROUND_LEVEL = SCREEN_HEIGHT - 150  # The ground level for the platformer mode
BULLET_SPEED = 5  # Slow bullet speed
BULLET_COOLDOWN = 500  # Time in milliseconds

# Font Setup
font = pygame.font.Font(None, 24)

# Load player frames for each direction
playerFramesRight = [pygame.image.load(f'DR{i}.png') for i in range(1, 10)]
playerFramesLeft = [pygame.image.load(f'DL{i}.png') for i in range(1, 10)]
playerFramesUp = [pygame.image.load(f'DU{i}.png') for i in range(1, 10)]
playerFramesDown = [pygame.image.load(f'DD{i}.png') for i in range(1, 10)]

# Load villain frames
villainFramesRight = [pygame.image.load(f"VR{i}.png") for i in range(1, 10)]
villainFramesLeft = [pygame.image.load(f"VL{i}.png") for i in range(1, 10)]

villainFrameDeath = pygame.image.load("VF6.png")
playerFrameDeath = pygame.image.load("MainDead.png")

# Load backgrounds
background0 = pygame.image.load("introbg.jpg")
background1 = pygame.image.load("lonesome-village-review-1.jpg")
backgroundForest = pygame.image.load("forest-iyGrLtMQ3-transformed (1).jpeg")
background2 = pygame.image.load("Untitled design.png")
background3 = pygame.image.load("quizBG.jpg")
npcImage = pygame.image.load("VillageNPC.png")
checkmark = pygame.image.load("checkmark.png")
xmark = pygame.image.load("xmark.png")
loseScreen = pygame.image.load("loseScreen.jpg")
winScreen = pygame.image.load("winScreen.jpg")
wastemongerSign = pygame.image.load("Wastemonger.png")

# Load bullet image
bulletImage = pygame.image.load("bullet.png")

# Load sounds
pygame.mixer.init()
aiSong = pygame.mixer.music.load('retro-game-arcade-236133.mp3')
pygame.mixer.music.play(-1)
Shoot = pygame.mixer.Sound('SciFiShoot.mp3')
cheer = pygame.mixer.Sound('Cheer.wav')
gameOver = pygame.mixer.Sound('gameOver.wav')
gameStart = pygame.mixer.Sound('gameStart.wav')
damageSound = pygame.mixer.Sound('damage-40114.mp3')
manScream = pygame.mixer.Sound('male_hurt7-48124.mp3')

# NPC Dialogue
npc2pos = (225, 190)
npc2Dialogue = [
    """Hi, I'm Peter Porky, and I'm here to teach you about sustainability.""",
    """Sustainability is a big issue, and it's crucial that we all do our part.""",
    """First, you need to understand what sustainability is.
    So, let's talk about the environment and what we can do to protect it.""",
    """These facts are crucial for understanding the problems and solutions, 
    so it's important to pay attention!""",
    """Sustainability means meeting our needs without harming the environment.""",
    """One key concept in being sustainable is renewable energy, like solar and 
    wind power, which don't pollute the Earth.""",
    """The world's forests are being cut down at alarming rates due to deforestation, 
    which causes harm to biodiversity and the climate.""",
    """Recycling and reducing waste are important actions to 
    conserve the resources we have.""",
    """Sustainable agriculture focuses on growing food in ways that are good 
    for the environment and support healthy environments for many species.""",
    """Electric vehicles are becoming more popular as a way to 
    reduce greenhouse gas emissions.""",
    """Green building practices, like using 
    energy-efficient materials, are helping to reduce our carbon footprint.""",
    """Eco-friendly technologies are being developed to clean the air, water, and oceans.""",
    """Everyone can make a difference! Small actions like reducing plastic use and 
    conserving water help create a more sustainable world.""",
    """You, like many others, can play a role in protecting the planet by learning 
    and spreading awareness.""",
    """Use these facts wisely when you're helping to fight environmental harm. 
    Good luck on your journey!""",
]

npc1pos = (400, 290)
npc1Dialogue = [
    """Green Guardian, your finally here! Fleetwood has been in crisis!""",
    """You HAVE to help us Green Guardian, if you dont, Fleetwood may cease to 
    exist.""",
    """Go down the path infront of me and talk to Rosy Red. She's the one being 
    affected by Waste Mongers actions for years!""",

    """Good Luck on your fight!""",
]

npcDialogue = [
    """Green Guardian? Is that you? I've been waiting for you, Waste Monger has
    been destroying my beloved town of Fleetwood, just take a look at how my land 
    has decayed due to Waste Mongers actions.""",

    """Our town has been tourtured ever since Waste Monger arrived, please stop 
    him Green Guardian.""", 

    """The people of Fleetwood need you now more than ever""",

    """Green Guardian... we believe in you!""",
 
]

# Quiz Questions
questions = [
    "1. What does sustainability mean?",
    "2. What is one key source of renewable energy?",
    "3. What is one of the biggest environmental issues caused by human activity?",
    "4. How can we help reduce our environmental impact when it comes to waste?",
    "5. What is the focus of sustainable agriculture?",
    "6. How can electric vehicles help the environment?",
    "7. What is an example of a green building practice?",
    "8. What technology is being developed to help clean the planet?",
    "9. What small action can everyone take to help the environment?",
    "10. Why is it important for people to learn about sustainability?"
]

# Answer options
options = [
    ["Using resources without causing harm", "Building new roads", "Using fossil fuels", "Overconsumption of water"],
    ["Solar power", "Coal", "Natural gas", "Nuclear power"],
    ["Deforestation", "Overfishing", "Pollution", "All of the above"],
    ["Recycling", "Throwing away more trash", "Burning plastic", "Using more single-use items"],
    ["Growing more food", "Using pesticides", "Supporting eco-friendly farming", "Cutting down forests"],
    ["By emitting more greenhouse gases", "By reducing emissions", "By using more plastic", "By burning coal"],
    ["Building with energy-efficient materials", "Increasing energy consumption", "Using non-renewable resources", "Building with toxic materials"],
    ["AI robots", "Eco-friendly technologies", "Plastic waste", "Pollution"],
    ["Conserving water", "Buying more plastic products", "Eating more meat", "Cutting down trees"],
    ["Because we must protect the environment", "To make more money", "To destroy forests", "Because it's not important"]
]

# Correct answers (sustainability-focused)
correctOptions = [
    "Using resources without causing harm",
    "Solar power",
    "All of the above",
    "Recycling",
    "Supporting eco-friendly farming",
    "By reducing emissions",
    "Building with energy-efficient materials",
    "Eco-friendly technologies",
    "Conserving water",
    "Because we must protect the environment"
]


# Get players direction for animation
def get_player_frames(direction):
    if direction == "right":
        return playerFramesRight
    elif direction == "left":
        return playerFramesLeft
    elif direction == "up":
        return playerFramesUp
    elif direction == "down":
        return playerFramesDown


# Function to render the text box
def renderTextBox(dialogue):
    pygame.draw.rect(screen,(0, 0, 0),(0, SCREEN_HEIGHT - TEXT_BOX_HEIGHT, SCREEN_WIDTH, TEXT_BOX_HEIGHT),)
    yStartText = SCREEN_HEIGHT - TEXT_BOX_HEIGHT + TEXT_MARGIN
    for line in dialogue.split("\n"):
        text = font.render(line.strip(), True, (255, 255, 255))
        screen.blit(text, (TEXT_MARGIN, yStartText))
        yStartText += text.get_height() + 5


# Function to render the Next button
def renderNextButton():
    pygame.draw.rect(
        screen,
        (200, 200, 200),
        (
            SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN,
            SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        ),
    )
    text = font.render("Next", True, (255, 255, 255))
    screen.blit(
        text,
        (
            SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN + 10,
            SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN + 10,
        ),
    )


# Check if the player clicks in the boundary of the next button
def isNextButtonClicked(mousePos):
    x, y = mousePos  # takes the x and y position of mouse position
    return (SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN <= x <=
            SCREEN_WIDTH - BUTTON_MARGIN
            and SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN <= y <=
            SCREEN_HEIGHT - BUTTON_MARGIN)

def isStartButtonClicked(mousePos):
    mousex, mousey = mousePos  # takes the x and y position of mouse position
    return (mousex > 200 and mousex < SCREEN_WIDTH - 200 and mousey > 275 and mousey < SCREEN_HEIGHT - 275)

# Check if the player is near the NPC
def isPlayerNearNpc(playerPos, npcPos, proximityRange=70):
    distance = ((playerPos[0] - npcPos[0])**2 +
                (playerPos[1] - npcPos[1])**2)**0.5  # Pythagorean theorem
    return distance <= proximityRange

def isPlayerNearOtherNpc(playerPos, npc1pos, proximityRange=70):
    distance = ((playerPos[0] - npc1pos[0] + 20)**2 +
                (playerPos[1] - npc1pos[1] + 20)**2)**0.5  # Pythagorean theorem
    if gameMode == "topdown":
        return distance <= proximityRange

def isPlayerNearNpc2(playerPos, npc2pos, proximityRange=70):
    distance = ((playerPos[0] - npc2pos[0] + 20)**2 +
                (playerPos[1] - npc2pos[1] + 20)**2)**0.5  # Pythagorean theorem
    if gameMode == "topdown":
        return distance <= proximityRange
    

def whichOptionClicked(mousePos):
    mousex, mousey = mousePos  # takes the x and y position of mouse position
    if (mousex > 20 and mousex < 350 and mousey > 200 and mousey < 350):
        return 0
    if (mousex > 450 and mousex < 780 and mousey > 200 and mousey < 350):
        return 1
    if (mousex > 20 and mousex < 350 and mousey > 400 and mousey < 550):
        return 2
    if (mousex > 450 and mousex < 780 and mousey > 400 and mousey < 550):
        return 3

def displayQuestionAndOptions(question):
    text = font.render(questions[question], True, (255, 255, 255))
    screen.blit(text,(20, 120))

# Initialize game variables

currentDialogueIndex = 0
currentDialogueOtherIndex = 0
currentDialogue2Index = 0
displayingDialogue = False
displayingOtherDialogue = False
displaying2Dialogue = False
running = True
clock = pygame.time.Clock()
currentBackground = background0
betweenarea = False
gameMode = "intro"

playerFrameCounter = 0
playerDirection = "down"
playerMoving = False
playerIsJump = False
playerJumpCount = 10
playerx = -300
playery = -100
npcPos = (-100, -100)
npc1pos = (400, 290)
villainPos = [-100, -100]
villainFrameCounter = 0
villainDirection = "right"
lastShotTime = 0
villainHealth = 200
playerHealth = 100
redHealthBox = 0
playerRedHealthBox = 0
villainDeathPos = (-100, -100)
villainDying = False
buttonClickedYet = False
playerClickedOnScreen = False
testQuestionNumber = randint(0, 9)

countGameOver = 1

# List to hold bullets and bullet distance travelled each frame
bulletPositions = []
bulletDistances = []

while running:
    clock.tick(30)
    currentTime = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            playerClickedOnScreen = True
            if gameMode == "intro" and isStartButtonClicked(
                pygame.mouse.get_pos()):
                gameStart.play()
                currentBackground = background1
                gameMode = "topdown"
                npcPos = (-500, -500)
                npc1pos = (400, 290)
                playerx = 50
                playery = 200
            elif gameMode == "Won":
                optionClicked = whichOptionClicked(pygame.mouse.get_pos())
                print(optionClicked)
                buttonClickedYet = True
            elif displayingDialogue and isNextButtonClicked(
                    pygame.mouse.get_pos()):
                currentDialogueIndex += 1
                if currentDialogueIndex >= len(npcDialogue):
                    currentDialogueIndex = 0
                    displayingDialogue = False

            elif displayingOtherDialogue and isNextButtonClicked(
                    pygame.mouse.get_pos()):
                currentDialogueOtherIndex += 1
                if currentDialogueOtherIndex >= len(npc1Dialogue):
                    currentDialogueOtherIndex = 0
                    displayingOtherDialogue = False

            elif displaying2Dialogue and isNextButtonClicked(
                    pygame.mouse.get_pos()):
                currentDialogue2Index += 1
                if currentDialogue2Index >= len(npc2Dialogue):
                    currentDialogue2Index = 0
                    displaying2Dialogue = False
        else:
            playerClickedOnScreen = False

    keys = pygame.key.get_pressed()
    playerMoving = False
    dx, dy = 0, 0
    screen.blit(currentBackground, (0, 0))
    if gameMode == "topdown":
        screen.blit(wastemongerSign, (650, 200))

    # Topdown game mode
    if gameMode == "topdown":
        if keys[pygame.K_LEFT]:
            playerDirection = "left"
            dx = -4
            if keys[pygame.K_SPACE]:
                dx = -8
            playerMoving = True
        if keys[pygame.K_RIGHT]:
            playerDirection = "right"
            dx = 4
            if keys[pygame.K_SPACE]:
                dx = 8
            playerMoving = True
        if keys[pygame.K_UP]:
            if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
                playerDirection = "up"
            dy = -4
            playerMoving = True
        if keys[pygame.K_DOWN]:
            if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
                playerDirection = "down"
            dy = 4
            playerMoving = True

        if playerMoving:
            playerx += dx
            playery += dy
            playerFrameCounter += 1
            if playerFrameCounter >= len(playerFramesRight):
                playerFrameCounter = 0
        else:
            playerFrameCounter = 0

        # between area
        if playery >= 150 and playery <= 300:
            betweenarea = True
        else:
            betweenarea = False

        if playerx <= 0 and betweenarea:
            playerx = 0

        if playerx <= 0 and not betweenarea:
            playerx = 0

        if playerx >= SCREEN_WIDTH - 30 and not betweenarea:
            playerx = SCREEN_WIDTH - 30

        if playery <= 15:
            playery = 15
        '''
        inFountainHeight = False
        inFountainWidth = False
        if playery >= 150 and playery<= 270:
            inFountainHeight = True
            
        if playerx >= 377 and playerx <=585:
            inFountainWidth = True

        if inFountainHeight and inFountainWidth:
            playerx = 0
            playery = 0
        '''
        # If player walks through right area
        if playerx >= 800 - 130 and betweenarea:
            gameMode = "platformer"
            npcPos = (-500, -500)
            villainPos = [500, 400]
            playerx = 10
            playery = 400
            currentBackground = background2
            
        # player goes to bottom area
        if playery >= 480 and playerx >= 430 and playerx <=620 :
            playerx = 500
            playery = 50
            npcPos = (450, 350)
            currentBackground = backgroundForest
            gameMode = "Forest"

    if gameMode == "Forest":
        if keys[pygame.K_LEFT]:
            playerDirection = "left"
            dx = -4
            if keys[pygame.K_SPACE]:
                dx = -8
            playerMoving = True
        if keys[pygame.K_RIGHT]:
            playerDirection = "right"
            dx = 4
            if keys[pygame.K_SPACE]:
                dx = 8
            playerMoving = True
        if keys[pygame.K_UP]:
            if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
                playerDirection = "up"
            dy = -4
            playerMoving = True
        if keys[pygame.K_DOWN]:
            if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
                playerDirection = "down"
            dy = 4
            playerMoving = True

        if playerMoving:
            playerx += dx
            playery += dy
            playerFrameCounter += 1
            if playerFrameCounter >= len(playerFramesRight):
                playerFrameCounter = 0
        else:
            playerFrameCounter = 0


        if playerx <= 0:
            playerx = 0


        if playerx >= SCREEN_WIDTH - 30:
            playerx = SCREEN_WIDTH - 30

        if playery <= 15:
            playery = 15

        if playery >= SCREEN_HEIGHT - 130:
            playery = SCREEN_HEIGHT - 130

        #player walks back to village from bottom
        if playery <= 30:
            gameMode = "topdown"
            playerx = 490
            playery = 479
            currentBackground = background1
            npcPos = (-500, -500)



    if gameMode == "platformer":
        if playerHealth > 0:
            if keys[pygame.K_LEFT]:
                playerDirection = "left"
                dx = -4
                playerMoving = True
            if keys[pygame.K_RIGHT]:
                playerDirection = "right"
                dx = 4
                playerMoving = True

            if keys[pygame.K_SPACE] and currentTime - lastShotTime > BULLET_COOLDOWN:
                Shoot.play()
                lastShotTime = currentTime
                # Calculate direction to the villain
                bulletx = playerx + 32
                bullety = playery + 22
                bulletDestinationY = villainPos[1] + 22
                if villainDirection == "right":
                    bulletDestinationX = villainPos[0] + 64
                elif villainDirection == "left":
                    bulletDestinationX = villainPos[0] - 64
                else:
                    bulletDestinationX = villainPos[0]
                angle = math.atan2(bulletDestinationY - bullety,
                                   bulletDestinationX - bulletx)
                # Calculate how far the bullet will travel each frame
                bulletdx = math.cos(angle) * BULLET_SPEED
                bulletdy = math.sin(angle) * BULLET_SPEED
                bulletPositions.append([bulletx, bullety])
                bulletDistances.append([bulletdx, bulletdy])

            if not playerIsJump:
                if keys[pygame.K_UP]:
                    playerIsJump = True
            # Jumping mechanics
            if playerIsJump:
                playerMoving = True
                if playerJumpCount >= -10:
                    neg = 1
                    if playerJumpCount < 0:
                        neg = -1
                    playery -= (playerJumpCount**2) * 0.5 * neg
                    playerJumpCount -= 1
                else:
                    playerIsJump = False
                    playerJumpCount = 10

            # Player can't walk off screen
            if playerx > SCREEN_WIDTH:
                playerx = 0          
            if playerx < 0:
                playerx = SCREEN_WIDTH

            # Update player frames and position
            if playerMoving:
                playerx += dx
                playery += dy
                playerFrameCounter += 1
                if playerFrameCounter >= len(playerFramesRight):
                    playerFrameCounter = 0

        # Villain dying sequence
        if villainHealth <= 0:
            if villainDying == False:
                villainDyingTimeStart = currentTime
                villainDying = True
            elapsed_time = currentTime - villainDyingTimeStart
            if elapsed_time < 2000:
                villainDeathPos = (villainPos[0], villainPos[1])
            else:
                gameMode = "Won"
                villainDeathPos = (-100, -100)
        # Villain movement mechanics    
        else:
            if villainPos[0] < playerx and playerHealth > 0:
                villainPos[0] += 2
                villainFrameCounter += 1
                villainDirection = "right"

            elif villainPos[0] > playerx and playerHealth > 0:
                villainPos[0] -= 2
                villainFrameCounter += 1
                villainDirection = "left"

            if villainFrameCounter >= len(villainFramesRight):
                villainFrameCounter = 0

        # Update bullet positions each frame and check if player is hit
        for i in range(len(bulletPositions) - 1, -1, -1):
            bulletPositions[i][0] += bulletDistances[i][0]
            bulletPositions[i][1] += bulletDistances[i][1]

            if (bulletPositions[i][0] <= villainPos[0] + 32 and bulletPositions[i][0] >= villainPos[0] - 32):
                villainHealth -= 10
                redHealthBox += 2.5
                damageSound.play()
                bulletPositions.pop(i)
                bulletDistances.pop(i)

            elif (bulletPositions[i][0] < 0 or bulletPositions[i][0] > SCREEN_WIDTH
                    or bulletPositions[i][1] < 0 or bulletPositions[i][1] > 432):
                bulletPositions.pop(i)
                bulletDistances.pop(i)


        # Player hitbox
        if (playerx <= villainPos[0] + 22 and playerx >= villainPos[0] - 22) and playery >= 336 and villainHealth > 0:
            playerHealth -= 100
            playerRedHealthBox += 100
            manScream.play()

        # Player dies
        if playerHealth <= 0:
            screen.blit(playerFrameDeath, (playerx, playery))
            if villainPos[0] < 810:
                villainPos[0] += 2
                villainFrameCounter += 1
                villainDirection = "right"
            if villainPos[0] >= SCREEN_WIDTH:
                gameMode = "Lost"

    # Lost game end screen        
    if gameMode == "Lost":
        currentBackground = loseScreen
        if countGameOver == 1:
            gameOver.play()
            countGameOver += 1
        screen.blit(currentBackground, (0, 0))

    # Quiz    
    if gameMode == "Won":
        playerFrameCounter = 0
        playerDirection = "down"
        playerMoving = False
        playerIsJump = False
        playerJumpCount = 10
        playerx = -300
        playery = -100
        npcPos = (-100, -100)
        villainPos = [-100, -100]
        villainFrameCounter = 0
        villainDirection = "right"
        villainDeathPos = (-100, -100)
        villainDying = False
        bulletPositions = []
        currentBackground = background3

        # Display the question
        questionText = font.render(questions[testQuestionNumber], True, (255, 255, 255))
        screen.blit(questionText,(40, 70))

        # Display the options
        option1Text = font.render(options[testQuestionNumber][0], True, (255, 255, 255))
        screen.blit(option1Text,(40, 275))
        option2Text = font.render(options[testQuestionNumber][1], True, (255, 255, 255))
        screen.blit(option2Text,(470, 275))
        option3Text = font.render(options[testQuestionNumber][2], True, (255, 255, 255))
        screen.blit(option3Text,(40, 475))
        option4Text = font.render(options[testQuestionNumber][3], True, (255, 255, 255))
        screen.blit(option4Text,(470, 475))

        # Check if selected option is correct
        if buttonClickedYet:
            selectedAnswer = options[testQuestionNumber][optionClicked]  #error but it works dont change it lol
            if selectedAnswer == correctOptions[testQuestionNumber]:
                screen.blit(checkmark, (300, 200))
                screen.blit(winScreen, (0, 0))
                if countGameOver == 1:
                    cheer.play()
                    countGameOver += 1
            else:
                screen.blit(xmark, (200, 100))
                gameMode = "Lost"


    # ??? forgot what this does lol    
    if gameMode == "Ending":
        currentBackground = background4
        screen.blit(currentBackground, (0, 0))

    # Clear the screen and draw the background
    # Draw the player
    playerFrames = get_player_frames(playerDirection)
    playerFrame = playerFrames[playerFrameCounter]
    if (gameMode == "topdown" or gameMode == "platformer" or gameMode == "Forest") and playerHealth > 0:
        screen.blit(playerFrame, (playerx, playery))
    screen.blit(npcImage, npcPos)
    screen.blit(villainFrameDeath, (villainDeathPos))
    if gameMode == "platformer":
        pygame.draw.rect(screen, (255, 0, 0), (playerx, playery-22, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (playerx, playery-22, 50 - playerRedHealthBox, 10))

    # Draw the villain
    if villainHealth > 0:
        if villainDirection == "right":
            villainFrames = villainFramesRight
        else:
            villainFrames = villainFramesLeft
        villainFrame = villainFrames[villainFrameCounter // 3]
        screen.blit(villainFrame, (villainPos[0], villainPos[1]))

        pygame.draw.rect(screen, (255, 0, 0), (villainPos[0], villainPos[1]-22, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (villainPos[0], villainPos[1]-22, 50 - redHealthBox, 10))

    # Draw each bullets
    for bullet in bulletPositions:
        screen.blit(bulletImage, (bullet[0], bullet[1]))


    # Update display
    if isPlayerNearNpc((playerx, playery), npcPos) and not displayingDialogue:
        displayingDialogue = True
        currentDialogueIndex = 0

    if not isPlayerNearNpc((playerx, playery), npcPos) and displayingDialogue:
        displayingDialogue = False
    # If displaing dialogue, render the next button
    if displayingDialogue:
        renderTextBox(npcDialogue[currentDialogueIndex])
        renderNextButton()

    if isPlayerNearOtherNpc((playerx, playery), npc1pos) and not displayingOtherDialogue:
        displayingOtherDialogue = True
        currentDialogueOtherIndex = 0

    if not isPlayerNearOtherNpc((playerx, playery), npc1pos) and displayingOtherDialogue:

        displayingOtherDialogue = False
    # If displaing dialogue, render the next button
    if displayingOtherDialogue:
        renderTextBox(npc1Dialogue[currentDialogueOtherIndex])
        renderNextButton()

    if isPlayerNearNpc2((playerx, playery), npc2pos) and not displaying2Dialogue:
        displaying2Dialogue = True
        currentDialogue2Index = 0

    if not isPlayerNearNpc2((playerx, playery), npc2pos) and displaying2Dialogue:
        displaying2Dialogue = False

    
    # If displaing dialogue, render the next button
    if displaying2Dialogue:
        renderTextBox(npc2Dialogue[currentDialogue2Index])
        renderNextButton()

    pygame.display.flip()

pygame.quit()
