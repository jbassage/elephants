import pygame, sys, random, math, petMaster, petAI
from pygame.locals import *


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FOODCOLOR = (76, 153, 0)
DARKFOOD = (51, 102, 0)
MEDLFOOD = (102, 204, 0)
LIGHTFOOD = (128, 255, 0)
WHITE = (255, 255, 255)
surusColor = [0, 125, 255]
abulColor = [255, 128, 0]
FIELDCOLOR = (255, 255, 153)
SURUSHOMECOLOR = (0, 0, 102)
ABULHOMECOLOR = (102, 51, 0)
GUESTHOMECOLOR = (153, 153, 0)
SWITCHON = (192, 192, 192)
SWITCHMED = (96, 96, 96)
SWITCHOFF = (32, 32, 32)
SWITCHBRIGHT = (224, 224, 224)
ROCK = (128, 128, 128)
WATER = (51, 153, 255)
RED = (204, 0, 0)
LIGHTRED = (255, 0, 0)
PANELCOLOR = (255, 255, 204)



def launchPanels(mSt, state, panelState):
    global windowSurface
    windowSurface = pygame.display.get_surface()
    panelState['dirtyRects'] = []

    panelState = bigPanel(mSt, state, panelState)
    namePanel(mSt, state)
    if mSt['petScan'][6] == True:
        petScan(mSt, state)
    panelState['dirtyRects'].append(pygame.Rect(mSt['petScan'][0] - mSt['bigPanel'][0],
                                                mSt['petScan'][1] - mSt['bigPanel'][1],
                                                mSt['petScan'][4],
                                                mSt['petScan'][5]))
        

    return panelState
    

def bigPanel(mSt, state, panelState):
    global windowSurface

    panelSurface = pygame.Surface((mSt['bigPanel'][4], mSt['bigPanel'][5]))
    panelSurface.fill(PANELCOLOR)

    BASICFONT = pygame.font.SysFont(None, 32)
    foodBarLen = 0

    # FOOD block
    textRemind = BASICFONT.render('FOOD', True, BLACK)
    textRemindRect = textRemind.get_rect()
    textRemindRect.top = 20
    textRemindRect.centerx = mSt['bigPanel'][4]/2

    if len(state['foods']) >= 100:
        foodBarLen = 400
    else:
        foodBarLen = len(state['foods']) * 4

    foodBarTop = pygame.Rect(0, 50, foodBarLen, 15)
    foodBarBottom = pygame.Rect(0, 65, foodBarLen, 15)
    foodBarBack = pygame.Rect(0, 50, 400, 30)
    foodBarBack.centerx = mSt['bigPanel'][4]/2
    foodBarTop.left = foodBarBack.left
    foodBarBottom.left = foodBarBack.left

    panelState['dirtyRects'].append(foodBarBack)#

    if len(state['foods']) > 100:
        foodTextColor = RED
    else:
        foodTextColor = BLACK

    addFoodButton = pygame.Rect( 0, 85, 60, 30)
    addFoodButton.right = foodBarBack.right
    panelState['buttonsLoc']['addFoodButton'] = addFoodButton
    panelState['dirtyRects'].append(addFoodButton)#
    if panelState['addFood'][0] == 0:
        addFoodButtonColor = FOODCOLOR
    elif panelState['addFood'][0] == 1:
        addFoodButtonColor = MEDLFOOD
    elif panelState['addFood'][0] == 2:
        addFoodButtonColor = LIGHTFOOD
        
    textFoodNum = BASICFONT.render('Food: ' + str(len(state['foods'])),
                                   True, foodTextColor)
    textFoodNumRect = textFoodNum.get_rect()
    textFoodNumRect.top = 90
    textFoodNumRect.left = foodBarBack.left
    panelState['dirtyRects'].append(textFoodNumRect.inflate(50,0))#
    
    textAddFoodButton = BASICFONT.render('Add', True, BLACK)
    textAddFoodButtonRect = textAddFoodButton.get_rect()
    textAddFoodButtonRect.center = addFoodButton.center
    
    textDispenser = BASICFONT.render('Dispenser:', True, BLACK)
    textDispenserRect = textDispenser.get_rect()
    textDispenserRect.top = 110
    textDispenserRect.centerx = mSt['bigPanel'][4]/2

    dispenseOffButton = pygame.Rect(0, 135, 60, 40)
    dispenseOnButton = pygame.Rect(0, 135, 60, 40)
    dispenseOffButton.right = mSt['bigPanel'][4]/2
    dispenseOnButton.left = mSt['bigPanel'][4]/2
    panelState['buttonsLoc']['dispenseOffButton'] = dispenseOffButton
    panelState['buttonsLoc']['dispenseOnButton'] = dispenseOnButton
    panelState['dirtyRects'].append(dispenseOffButton)#
    panelState['dirtyRects'].append(dispenseOnButton)#

    if state['foodDispense'] == True:
        dispenseOnColor = SWITCHON
        if panelState['dispenseOffButton'][0] == 0:
            dispenseOffColor = SWITCHOFF
        elif panelState['dispenseOffButton'][0] == 1:
            dispenseOffColor = SWITCHMED
        elif panelState['dispenseOffButton'][0] == 2:
            dispenseOffColor = SWITCHBRIGHT
    elif state['foodDispense'] == False:
        dispenseOffColor = SWITCHON
        if panelState['dispenseOnButton'][0] == 0:
            dispenseOnColor = SWITCHOFF
        elif panelState['dispenseOnButton'][0] == 1:
            dispenseOnColor = SWITCHMED
        elif panelState['dispenseOnButton'][0] == 2:
            dispenseOnColor = SWITCHBRIGHT

    textDispenseOff = BASICFONT.render('Off', True, BLACK)
    textDispenseOffRect = textDispenseOff.get_rect()
    textDispenseOffRect.center = dispenseOffButton.center

    textDispenseOn = BASICFONT.render('On', True, BLACK)
    textDispenseOnRect = textDispenseOn.get_rect()
    textDispenseOnRect.center = dispenseOnButton.center

    # ELEPHANTS block
    textElephants = BASICFONT.render('ELEPHANTS', True, BLACK)
    textElephantsRect = textElephants.get_rect()
    textElephantsRect.top = dispenseOffButton.bottom + 40
    textElephantsRect.centerx = mSt['bigPanel'][4]/2

    mouseReleaseButton = pygame.Rect( 0, 0, 0, 30)
    mouseReleaseButton.top = textElephantsRect.top + 30
    textMouseRelease = BASICFONT.render('Release from mouse control', True, BLACK)
    textMouseReleaseRect = textMouseRelease.get_rect()
    mouseReleaseButton.width = textMouseReleaseRect.width + 15
    mouseReleaseButton.centerx = mSt['bigPanel'][4]/2
    textMouseReleaseRect.center = mouseReleaseButton.center
    panelState['buttonsLoc']['mouseRelease'] = mouseReleaseButton
    panelState['dirtyRects'].append(mouseReleaseButton)#
    if panelState['mouseRelease'][0] == 0:
        mouseReleaseButtonColor = SWITCHON
    elif panelState['mouseRelease'][0] == 1:
        mouseReleaseButtonColor = SWITCHBRIGHT
    elif panelState['mouseRelease'][0] == 2:
        mouseReleaseButtonColor = WHITE
    
    textRadarSwitch = BASICFONT.render('Pet radar:', True, BLACK)
    textRadarSwitchRect = textRadarSwitch.get_rect()
    textRadarSwitchRect.top = mouseReleaseButton.bottom + 20
    textRadarSwitchRect.centerx = mSt['bigPanel'][4]/2

    radarOffButton = pygame.Rect(0, 0, 60, 40)
    radarOnButton = pygame.Rect(0, 0, 60, 40)
    radarOffButton.top = textRadarSwitchRect.bottom + 5
    radarOnButton.top = textRadarSwitchRect.bottom + 5
    radarOffButton.right = mSt['bigPanel'][4]/2
    radarOnButton.left = mSt['bigPanel'][4]/2
    panelState['buttonsLoc']['radarOffButton'] = radarOffButton
    panelState['buttonsLoc']['radarOnButton'] = radarOnButton
    panelState['dirtyRects'].append(radarOffButton)#
    panelState['dirtyRects'].append(radarOnButton)#

    if mSt['petScan'][6] == True:
        radarOnColor = SWITCHON
        if panelState['radarOffButton'][0] == 0:
            radarOffColor = SWITCHOFF
        elif panelState['radarOffButton'][0] == 1:
            radarOffColor = SWITCHMED
        elif panelState['radarOffButton'][0] == 2:
            radarOffColor = SWITCHBRIGHT
    elif mSt['petScan'][6] == False:
        radarOffColor = SWITCHON
        if panelState['radarOnButton'][0] == 0:
            radarOnColor = SWITCHOFF
        elif panelState['radarOnButton'][0] == 1:
            radarOnColor = SWITCHMED
        elif panelState['radarOnButton'][0] == 2:
            radarOnColor = SWITCHBRIGHT

    textRadarOff = BASICFONT.render('Off', True, BLACK)
    textRadarOffRect = textRadarOff.get_rect()
    textRadarOffRect.center = radarOffButton.center

    textRadarOn = BASICFONT.render('On', True, BLACK)
    textRadarOnRect = textRadarOn.get_rect()
    textRadarOnRect.center = radarOnButton.center

    petScanBackgrnd = pygame.Rect(0, 0, 0, 0)
    petScanBackgrnd.left   = mSt['petScan'][0] - mSt['bigPanel'][0] - 1
    petScanBackgrnd.top    = mSt['petScan'][1] - mSt['bigPanel'][1] - 1
    petScanBackgrnd.width  = mSt['petScan'][4] + 2
    petScanBackgrnd.height = mSt['petScan'][5] + 2


    pygame.draw.rect(panelSurface, BLACK, foodBarBack)
    pygame.draw.rect(panelSurface, LIGHTRED, foodBarTop)
    pygame.draw.rect(panelSurface, RED, foodBarBottom)
    pygame.draw.rect(panelSurface, addFoodButtonColor, addFoodButton)
    pygame.draw.rect(panelSurface, dispenseOffColor, dispenseOffButton)
    pygame.draw.rect(panelSurface, dispenseOnColor, dispenseOnButton)
    pygame.draw.rect(panelSurface, mouseReleaseButtonColor, mouseReleaseButton)
    pygame.draw.rect(panelSurface, radarOffColor, radarOffButton)
    pygame.draw.rect(panelSurface, radarOnColor, radarOnButton)
    pygame.draw.rect(panelSurface, BLACK, petScanBackgrnd, 1)
    
    panelSurface.blit(textDispenseOff, textDispenseOffRect)
    panelSurface.blit(textDispenseOn, textDispenseOnRect)
    panelSurface.blit(textDispenser, textDispenserRect)
    panelSurface.blit(textAddFoodButton, textAddFoodButtonRect)
    panelSurface.blit(textRemind, textRemindRect)
    panelSurface.blit(textFoodNum, textFoodNumRect)
    panelSurface.blit(textElephants, textElephantsRect)
    panelSurface.blit(textMouseRelease, textMouseReleaseRect)
    panelSurface.blit(textRadarSwitch, textRadarSwitchRect)
    panelSurface.blit(textRadarOff, textRadarOffRect)
    panelSurface.blit(textRadarOn, textRadarOnRect)
    
        
    windowSurface.blit(panelSurface, (mSt['bigPanel'][0], mSt['bigPanel'][1]))

    return panelState

def namePanel(mSt, state):
    global windowSurface
    
    panelSurface = pygame.Surface((mSt['namePanel'][4], mSt['namePanel'][5]))
    panelSurface.fill(SWITCHOFF)

    PANELFONT = pygame.font.SysFont(None, 115)


    if state['creaturesList'][0].rect.colliderect(state['homes']['surus'][0]):
        surusFontColor = WHITE
    else:
        surusFontColor = SWITCHON

    if state['creaturesList'][1].rect.colliderect(state['homes']['abul'][0]):
        abulFontColor = WHITE
    else:
        abulFontColor = SWITCHON
    
    MIDHEIGHT = mSt['namePanel'][5]/2
    
    textSurusName = PANELFONT.render('Surus', True, surusFontColor)
    textSurusNameRect = textSurusName.get_rect()
    textSurusNameRect.left = 0
    textSurusNameRect.centery = MIDHEIGHT

    textOtherName = PANELFONT.render('and', True, SWITCHON)
    textOtherNameRect = textOtherName.get_rect()
    textOtherNameRect.topleft = [textSurusNameRect.right + 50,
                                 textSurusNameRect.top]
    
    textAbulName = PANELFONT.render('Abul', True, abulFontColor)
    textAbulNameRect = textAbulName.get_rect()
    textAbulNameRect.topleft = [textOtherNameRect.right + 50,
                                textSurusNameRect.top]

    margins = mSt['namePanel'][4] - textAbulNameRect.right
    textSurusNameRect.left = margins/2
    textOtherNameRect.left = textSurusNameRect.right + 50
    textAbulNameRect.left = textOtherNameRect.right + 50

    
    panelSurface.blit(textAbulName, textAbulNameRect)
    panelSurface.blit(textOtherName, textOtherNameRect)
    panelSurface.blit(textSurusName, textSurusNameRect)
  

    windowSurface.blit(panelSurface, (mSt['namePanel'][0],mSt['namePanel'][1]))

def petScan(mSt, state):
    global windowSurface
    INMARG = mSt['field'][0] - mSt['bigPanel'][2]
    
    panelSurface = pygame.Surface((mSt['petScan'][4], mSt['petScan'][5]))
    panelSurface.fill(FIELDCOLOR)

    PANELFONT = pygame.font.SysFont(None, 25)


    textScanTitle = PANELFONT.render('Pet RADAR', True, BLACK)
    textScanTitleRect = textScanTitle.get_rect()
    textScanTitleRect.centery = 25
    textScanTitleRect.centerx = mSt['petScan'][4]/2

    scanScreen = pygame.Rect(0, 50, mSt['field'][4]/3.5, mSt['field'][5]/3.5)
    scanScreen.centerx = mSt['petScan'][4]/2

    abulBlip = pygame.Rect(0, 0, 14, 14)
    abulBlip.centerx = state['creaturesList'][1].rect.centerx/3.5 + INMARG
    abulBlip.centery = state['creaturesList'][1].rect.centery/3.5 + 50

    surusBlip = pygame.Rect(0, 0, 14, 14)
    surusBlip.centerx = state['creaturesList'][0].rect.centerx/3.5 + INMARG
    surusBlip.centery = state['creaturesList'][0].rect.centery/3.5 + 50
    

    pygame.draw.rect(panelSurface, BLACK, scanScreen)
    pygame.draw.rect(panelSurface, abulColor, abulBlip)
    pygame.draw.rect(panelSurface, surusColor, surusBlip)

    for creature in state['creaturesList']:
        if creature.name != 'surus' and creature.name != 'abul':
            blip = pygame.Rect(0, 0, 14, 14)
            blip.centerx = creature.rect.centerx/3.5 + 25
            blip.centery = creature.rect.centery/3.5 + 50
            pygame.draw.rect(panelSurface, GREEN, blip)
    
    panelSurface.blit(textScanTitle, textScanTitleRect)

    windowSurface.blit(panelSurface, (mSt['petScan'][0], mSt['petScan'][1]))
