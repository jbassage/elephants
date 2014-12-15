Pet Elephants, for python 3.2 and pygame
John Bassage

So this is a thing, like a game but you can just watch it. I wanted to practice writing a pet. It won't work on its own like this, it isn't set up to be deployable at all. It needs to be opened in the python 3.2 IDLE and run from there, and it needs pygame and also it isn't . That's from pygame.org. They have their own documentation and looking that up will beat the hell out of me trying to remember what I did with it two years ago.

Once you have pygame, the main module of this elephants thing is petMaster.py. That's the one that needs to be run.

Instructions:

The game depicts an elephant pen with two elephants. Surus lives int he blue corner, and Abul lives in the brown corner. They both eat green food, which is automatically dispensed across the field. The food dispenser can be turned off or on by the elephants, using the grey switch in the lower right corner. The user can turn the food dispenser on or off using the siwtch ont he panel to the left. The panel also displays how much food there is on the field, and can be used to add food. The mouse scroll wheel can also be used to add food, and a middle click will add 500 pieces of food.

Click and drag the mouse to force the elephants to follow the cursor. They can be released from mouse control using either the panel button or the E key.

Controls:

Left click: control Surus

Right click: control Abul

Scroll up or down: place 1 food

Middle click: place 500 food

e: Release elephants from mouse control

d: see debug text and pathfinding grid view

a: slow-mo mode (also for debugging)

f: flip food siwtch

q: release elephants from mouse control

r: reset elephant position to their houses

=========
