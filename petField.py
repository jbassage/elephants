import pygame, sys, random, math, petMaster, petAI, petPanel, pathfinder
from pygame.locals import *

FPSCLOCK = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FOODCOLOR = (76, 153, 0)
DARKFOOD = (51, 102, 0)
WHITE = (255, 255, 255)
surusColor = [0, 125, 255]
abulColor = [255, 128, 0]
FIELDCOLOR = (255, 255, 153)
SURUSHOMECOLOR = (0, 0, 102)
ABULHOMECOLOR = (102, 51, 0)
GUESTHOMECOLOR = (153, 153, 0)
SWITCHON = (192, 192, 192)
SWITCHOFF = (32, 32, 32)
ROCK = (128, 128, 128)
WATER = (51, 153, 255)
RED = (204, 0, 0)
LIGHTRED = (255, 0, 0)
PANELCOLOR = (255, 255, 204)

FOODSIZE = 20

def launch(mSt, creaturesList):

    runField(mSt, creaturesList)

def runField(mSt, creaturesList):
    global FPSCLOCK

    windowSurface = pygame.display.get_surface()

    #creates the surface that the field is drawn on
    fieldSurface = pygame.Surface((mSt['field'][4], mSt['field'][5]))
    fieldRect = pygame.Rect(mSt['field'][0], mSt['field'][1],
                            mSt['field'][4], mSt['field'][5])

    # not really necessary to give object to each pet since fieldState['creaturesList']
    # serves this purpose, but the two main ones are named for certain debugging stuff
    surus = creaturesList[0]
    abul = creaturesList[1]

    # fullscreen not currently implemented
    fullscreen = False

    
    # set up debug text
    debug = True
    currentFPS = 0
    BASICFONT = pygame.font.SysFont(None, 25)

    textFPS = BASICFONT.render('FPS: ' + str(int(currentFPS)), True, BLACK)
    textFPSRect = textFPS.get_rect()
    textFPSRect.topleft = [5, 5]

    textSurusTarget = BASICFONT.render('tTarget: ' + 'longword', True, WHITE)
    textSurusTargetRect = textSurusTarget.get_rect()
    textSurusTargetRect.topright = [mSt['field'][4] - 5, textFPSRect.bottom + 5]

    textSurusTummy = BASICFONT.render('tTummy: ' + str(surus.tummy), True, WHITE)
    textSurusTummyRect = textSurusTummy.get_rect()
    textSurusTummyRect.topleft = [textSurusTargetRect.left, textSurusTargetRect.bottom+5]

    textSurusHurry = BASICFONT.render('tHurry: ' + str(surus.hurry), True, WHITE)
    textSurusHurryRect = textSurusHurry.get_rect()
    textSurusHurryRect.topleft = [textSurusTargetRect.left, textSurusTummyRect.bottom +5]

    textAbulTarget = BASICFONT.render('fTarget: ' + 'longword', True, WHITE)
    textAbulTargetRect = textAbulTarget.get_rect()
    textAbulTargetRect.topright = [mSt['field'][4] - 5, textSurusHurryRect.bottom +5]

    textAbulTummy = BASICFONT.render('fTummy: ' + str(abul.tummy), True, WHITE)
    textAbulTummyRect = textAbulTummy.get_rect()
    textAbulTummyRect.topleft = [textAbulTargetRect.left, textAbulTargetRect.bottom + 5]

    textAbulHurry = BASICFONT.render('fHurry: ' + str(abul.hurry), True, WHITE)
    textAbulHurryRect = textAbulHurry.get_rect()
    textAbulHurryRect.topleft = [textAbulTargetRect.left, textAbulTummyRect.bottom +5]

    textFPSRect.topleft = [textAbulTargetRect.left, 5]

    #extra debug text
    textDebug1 = BASICFONT.render('', True, BLACK)
    textDebug1Rect = textDebug1.get_rect()
    textDebug1Rect.topleft = [200, 5]
    
    textDebug2 = BASICFONT.render('', True, BLACK)
    textDebug2Rect = textDebug2.get_rect()
    textDebug2Rect.topleft = [200, textDebug1Rect.bottom + 5]


    # set up a grid to overlay the field, used by the AI for A* pathfinding
    CELLSIZE = 50
    GRIDWIDTH = mSt['field'][4] // CELLSIZE
    GRIDHEIGHT = mSt['field'][5] // CELLSIZE
    
    grid = []
    for x in range(GRIDWIDTH):
        grid.append([])
        for y in range(GRIDHEIGHT):
            grid[x].append(pathfinder.GridCell(CELLSIZE, x, y))

    
    # set up the field
    homes = {'surus'    :[pygame.Rect( 0, 0, 150, 150 ), SURUSHOMECOLOR],
            'abul'      :[pygame.Rect( 0, mSt['field'][5] - 150, 150, 150 ), ABULHOMECOLOR],
            'guest'     :[pygame.Rect( mSt['field'][4] - 100, mSt['field'][5]/2 - 100, 100, 200), GUESTHOMECOLOR]}
    
    # fieldState library passed to other modules / functions contains information on what's going on
    fieldState = {'grid'            : grid,
                  'gridDims'        : [CELLSIZE, GRIDWIDTH, GRIDHEIGHT],
                  'dirtyRects'      : [],
                  'foods'           : [],
                  'foodDispense'    : True,
                  'foodSwitch'      : pygame.Rect( mSt['field'][4]-30, mSt['field'][5]-30, 30,30),
                  'addFood'         : [False, 0, False],
                  'homes'           : homes,
                  'pond'            : pygame.Rect ( mSt['field'][4] - 300, 0, 300, 130),
                  'creaturesList'   : creaturesList,
                  'collidables'     : []}


    boulder1 = pygame.Rect( 600, 300, 150, 100)
    fieldState['collidables'].append(boulder1)
    boulder2 = pygame.Rect( 700, 150, 50, 250)
    fieldState['collidables'].append(boulder2)

    for x in range(GRIDWIDTH):
        for y in range(GRIDHEIGHT):
            for wall in fieldState['collidables']:
                if grid[x][y].rect.colliderect(wall) and not 'wall' in grid[x][y].pathType:
                    grid[x][y].pathType.append('wall')
                    grid[x][y].outlineColor = ROCK
    
    for creature in fieldState['creaturesList']:
        fieldState['collidables'].append(creature.rect)
    # 'dirty rects' method of surface refresh hasn't been implemented for a few versions,
    # but should be mostly in place
    fieldState['dirtyRects'].append(pygame.Rect(0, 0, mSt['window'][2], mSt['window'][3]))#    


    foodSwitchColor = SWITCHON
    pondShallow = pygame.Rect(fieldState['pond'].left - 50, -130, 100, 260)




    

    # set up the food data structure
    foodCounter = 0
    newfood = 50 # Frequency with which food is added.
    foodBurst = False # controls bursts of high drop rates
    burstCounter = 0

    # set up the panels for the field
    panelButtons = {'addFoodButton'     : None,
                    'dispenseOffButton' : None,
                    'dispenseOnButton'  : None,
                    'mouseRelease'      : None,
                    'radarOffButton'    : None,
                    'radarOnButton'     : None}
    panelState   = {'dirtyRects'        : [],
                    'buttonsLoc'        : panelButtons,
                    'addFood'           : [0, False],
                    'dispenseOffButton' : [0, False],
                    'dispenseOnButton'  : [0, False],
                    'mouseRelease'      : [0, False],
                    'radarOffButton'    : [0, False],
                    'radarOnButton'     : [0, False]}
    q_down = False # to keep track of when to light up certain panels
    f_down = False
    ''' For each of the panel buttons, button[0] indicates color. 0 = standard, 1 = hover, 2 = pressed.
        button[1] indicates whether the button is being pressed.
    '''

    debug1 = ''
    debug2 = ''

    
    # run the game loop
    while True:
        panelState = petPanel.launchPanels(mSt, fieldState, panelState)
        for i in panelState['dirtyRects']:
            fieldState['dirtyRects'].append(i.move(mSt['bigPanel'][0], mSt['bigPanel'][1]))#
        
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                petMaster.terminate()
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    fieldX = event.pos[0] - mSt['field'][0]
                    fieldY = event.pos[1] - mSt['field'][1]
                    if fieldRect.collidepoint(event.pos[0], event.pos[1]):
                        fieldState['foods'].append(pygame.Rect(fieldX, fieldY, FOODSIZE, FOODSIZE))
                        fieldState['dirtyRects'].append(pygame.Rect(fieldX + mSt['field'][0], fieldY + mSt['field'][1], FOODSIZE, FOODSIZE))#
                if event.button == 2:
                    fieldX = event.pos[0] - mSt['field'][0]
                    fieldY = event.pos[1] - mSt['field'][1]
                    if fieldRect.collidepoint(event.pos[0], event.pos[1]):
                        for i in range(500):
                            fieldState['foods'].append(pygame.Rect(fieldX, fieldY, FOODSIZE, FOODSIZE))
                            fieldState['dirtyRects'].append(pygame.Rect(fieldX + mSt['field'][0], fieldY + mSt['field'][1], FOODSIZE, FOODSIZE))#
                if event.button == 1:
                    panelX = event.pos[0] - mSt['bigPanel'][0]
                    panelY = event.pos[1] - mSt['bigPanel'][1]
                    pL = (panelX, panelY)
                    if fieldRect.collidepoint(event.pos[0], event.pos[1]):
                        surus.target[0] = event.pos[0] - mSt['field'][0]
                        surus.target[1] = event.pos[1] - mSt['field'][1]
                        surus.targetType = 'mouse'
                        surus.targetSpcfc = 'mouse'
                        surus.seekTarget = False
                    elif panelState['buttonsLoc']['addFoodButton'].collidepoint(pL):
                        panelState['addFood'][0] = 2
                        panelState['addFood'][1] = True
                    elif panelState['buttonsLoc']['dispenseOffButton'].collidepoint(pL):
                        panelState['dispenseOffButton'][0] = 2
                        panelState['dispenseOffButton'][1] = True
                    elif panelState['buttonsLoc']['dispenseOnButton'].collidepoint(pL):
                        panelState['dispenseOnButton'][0] = 2
                        panelState['dispenseOnButton'][1] = True
                    elif panelState['buttonsLoc']['mouseRelease'].collidepoint(pL):
                        panelState['mouseRelease'][0] = 2
                        panelState['mouseRelease'][1] = True
                    elif panelState['buttonsLoc']['radarOffButton'].collidepoint(pL):
                        panelState['radarOffButton'][0] = 2
                        panelState['radarOffButton'][1] = True
                    elif panelState['buttonsLoc']['radarOnButton'].collidepoint(pL):
                        panelState['radarOnButton'][0] = 2
                        panelState['radarOnButton'][1] = True
                        
                if event.button == 3:
                    if fieldRect.collidepoint(event.pos[0], event.pos[1]):
                        abul.target[0] = event.pos[0] - mSt['field'][0]
                        abul.target[1] = event.pos[1] - mSt['field'][1]
                        abul.targetType = 'mouse'
                        abul.targetSpcfc = 'mouse'
                        abul.seekTarget = False
                        
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    panelX = event.pos[0] - mSt['bigPanel'][0]
                    panelY = event.pos[1] - mSt['bigPanel'][1]
                    pL = [panelX, panelY]
                    surus.targetSpcfc = None
                    
                    if panelState['buttonsLoc']['addFoodButton'].collidepoint(pL) and panelState['addFood'][1] == True:
                        fieldState['addFood'][0] = True
                        panelState['addFood'][0] = 1
                    panelState['addFood'][1] = False

                    if panelState['buttonsLoc']['dispenseOffButton'].collidepoint(pL) and panelState['dispenseOffButton'][1] == True:
                        fieldState['foodDispense'] = False
                        foodBurst = False
                        fieldState['dirtyRects'].append(fieldState['foodSwitch'].move(mSt['field'][0], mSt['field'][1]))
                        panelState['dispenseOffButton'][0] = 1
                    panelState['dispenseOffButton'][1] = False

                    if panelState['buttonsLoc']['dispenseOnButton'].collidepoint(pL) and panelState['dispenseOnButton'][1] == True:
                        fieldState['foodDispense'] = True
                        fieldState['dirtyRects'].append(fieldState['foodSwitch'].move(mSt['field'][0], mSt['field'][1]))
                        panelState['dispenseOnButton'][0] = 1
                    panelState['dispenseOnButton'][1] = False
                    
                    if panelState['buttonsLoc']['mouseRelease'].collidepoint(pL) and panelState['mouseRelease'][1] == True:
                        for creature in fieldState['creaturesList']:
                            if creature.targetSpcfc != 'mouse':
                                creature.seekTarget = True
                        panelState['mouseRelease'][0] = 1
                    panelState['mouseRelease'][1] = False

                    if panelState['buttonsLoc']['radarOffButton'].collidepoint(pL) and panelState['radarOffButton'][1] == True:
                        mSt['petScan'][6] = False
                        panelState['radarOffButton'][0] = 1
                    panelState['radarOffButton'][1] = False

                    if panelState['buttonsLoc']['radarOnButton'].collidepoint(pL) and panelState['radarOnButton'][1] == True:
                        mSt['petScan'][6] = True
                        panelState['radarOnButton'][0] = 1
                    panelState['radarOnButton'][1] = False
                    
                if event.button == 3:
                    abul.targetSpcfc = None
                    
            if event.type == MOUSEMOTION:
                panelX = event.pos[0] - mSt['bigPanel'][0]
                panelY = event.pos[1] - mSt['bigPanel'][1]
                pL = (panelX, panelY)
                
                if panelState['buttonsLoc']['addFoodButton'].collidepoint(pL):
                    if panelState['addFood'][0] == 0 or panelState['addFood'][0] == 1:
                        panelState['addFood'][0] = 1
                    if panelState['addFood'][1] == True:
                        panelState['addFood'][0] = 2
                else:
                    panelState['addFood'][0] = 0

                if panelState['buttonsLoc']['dispenseOffButton'].collidepoint(pL):
                    if panelState['dispenseOffButton'][0] == 0 or panelState['dispenseOffButton'][0] == 1:
                        panelState['dispenseOffButton'][0] = 1
                    if panelState['dispenseOffButton'][1] == True:
                        panelState['dispenseOffButton'][0] = 2
                elif not panelState['buttonsLoc']['dispenseOffButton'].collidepoint(pL) and f_down == False:
                    panelState['dispenseOffButton'][0] = 0

                if panelState['buttonsLoc']['dispenseOnButton'].collidepoint(pL):
                    if panelState['dispenseOnButton'][0] == 0 or panelState['dispenseOnButton'][0] == 1:
                        panelState['dispenseOnButton'][0] = 1
                    if panelState['dispenseOnButton'][1] == True:
                        panelState['dispenseOnButton'][0] = 2
                elif not panelState['buttonsLoc']['dispenseOnButton'].collidepoint(pL) and f_down == False:
                    panelState['dispenseOnButton'][0] = 0

                if panelState['buttonsLoc']['mouseRelease'].collidepoint(pL):
                    if panelState['mouseRelease'][0] == 0 or panelState['mouseRelease'][0] == 1:
                        panelState['mouseRelease'][0] = 1
                    if panelState['mouseRelease'][1] == True:
                        panelState['mouseRelease'][0] = 2
                elif not panelState['buttonsLoc']['mouseRelease'].collidepoint(pL) and not q_down:
                    panelState['mouseRelease'][0] = 0

                if panelState['buttonsLoc']['radarOffButton'].collidepoint(pL):
                    if panelState['radarOffButton'][0] == 0 or panelState['radarOffButton'][0] == 1:
                        panelState['radarOffButton'][0] = 1
                    if panelState['radarOffButton'][1] == True:
                        panelState['radarOffButton'][0] = 2
                else:
                    panelState['radarOffButton'][0] = 0

                if panelState['buttonsLoc']['radarOnButton'].collidepoint(pL):
                    if panelState['radarOnButton'][0] == 0 or panelState['radarOnButton'][0] == 1:
                        panelState['radarOnButton'][0] = 1
                    if panelState['radarOnButton'][1] == True:
                        panelState['radarOnButton'][0] = 2
                else:
                    panelState['radarOnButton'][0] = 0
                    

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    petMaster.terminate()
                if event.key == K_a:
                    if mSt['FPS'] == 40:
                        mSt['FPS'] = 2
                    elif mSt['FPS'] == 2:
                        mSt['FPS'] = 40
                if event.key == ord('f'):
                    if fieldState['foodDispense']:
                        panelState['dispenseOffButton'][0] = 2
                    if not fieldState['foodDispense']:
                        panelState['dispenseOnButton'][0] = 2
                    f_down = True
                if event.key == ord('q'):
                    panelState['mouseRelease'][0] = 2
                    q_down = True
                if event.key == ord('d'):
                    debug = not debug
                    print('\n\n\n')####
                if event.key == ord('r'):
                    for creature in fieldState['creaturesList']:
                        if creature.name in fieldState['homes'].keys():
                            creature.rect.centerx = fieldState['homes'][creature.name][0].centerx
                            creature.rect.centery = fieldState['homes'][creature.name][0].centery
                        else:
                            creature.rect.centerx = fieldState['homes']['guest'][0].centerx
                            creature.rect.centery = fieldState['homes']['guest'][0].centery

            if event.type == KEYUP:
                if event.key == K_q:
                    for creature in fieldState['creaturesList']:
                        if creature.targetSpcfc != 'mouse':
                            creature.seekTarget = True
                    panelState['mouseRelease'][0] = 0
                    q_down = False
                if event.key == K_f:
                    fieldState['foodDispense'] = not fieldState['foodDispense']
                    foodBurst = False
                    fieldState['dirtyRects'].append(fieldState['foodSwitch'].move(mSt['field'][0], mSt['field'][1]))#
                    if fieldState['foodDispense']:
                        panelState['dispenseOffButton'][0] = 0
                    if not fieldState['foodDispense']:
                        panelState['dispenseOnButton'][0] = 0
                    f_down = False
              
                 
                
        
        
        # Add new food
        if fieldState['addFood'][0] == True:
            addFood(mSt, fieldState)
            fieldState['addFood'][0] = False
        if fieldState['foodDispense'] == True:
            foodCounter += 1
            if foodCounter >= newfood:
                foodCounter = 0
                fieldState = addFood(mSt, fieldState)
                if foodBurst == False: 
                    newfood = random.randint(15,30)
                    foodBurst = not bool(random.randint(0,10))
                if foodBurst == True:
                    newfood = random.randint(1,3)
                    burstCounter += 1
                    # length of the burst is not predefined, each drop has an increasing chance of ending it
                    if burstCounter >= random.randint(50, 200):
                        foodBurst = False
                        burstCounter = 0
        
        # update the grid's wall cells with field's collidable info
        for x in range(GRIDWIDTH):
            for y in range(GRIDHEIGHT):
                for creature in fieldState['creaturesList']:
                    if (creature.name+' wall') in grid[x][y].pathType:
                        grid[x][y].pathType.remove(creature.name+' wall')
                        grid[x][y].outlineColor = None
                        creature.wallCells.remove(grid[x][y])
                    if grid[x][y].rect.colliderect(creature.rect):
                        grid[x][y].pathType.append(creature.name + ' wall')
                        grid[x][y].outlineColor = ROCK
                        creature.wallCells.append(grid[x][y])

        debug1 = str(grid[3][3].pathType)
        debug2 = str(len(surus.wallCells))



        # creature upkeep
        for creature in fieldState['creaturesList']:
            if creature.cell:
                ''' 'start' and 'end' pathType info is irrelivent for pathfinding module, the module
                is passed the creatures' currrent cell and target cell. This and similar blocks
                are superfluous'''
                creature.cell.pathType.remove(creature.name+' start')
                creature.cell.outlineColor = None
            if creature.targetCell:
                creature.targetCell.pathType.remove(creature.name+' end')
                creature.targetCell.outlineColor = None
                
            fieldState['dirtyRects'].append(creature.rect.move(mSt['field'][0], mSt['field'][1]).inflate(11,11))#
            creature = petAI.upkeep(mSt, creature, fieldState)
            fieldState['dirtyRects'].append(creature.rect.move(mSt['field'][0], mSt['field'][1]).inflate(11,11))#

            cell_x = creature.rect.centerx // CELLSIZE
            cell_y = creature.rect.centery // CELLSIZE
            creature.cell = grid[cell_x][cell_y]
            creature.cell.pathType.append(creature.name+' start')
            creature.cell.outlineColor = GREEN
            target_x = creature.target[0] // CELLSIZE
            if target_x >= GRIDWIDTH:
                target_x = GRIDWIDTH-1
            if target_x < 0:
                target_x = 0
            target_y = creature.target[1] // CELLSIZE
            if target_y >= GRIDHEIGHT:
                target_y = GRIDHEIGHT-1
            if target_y < 0:
                target_y = 0
            creature.targetCell = grid[target_x][target_y]
            creature.targetCell.pathType.append(creature.name+' end')
            creature.targetCell.outlineColor = RED



            

                        
        # update debug text
        textSurusTarget = BASICFONT.render('sTarget: ' + surus.targetType, True, SURUSHOMECOLOR)
        textSurusTummy = BASICFONT.render('sSpeed: ' + str(surus.moveSpeed), True, SURUSHOMECOLOR)
        textSurusHurry = BASICFONT.render('sHurry: ' + str(surus.hurry), True, SURUSHOMECOLOR)
        textAbulTarget = BASICFONT.render('aTarget: ' + abul.targetType, True, ABULHOMECOLOR)
        textAbulTummy = BASICFONT.render('aSpeed: ' + str(abul.moveSpeed), True, ABULHOMECOLOR)
        textAbulHurry = BASICFONT.render('aHurry: ' + str(abul.hurry), True, ABULHOMECOLOR)
        debug1 #= str(fieldState['creaturesList'][0].debug[4])
        debug2 #= str(fieldState['creaturesList'][0].debug[5])
        textDebug1 = BASICFONT.render(debug1, True, BLACK)
        textDebug2 = BASICFONT.render(debug2, True, BLACK)
        textFPS = BASICFONT.render('FPS: ' + str(int(currentFPS)), True, BLACK)

        

        # check if the pet has intersected with any food squares.
        for food in fieldState['foods'][:]:
            for creature in fieldState['creaturesList']:
                if creature.rect.colliderect(food) and creature.targetSpcfc == food:
                    creature.tummy +=1
                    creature.targetSpcfc = None
                    if food in fieldState['foods']:
                        fieldState['foods'].remove(food)
                    fieldState['dirtyRects'].append(food.move(mSt['field'][0], mSt['field'][1]))
                    

        # check if the pet has interacted with the food switch.
        for creature in fieldState['creaturesList']:
            if creature.rect.colliderect(fieldState['foodSwitch']) and creature.targetSpcfc == 'foodSwitch':
                fieldState['foodDispense'] = not fieldState['foodDispense']
                foodBurst = False
                creature.targetSpcfc = 'none'
                fieldState['dirtyRects'].append(fieldState['foodSwitch'].move(mSt['field'][0], mSt['field'][1]))

        # Field items maintenance
        if fieldState['foodDispense'] == True:
            foodSwitchColor = SWITCHON
        if fieldState['foodDispense'] == False:
            foodSwitchColor = SWITCHOFF


        # draw the background
        fieldSurface.fill(FIELDCOLOR)

        # draw the field items
        for i in fieldState['homes'].keys():
            pygame.draw.rect(fieldSurface, fieldState['homes'][i][1], fieldState['homes'][i][0])

        pygame.draw.rect(fieldSurface, foodSwitchColor, fieldState['foodSwitch'])
        pygame.draw.rect(fieldSurface, WATER, fieldState['pond'])
        pygame.draw.ellipse(fieldSurface, WATER, pondShallow)

        pygame.draw.rect(fieldSurface, ROCK, boulder1)
        pygame.draw.rect(fieldSurface, ROCK, boulder2)


        # draw the food
        for i in range(len(fieldState['foods'])):
            pygame.draw.rect(fieldSurface, FOODCOLOR, fieldState['foods'][i])

        # draw the the dudes
        for creature in creaturesList:
            drawLoc = creature.rect.move(-5,-5)
            fieldSurface.blit(creature.surface, drawLoc)

 



        # Debug displays
        if debug == True:

            fieldSurface.blit(textSurusTarget, textSurusTargetRect)
            fieldSurface.blit(textSurusTummy, textSurusTummyRect)
            fieldSurface.blit(textSurusHurry, textSurusHurryRect)
            fieldSurface.blit(textAbulTarget, textAbulTargetRect)
            fieldSurface.blit(textAbulTummy, textAbulTummyRect)
            fieldSurface.blit(textAbulHurry, textAbulHurryRect)
            fieldSurface.blit(textFPS, textFPSRect)
            fieldSurface.blit(textDebug1, textDebug1Rect)
            fieldSurface.blit(textDebug2, textDebug2Rect)
            pygame.draw.circle(fieldSurface, SURUSHOMECOLOR, surus.target, 5, 0)
            pygame.draw.circle(fieldSurface, ABULHOMECOLOR, abul.target, 5, 0)
            if surus.debug[0]: 
                pygame.draw.circle(fieldSurface, GREEN, surus.debug[0][0], 5, 0)
            if surus.debug[1]: 
                pygame.draw.circle(fieldSurface, GREEN, surus.debug[1][0], 5, 0)
            if surus.debug[2]: 
                pygame.draw.circle(fieldSurface, GREEN, surus.debug[2][0], 5, 0)
            if surus.debug[3]: 
                pygame.draw.circle(fieldSurface, GREEN, surus.debug[3][0], 5, 0)
            if surus.debug[4]:
                pygame.draw.circle(fieldSurface, LIGHTRED, surus.debug[4][0], 5, 0)
            if surus.debug[5]:
                pygame.draw.circle(fieldSurface, RED, surus.debug[5][0], 5, 0)
            if surus.waypoints:
                pygame.draw.circle(fieldSurface, WHITE, surus.waypoints[0], 5, 0)

            #grid display:
            for x in list(range(int(GRIDWIDTH))):
                pygame.draw.line(fieldSurface, SWITCHON, (x*CELLSIZE, 0), (x*CELLSIZE, CELLSIZE*GRIDHEIGHT))
            for y in list(range(int(GRIDHEIGHT))):
                pygame.draw.line(fieldSurface, SWITCHON, (0, y*CELLSIZE), (CELLSIZE*GRIDWIDTH, y*CELLSIZE))
            for x in list(range(GRIDWIDTH)):
                for y in list(range(GRIDHEIGHT)):
                    if grid[x][y].outlineColor:
                        pygame.draw.rect(fieldSurface, grid[x][y].outlineColor, grid[x][y].rect, grid[x][y].outlineSize)
        

        # draw the window onto the screen
        windowSurface.blit(fieldSurface, (mSt['field'][0], mSt['field'][1]))
        fieldState['dirtyRects'].append(pygame.Rect(mSt['namePanel'][0],
                                                    mSt['namePanel'][1],
                                                    mSt['namePanel'][4],
                                                    mSt['namePanel'][5]))
        pygame.display.update()
##        pygame.display.update(fieldState['dirtyRects'])
        fieldState['dirtyRects'] = []
        FPSCLOCK.tick(mSt['FPS'])
        currentFPS = FPSCLOCK.get_fps()



def addFood(mSt, fieldState):
    '''randomly adds a piece of foods on the field, but (mostly) not in a collidable object'''
    addFoodx = random.randint(0, mSt['field'][4] - FOODSIZE - 50)
    addFoody = random.randint(0, mSt['field'][5] - FOODSIZE)
    blacklist = []
    for collidable in fieldState['collidables']:
        blacklist.append(collidable)
    for home in fieldState['homes'].keys():
        blacklist.append(fieldState['homes'][home][0])
    for rect in blacklist: 
        potentialFood = pygame.Rect(addFoodx, addFoody, FOODSIZE, FOODSIZE)
        if rect.colliderect(potentialFood):
            if rect.left - FOODSIZE > 0:
                addFoodx = rect.left - FOODSIZE
            elif rect.bottom + FOODSIZE < mSt['field'][5]:
                addFoody = rect.bottom
            elif rect.top - FOODSIZE > 0:
                addFoody = rect.top - FOODSIZE
            elif rect.right + FOODSIZE < mSt['field'][4]:
                addFoodx = rect.right
    fieldState['foods'].append(pygame.Rect(addFoodx, addFoody, FOODSIZE, FOODSIZE))
    fieldState['dirtyRects'].append(pygame.Rect(addFoodx + mSt['field'][0], addFoody + mSt['field'][1], FOODSIZE, FOODSIZE))
    return fieldState
