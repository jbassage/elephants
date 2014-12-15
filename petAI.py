import pygame, sys, random, math, petMaster, petField, pathfinder
from pygame.locals import *


# the pets
class Pet:
    def __init__(self, initSurface, surfacesList, initPos=(50, 50), \
                 name='dumbo', hungerRollover=30, hungerLimits=(5,10)):
        self.rect           = pygame.Rect (initPos[0], initPos[1], 50, 50)
        self.cell           = None
        self.wallCells      = []
        self.surface        = initSurface
        self.surfacesList   = surfacesList
        self.name           = name
        self.target         = [50, 50]
        self.targetCell     = None
        self.waypoints      = []
        self.debug          = [None, None, None, None, None, None]
        self.tummy          = 15
        self.targetType     = 'idle'
        self.targetSpcfc    = None,
        self.hungerCounter  = make_hunger_counter(hungerRollover)
        self.hungerLimits   = hungerLimits
        self.hungry         = True
        self.hurry          = 4
        self.seekTarget     = True
        self.moveSpeed      = 3
        self.move           = [0, 0]
        self.path           = []
        self.idle           = make_idle_counter()



# update hunger, targeting, etc
def upkeep(mSt, who, fieldState):

    if who.name == 'surus':
        who = hurrySurus(who, fieldState)
    elif who.name == 'abul':
        who = hurryAbul(who, fieldState)

    hunger = next(who.hungerCounter)
    if hunger and who.tummy > 0:
        who.tummy -= 1
    if who.tummy <= who.hungerLimits[0]:
        who.hungry = True
    if who.tummy >= who.hungerLimits[1]:
        who.hungry = False
    if who.seekTarget:
        who = getTarget(who, fieldState)
    elif who.targetSpcfc == 'mouse':
        who.target[0] = pygame.mouse.get_pos()[0] - mSt['field'][0]
        who.target[1] = pygame.mouse.get_pos()[1] - mSt['field'][1]
    who = waypoints(mSt, who, fieldState)
    who = move(mSt, who, fieldState)
    who = facing(who, fieldState)

    return who

def make_hunger_counter(rollover):
    hungerCounter = 0
    hungerStep = False
    while True:
        hungerCounter +=1
        if hungerCounter > rollover:
            hungerCounter = 0
        if hungerCounter == rollover:
            hungerStep = True
        else:
            hungerStep = False
        yield hungerStep

###############################################################################
##                             TARGET SELECTION                              ##
###############################################################################

#select a target
def getTarget(who, fieldState):
    if who.name == 'surus':
        getTargetSurus(who, fieldState)
    elif who.name == 'abul':
        getTargetAbul(who, fieldState)
    else:
        getTargetAbul(who, fieldState)
    return who

# Custom target priority list for Surus
def getTargetSurus(who, fieldState):
    if len(fieldState['foods']) > ( who.hungerLimits[1] - who.tummy + 15) \
       and fieldState['foodDispense'] == True:
        targetSwitch(who, fieldState, False)
    elif who.hungry == True and len(fieldState['foods']) > 0:
        targetDryFood(who, fieldState)
    elif who.hungry == True and len(fieldState['foods']) == 0:
        targetSwitch(who, fieldState, True)
    elif who.hungry == False and fieldState['foodDispense'] == True:
        targetSwitch(who, fieldState, False)
    elif who.hungry == False and fieldState['foodDispense'] == False:
        targetHome(who, fieldState)
    else:
        targetHome('guest', fieldState)
    return who

#Custom target priority list for Abul
def getTargetAbul(who, fieldState):
    if who.hungry == True and len(fieldState['foods']) > 0:
        targetFood(who, fieldState)
    elif who.hungry == True and len(fieldState['foods']) == 0:
        targetSwitch(who, fieldState, True)
    elif who.hungry == False:
        targetHome(who, fieldState)
    else:
        targetHome('guest', fieldState)
    return who

##############################################



# set home as target
def targetHome(who, fieldState):
    if who.name in fieldState['homes'].keys():
        who.target[0] = fieldState['homes'][who.name][0].centerx
        who.target[1] = fieldState['homes'][who.name][0].centery
        who.targetType = 'home'
        return who
    else:
        who.target[0] = fieldState['homes']['guest'][0].centerx
        who.target[1] = fieldState['homes']['guest'][0].centery
        who.targetType = 'home'
        return who


#get closest food as new target
def targetFood(who, fieldState):
    closestFood = [1,1] # change this number
    closestDistance = 1000000 # change this number
    foundFood = False
    ignoreFood = False
    who.targetSpcfc = None
    # If there's only 1 food on the field, leave it for who's closest & hungry
    if len(fieldState['foods']) == 1:
        for creature in fieldState['creaturesList']:
            otherDist = math.hypot ( fieldState['foods'][0].centerx - creature.rect.centerx, 
                                     fieldState['foods'][0].centery - creature.rect.centery )
            selfDist = math.hypot ( fieldState['foods'][0].centerx - who.rect.centerx, 
                                    fieldState['foods'][0].centery - who.rect.centery )
            if creature != who and creature.hungry == True \
               and otherDist < selfDist:
                ignoreFood = True
    
    for i in range(len(fieldState['foods'])):
        targeted = False
        distance = math.hypot ( fieldState['foods'][i].centerx - who.rect.centerx,
                                fieldState['foods'][i].centery - who.rect.centery )
        # don't go for a food if someone else already is
        for creature in fieldState['creaturesList']:
            if creature != who and creature.targetSpcfc == fieldState['foods'][i]:
                targeted = True
        # find closest available food
        if distance < closestDistance and targeted == False \
           and ignoreFood == False:
            closestDistance = distance
            closestFood[0] = fieldState['foods'][i].centerx
            closestFood[1] = fieldState['foods'][i].centery
            who.targetSpcfc = fieldState['foods'][i]
            foundFood = True
            
    if foundFood:
        who.target[0] = closestFood[0]
        who.target[1] = closestFood[1]
        who.targetType = 'food'
    elif not foundFood:
        targetSwitch(who, fieldState, True)
    return who

#get closest food as new target, but target food in the pond last
def targetDryFood(who, fieldState):
    closestFood = [1,1] # change this number
    closestDistance = 1000000 # change this number
    foundFood = False
    ignoreFood = False
    who.targetSpcfc = None
    # If there's only 1 food on the field, leave it for who's closest & hungry
    if len(fieldState['foods']) == 1:
        for creature in fieldState['creaturesList']:
            otherDist = math.hypot( fieldState['foods'][0].centerx - creature.rect.centerx, 
                                    fieldState['foods'][0].centery - creature.rect.centery )
            selfDist = math.hypot( fieldState['foods'][0].centerx - who.rect.centerx, 
                                   fieldState['foods'][0].centery - who.rect.centery )
            if creature != who and creature.hungry and otherDist < selfDist:
                ignoreFood = True
    
    for i in range(len(fieldState['foods'])):
        targeted = False
        distance = math.hypot ( fieldState['foods'][i].centerx - who.rect.centerx,
                                fieldState['foods'][i].centery - who.rect.centery )
        # only go for food in the pond if there's no other food
        if fieldState['foods'][i].colliderect(fieldState['pond']):
            targeted = True
        # don't go for a food if someone else already is
        for creature in fieldState['creaturesList']:
            if creature != who \
               and creature.targetSpcfc == fieldState['foods'][i]:
                targeted = True
        # find closest available food
        if distance < closestDistance and targeted == False \
           and ignoreFood == False:
            closestDistance = distance
            closestFood[0] = fieldState['foods'][i].centerx
            closestFood[1] = fieldState['foods'][i].centery
            who.targetSpcfc = fieldState['foods'][i]
            foundFood = True
            
    if foundFood:
        who.target[0] = closestFood[0]
        who.target[1] = closestFood[1]
        who.targetType = 'food'
    elif not foundFood:
        targetFood(who, fieldState)
    return who


# get food switch as target unless it's already set the right way
def targetSwitch(who, fieldState, state):
    if state != fieldState['foodDispense']:
        ignoreSwitch = False
        for creature in fieldState['creaturesList']:
            if creature != who and creature.targetSpcfc == 'foodSwitch':
                ignoreSwitch = True
        if ignoreSwitch == False:
            who.target[0] = fieldState['foodSwitch'].centerx
            who.target[1] = fieldState['foodSwitch'].centery
            who.targetType = 'switch'
            who.targetSpcfc = 'foodSwitch'
            return who
        else:
            target_idle(who)
    elif state == fieldState['foodDispense']:
        target_idle(who)



# makes the pet walk in circles when 'idle'
def target_idle(who):
    direction = next(who.idle)
    if direction == 0:
        who.target[0] = who.rect.centerx - 40
        who.target[1] = who.rect.centery - 0
    elif direction == 1:
        who.target[0] = who.rect.centerx + 0
        who.target[1] = who.rect.centery - 30
    elif direction == 2:
        who.target[0] = who.rect.centerx + 30
        who.target[1] = who.rect.centery + 0
    elif direction == 3:
        who.target[0] = who.rect.centerx - 0
        who.target[1] = who.rect.centery + 30
    who.targetType = 'idle'
    return who
    
# periodically changes the direction seed for idle
def make_idle_counter():
    idleCounter = 0
    idleDir = 1
    while True:
        idleCounter +=1
        if idleCounter > 10:
            idleCounter = 0
        if idleCounter == 10:
            idleDir += 1
        if idleDir > 3:
            idleDir = 0
        yield idleDir

###############################################################################
##                                MOVEMENT                                   ##
###############################################################################

# draws path from pathfinding
def find_path(mSt, who, fieldState):
##    print(who.name + str(who.cell.coords) +':')###
    for cell in who.path:
        cell[0].outlineColor = None
    # adds other creatures' wall cells as walls
    for creature in fieldState['creaturesList']:
        if creature != who:
            for cell in creature.wallCells:
                x_pos = cell.coords[0]
                y_pos = cell.coords[1]
                fieldState['grid'][x_pos][y_pos].pathType.append('wall')
    who.path = []
    path_cells = pathfinder.get_path_from_gridStartGoal(fieldState['grid'],
                                                        who.cell, who.targetCell)
    for cell in path_cells:
        who.path.append([cell, False]) # cell, and whether cell has been entered
    # takes the other creatures's wall cells back off
    for creature in fieldState['creaturesList']:
        if creature != who:
            for cell in creature.wallCells:
                x_pos = cell.coords[0]
                y_pos = cell.coords[1]
                fieldState['grid'][x_pos][y_pos].pathType.remove('wall')
    
    for cell in who.path:
        cell[0].outlineColor = (255, 255, 255)
##        print(str(cell[0].coords), end = ', ')###
##    print('')###


# sets a waypoint if target is inside a collidable
# or if the corner of a collidable is within 2 pixels' distance
def waypoints(mSt, who, fieldState):
    get_path = True

    #check for obstacles between each corner and the target
    topleft = checkLine(who.rect.left, who.rect.top,
                        who.target[0], who.target[1], who, fieldState)
    topright = checkLine(who.rect.right, who.rect.top,
                         who.target[0], who.target[1], who, fieldState)
    bottomleft =checkLine(who.rect.left, who.rect.bottom,
                          who.target[0], who.target[1], who, fieldState)
    bottomright =checkLine(who.rect.right, who.rect.bottom,
                           who.target[0], who.target[1], who, fieldState)    
    who.debug = [topleft, topright, bottomleft, bottomright]
    who.debug.extend([None, None])
    if topleft == None and topright == None \
       and bottomleft == None and bottomright == None:
        who.waypoints = []
        for cell in who.path:
            cell[0].outlineColor = None
        who.waypoints = []
        get_path = False

    bigger_shadow = who.rect.inflate(2, 2)
    for collidable in fieldState['collidables']:
        if collidable != who.rect:
            if bigger_shadow.colliderect(collidable):
                get_path = True
                
    if not who.cell or not who.targetCell:
        get_path = False

    if who.cell == who.targetCell:
        get_path = False

    

    if get_path:
        if who.path:
            if who.path[-1][0] != who.targetCell: # if current path leads to wrong target
##                print('A: ', end='')###
                find_path(mSt, who, fieldState)
            else: # if current path still leads to target
                if who.path[0][0] != who.cell and who.path[0][1]: # if path doesn't start at creature #######
##                    print('deleting path' + str(who.path[0][0].coords) +'; '+who.name+' at '+str(who.cell.coords))
                    del who.path[0]
            for cell in who.path: # if a creature has crossed the previously found path
                for creature in fieldState['creaturesList']:
                    if creature != who and cell[0].rect.colliderect(creature.rect):
##                        print('C: ', end='')###
                        find_path(mSt, who, fieldState)
        if not who.path:
##            print('B: ', end= '')###
            find_path(mSt, who, fieldState)
    elif who.path:
        who.path = []
##        print ('break path ' + who.name + str(who.cell.coords))###
        
    if len(who.path) < 2:
        who.waypoints = []
    else:
        point_x = int(who.path[1][0].coords[0]*fieldState['gridDims'][0]+fieldState['gridDims'][0]/2)
        point_y = int(who.path[1][0].coords[1]*fieldState['gridDims'][0]+fieldState['gridDims'][0]/2)
        if who.path[1][0].rect.centerx == who.cell.rect.centerx \
           and who.cell.rect.centerx != who.rect.centerx:
            point_y = int(who.rect.centery)
        if who.path[1][0].rect.centery == who.cell.rect.centery \
           and who.cell.rect.centery != who.rect.centery:
            point_x = int(who.rect.centerx)
        who.waypoints = [[point_x, point_y]]

    if who.path and who.cell == who.path[0][0]: # mark current cell as passed
        who.path[0][1] = True
    return who

# checks for things between AI and target
# This is Bresenham's line algorithm (found on wikipedia)
def checkLine(x0, y0, x1, y1, who, fieldState):
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    err = dx-dy

    while x0 != x1 or y0 != y1:
        e2 = 2*err
        if e2 > -dy:
            err = err - dy
            x0 += sx
        if e2 < dx:
            err = err + dx
            y0 += sy
        for collidable in fieldState['collidables']:
            if collidable != who.rect and collidable.collidepoint(x0, y0):
                if collidable.left - x0 < 2 and collidable.left - x0 > -2:
                    side = 'west'
                    endpoints = collidable.topleft, collidable.bottomleft
                elif collidable.right - x0 < 2 and collidable.right - x0 > -2:
                    side = 'east'
                    endpoints = collidable.topright, collidable.bottomright
                elif collidable.top - y0 < 2 and collidable.top - y0 > -2:
                    side = 'north'
                    endpoints = collidable.topleft, collidable.topright
                elif collidable.bottom -y0 < 2 and collidable.bottom - y0 > -2:
                    side = 'south'
                    endpoints = collidable.bottomleft, collidable.bottomright
                else:
                    side = 'unknown'
                    endpoints = None
                    
                return [x0, y0], side, endpoints
    return None


# determines where the creature wants to move
def move(mSt, who, fieldState):
    if not who.waypoints:
        dest = [who.target[0], who.target[1]]
    else:
        dest = [who.waypoints[0][0], who.waypoints[0][1]]
    destDist = math.hypot ( dest[0]- who.rect.centerx,
                              dest[1]- who.rect.centery)
    who.moveSpeed = who.hurry * 3
    
    a = dest[0] - who.rect.centerx
    b = dest[1] - who.rect.centery
    ab = a**2 + b**2
    if who.moveSpeed != 0:
        p = ab**.5 // who.moveSpeed +1
        who.move = [int(a/p), int(b/p)]
    else:
        who.move = [0,0]

    # collision handling
    obstacle, obstDist = obstacleCheck(mSt, who, fieldState)
    if obstacle == 'none':
        who.rect.move_ip(who.move[0], who.move[1])
    elif obstacle != 'none':
        if obstacle == 'east' or obstacle == 'west':
            who.move[0] = obstDist
        if obstacle == 'north' or obstacle == 'south':
            who.move[1] = obstDist
        if obstacle == 'corner':
            who.move[random.randint(0,1)] = 0
        if obstacleCheck(mSt, who, fieldState)[0] == 'none':
            who.rect.move_ip(who.move[0], who.move[1])


    return who


# Collision detection
def obstacleCheck(mSt, who, fieldState):
    obstacle = 'none'
    obstDist = 0
    oldX = 0
    oldY = 0
    goal = who.rect.move(who.move[0], who.move[1])
    for collidable in fieldState['collidables']:
        if collidable != who.rect and goal.colliderect(collidable):
            if collidable.left >= who.rect.right:
                obstacle = 'east'
                obstDist = collidable.left - who.rect.right
            elif collidable.right <= who.rect.left:
                obstacle = 'west'
                obstDist = collidable.right - who.rect.left
            elif collidable.top >= who.rect.bottom:
                obstacle = 'south'
                obstDist = collidable.top - who.rect.bottom
            elif collidable.bottom <= who.rect.top:
                obstacle = 'north'
                obstDist = collidable.bottom - who.rect.top
            else:
                obstacle = 'corner'
    if goal.left < 0:
        obstacle = 'west'
        obstDist = 0 - who.rect.left
    elif goal.right > mSt['field'][4]:
        obstacle = 'east'
        obstDist = mSt['field'][4] - who.rect.right
    elif goal.top < 0:
        obstacle = 'north'
        obstDist = 0 - who.rect.top
    elif goal.bottom > mSt['field'][5]:
        obstacle = 'south'
        obstDist = mSt['field'][5] - who.rect.bottom
        
    return obstacle, obstDist

# sets hurry for Surus
def hurrySurus(who, fieldState):
    TargetDist = math.hypot( who.target[0] - who.rect.centerx,
                             who.target[1] - who.rect.centery )
    if who.targetType == 'idle':
        who.hurry = 1
    elif who.targetType == 'home' and fieldState['foodDispense']:
        who.hurry = 1
    elif who.targetType == 'home' and not fieldState['foodDispense']:
        who.hurry = 4
    elif who.targetType == 'switch' and fieldState['foodDispense']:
        who.hurry = 8
    elif who.targetType == 'switch' and not fieldState['foodDispense']:
        who.hurry = 4
    elif len(fieldState['foods']) > 10 and who.tummy <= 20 \
         and fieldState['foodDispense'] == True:
        who.hurry = 8
    elif len(fieldState['foods']) > 10 and who.tummy <= 20 \
         and fieldState['foodDispense'] == False:
        who.hurry = 4
    elif len(fieldState['foods']) > 10 and who.tummy > 20:
        who.hurry = 4
    elif len(fieldState['foods']) <= 10 and who.tummy <= 20:
        who.hurry = 4
    elif len(fieldState['foods']) <= 10 and who.tummy > 20:
        who.hurry = 2
    if TargetDist >= who.rect.width * 10:
        who.hurry += 5
    return who

# sets hurry for Abul and others
def hurryAbul(who, fieldState):
    TargetDist = math.hypot( who.target[0] - who.rect.centerx,
                             who.target[1] - who.rect.centery )
    if who.targetType == 'idle':
        who.hurry = 2
    else:
        who.hurry = 4
    if TargetDist >= who.rect.width * 8:
        who.hurry += 3
    return who

# set appropriate surface based on direction
def facing(who, fieldState):
    if who.move[1] * -1 > abs(who.move[0]):
        who.surface = who.surfacesList[0]
    elif who.move[0] > abs(who.move[1]):
        who.surface = who.surfacesList[1]
    elif who.move[1] > abs(who.move[0]):
        who.surface = who.surfacesList[2]
    elif who.move[0] * -1 > abs(who.move[1]):
        who.surface = who.surfacesList[3]
    return who
