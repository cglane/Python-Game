import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell

# # Set row 1, cell 5 to one. (Remember rows and
# # column numbers start at zero.)
# grid[1][5] = 1
# Set last player to play
last = 1
# Initalize player score map
playersMap = {'1':[],'-1':[]}
# Sets winning number of connecting dots
winningScore = 9

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Checking for a winner

class checkScore(object):
    # Init creates a list ordered by the x values and
    # another list ordered by the y values
    def __init__(self, playerList, player):
        self.rawList = playerList
        self.xList = sorted(sorted(playerList, key= lambda y: y[0]), key = lambda x: x[0])
        self.yList = sorted(self.xList, key= lambda y: y[1])
        self.player = player

    def straitLine(self,orderedList,axis):
        global winningScore
        totalScore = 0
        for index, value in enumerate(orderedList):
            if((index+1 < len(orderedList)) and (value[axis]== orderedList[index+1][axis])):
                totalScore += 1
                if totalScore >= winningScore:
                    return True
                    pass
            else:
                totalScore = 0
            pass

    def angledLine(self):
        totalXY = 0
        rangeMax = 10
        xyList = [[x,x] for x in range(0,10)]
        yxList = [[x,(9-x)] for x in range(0,10)]
        xyMatch = [x for x in xyList if x in self.rawList]
        yxMatch = [x for x in yxList if x in self.rawList]
        if(len(xyMatch) == len(xyList)):
            return True
        if(len(yxMatch) == len(yxList)):
            return True

    def allScores(self):
        if self.straitLine(self.xList,0) or self.straitLine(self.yList,1) or self.angledLine():
            print (self.player, ' wins')
            pygame.quit()

def addPosition(player,position):
    global last
    if player == '-1':
        if(position in playersMap['-1']):
            last = (last * -1)
            return False
        else:
            playersMap['-1'].append(position)
            newScore = checkScore(playersMap['-1'],'-1')
            newScore.allScores()
            if(position in playersMap['1']):
                playersMap['1'] = filter(lambda a: a != position, playersMap['1'])
    else:
        if(position in playersMap['1']):
            last = (last * -1)
            return False
        else:
            playersMap['1'].append(position)
            newScore = checkScore(playersMap['1'],'1')
            newScore.allScores()
            if(position in playersMap['-1']):
                playersMap['-1'] = filter(lambda a: a != position, playersMap['-1'])
    pass

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            grid[row][column] =  last = (-1 * last)
            if last == 1:
                addPosition('1',[column,row])
            if last == -1:
                addPosition('-1',[column,row])

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            if grid[row][column] == -1:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
