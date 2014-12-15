# A study in AI
# John Bassage john.bassage@gmail.com

import pygame, sys, random, math, petField, petAI
from pygame.locals import *

WINDOWWIDTH = 1700
WINDOWHEIGHT = 950
OUTSIDEMARGIN = 50
INSIDEMARGIN = 25

# so-called master state library, contains reference info for all panes
mSt = {'FPS'        : 40,
       'window'     : [0, 0, WINDOWWIDTH, WINDOWHEIGHT, 0, 0],
       'field'      : [550,
                       OUTSIDEMARGIN,
                       WINDOWWIDTH - OUTSIDEMARGIN,
                       WINDOWHEIGHT - 200, 0, 0],
       'bigPanel'   : [OUTSIDEMARGIN,
                       OUTSIDEMARGIN,
                       0,
                       WINDOWHEIGHT - OUTSIDEMARGIN * 1.5, 0, 0],
       'namePanel'  : [0, 0, 0, 0, 0, 0],
       'petScan'    : [0, 0, 0, 0, 0, 0, False]}

# automatically calculate various pane placements based on margins and field location
mSt['bigPanel'][2]  = mSt['field'][0] - INSIDEMARGIN
mSt['namePanel'][0] = mSt['field'][0]
mSt['namePanel'][1] = mSt['field'][3] + INSIDEMARGIN
mSt['namePanel'][2] = mSt['field'][2]
mSt['namePanel'][3] = mSt['bigPanel'][3]

mSt['window'][4]    = mSt['window'][2]    - mSt['window'][0]
mSt['window'][5]    = mSt['window'][3]    - mSt['window'][1]
mSt['field'][4]     = mSt['field'][2]     - mSt['field'][0]
mSt['field'][5]     = mSt['field'][3]     - mSt['field'][1]
mSt['bigPanel'][4]  = mSt['bigPanel'][2]  - mSt['bigPanel'][0]
mSt['bigPanel'][5]  = mSt['bigPanel'][3]  - mSt['bigPanel'][1]
mSt['namePanel'][4] = mSt['namePanel'][2] - mSt['namePanel'][0]
mSt['namePanel'][5] = mSt['namePanel'][3] - mSt['namePanel'][1]

mSt['petScan'][4]   = mSt['field'][4]/3.5 + INSIDEMARGIN*2
mSt['petScan'][5]   = mSt['field'][5]/3.5 + INSIDEMARGIN + 50
mSt['petScan'][0]   = mSt['bigPanel'][0] + mSt['bigPanel'][4]/2 \
                      - mSt['petScan'][4]/2
mSt['petScan'][1]   = mSt['bigPanel'][3] - mSt['petScan'][5] - INSIDEMARGIN
mSt['petScan'][2]   = mSt['petScan'][0]  + mSt['petScan'][4]
mSt['petScan'][3]   = mSt['petScan'][1]  + mSt['petScan'][5]


BLACK = (0, 0, 0)
FOODCOLOR = (76, 153, 0)
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




def main():
    global FPSCLOCK, windowSurface, BASICFONT, IMAGESDICT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    windowSurface = pygame.display.set_mode((mSt['window'][2], mSt['window'][3]))
    pygame.display.set_caption('Pets')
    pygame.display.set_icon(pygame.image.load('elephantSouth.png'))

    IMAGESDICT = {'surusSouth': pygame.image.load('surusSouth.png').convert_alpha(),
                  'surusWest': pygame.image.load('surusWest.png').convert_alpha(),
                  'surusNorth': pygame.image.load('surusNorth.png').convert_alpha(),
                  'surusEast': pygame.image.load('surusEast.png').convert_alpha(),
                  'abulSouth': pygame.image.load('abulSouth.png').convert_alpha(),
                  'abulWest': pygame.image.load('abulWest.png').convert_alpha(),
                  'abulNorth': pygame.image.load('abulNorth.png').convert_alpha(),
                  'abulEast': pygame.image.load('abulEast.png').convert_alpha(),
                  'elephant': pygame.image.load('elephantSouth.png').convert_alpha()}


    # set up the pets
    sPos = (300, 100)
    sSurf = IMAGESDICT['surusSouth']
    sSurfList = [IMAGESDICT['surusNorth'],
                         IMAGESDICT['surusEast'],
                         IMAGESDICT['surusSouth'],
                         IMAGESDICT['surusWest']]
    sName = 'surus'
    sRoll = 100
    sLim = (10, 25)

    aPos = (300, 300)
    aSurf = IMAGESDICT['abulNorth']
    aSurfList = [IMAGESDICT['abulNorth'],
                        IMAGESDICT['abulEast'],
                        IMAGESDICT['abulSouth'],
                        IMAGESDICT['abulWest']]
    aName = 'abul'
    aRoll = 40
    aLim = (20, 25)


    
    surus = petAI.Pet(sSurf, sSurfList, sPos, sName, sRoll, sLim)
    abul = petAI.Pet(aSurf, aSurfList, aPos, aName, aRoll, aLim)

    

##    dumbo = petAI.Pet(IMAGESDICT['elephant'],
##                      [IMAGESDICT['elephant'],
##                       IMAGESDICT['elephant'],
##                       IMAGESDICT['elephant'],
##                       IMAGESDICT['elephant']])
    # To enable a third pet, add it to this list, and
    # uncomment the pet above or create a new one
    creaturesList = [surus, abul]



    windowSurface.fill(BLACK)

    petField.launch(mSt, creaturesList)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

