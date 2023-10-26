# Displays a bouncing logo of the users choice resembling the bouncing DVD Logo.

# Copyright (C) 2023 Thomas Rader

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from tkinter import *
import argparse

# Boundary class so each gif frame can have different collision conditions
class Bounds():
    def __init__(self, image):
        fullWidth = int(imgWidth * 2)
        fullHeight = int(imgHeight * 2)
        self.leftPad = scanImage(image, range(fullWidth), range(fullHeight), False, True) if dynamicCollision else 0
        self.rightPad = scanImage(image, range(fullWidth), range(fullHeight), True, True) if dynamicCollision else 0
        self.upPad = scanImage(image, range(fullHeight), range(fullWidth), False, False) if dynamicCollision else 0
        self.downPad = scanImage(image, range(fullHeight), range(fullWidth), True, False) if dynamicCollision else 0

        # print("left = "+str(self.leftPad)+" right = "+str(self.rightPad)+" up = "+str(self.upPad)+" down = "+str(self.downPad))

# Creating gif class
class Animation():
    def __init__(self,file):
        self.frameTotal = maxFrames(file)
        if animated:
            self.frames = [PhotoImage(file=file,format='gif -index %i' %(i)) for i in range(self.frameTotal)]
            self.bounds = [Bounds(self.frames[i]) for i in range(self.frameTotal)]
        else:
            self.frames = [PhotoImage(file=file)]
            self.bounds = [Bounds(self.frames[0])]

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-name", "-file", "-fileName", type=str, help="name of image file to load", default="dvd.png")
parser.add_argument("-bg", "-backgroundColor", type=str, help="background color of whole window", default="#00FF00")
parser.add_argument("-transparent", "-transparency", action='store_true', help="background transparency of whole window")
parser.add_argument("-width", "-w", type=int, help="width of whole window", default=1920)
parser.add_argument("-height", type=int, help="height of whole window", default=1080)
parser.add_argument("-velX", type=int, help="how fast the image moves in the horizontal direction", default=0)
parser.add_argument("-velY", type=int, help="how fast the image moves in the vertical direction", default=0)
parser.add_argument("-speed", "-velocity", type=int, help="how fast the image moves", default=5)
parser.add_argument("-update", "-tick", type=int, help="how fast the program updates in milliseconds", default=10)
parser.add_argument("-animated", "-gif", action='store_true', help="use if the file is a gif (gif exclusively used for animation)")
parser.add_argument("-animationSpeed", type=int, help="how fast the animation plays (how many ms in between frames)", default=15)
parser.add_argument("-static", "-staticCollision", action='store_false', help="stops dynamic dimensions for collision detection with animated images")
parser.add_argument("-windowed", action='store_false', help="window toggle")
args = parser.parse_args()

name = args.name                                # name of image file
width = args.width                              # width of full window
height = args.height                            # height of full window
backgroundColor = args.bg                       # background color for window
transparent = args.transparent                  # determines if the window is transparent
velX = velY = args.speed                        # how fast the image moves
update = args.update                            # how fast the tick speed is
animated = args.animated                        # use with gif
animationSpeed = args.animationSpeed            # how fast gif plays
dynamicCollision = args.static                  # finds transparent pixels on every side of every frame for dynamic collision
fullscreen = args.windowed                      # fullscreen toggle
geometryDisplay = str(width)+"x"+str(height)    # tkinter display setting accomodating variables
x = 0                                           # location of image
y = 0                                           # location of image
frameTotal = 1                                  # how many frames are in the animated image
frameCount = 0                                  # keeps track of current frame for animation
maxFrameAmount = 99999999                       # avoiding forever loop 
title = "DVD Logo"                              # title for window

# Checking velocities
if args.velX == 0 and args.velY == 0:
    velY = velY + 1
if args.velX != 0:
    velX = args.velX
if args.velY != 0:
    velY = args.velY

# Making sure default name is correct (only use gifs please)
if animated and args.name == 'dvd.png':
    name = 'dvd.gif'

# Make sure that animated is toggled if gif
if not animated and args.name[-4:] == '.gif':
    animated = True

# Create an instance of tkinter
win = Tk()
win.title(title)

# Settings fullscreen
win.attributes("-fullscreen", fullscreen)

# Set the geometry of window
win.geometry(geometryDisplay)

# Add a background color to the window
win.config(bg = backgroundColor)

# Create a transparent window
if transparent == True:
    win.wm_attributes('-transparentcolor',backgroundColor)

# Binding escape key to exit program
win.bind('<Escape>', exit)

# Finding max frame of gif file
def maxFrames(file):
    count = 0
    while count < maxFrameAmount:
        try:
            PhotoImage(file=file,format='gif -index %s'%str(count))
        except:
            return count
        count = count + 1
    exit(1)

# Finds transparent pixels on different sides of image
# rowFirst = horizontal detection; reverse goes opposite way for right/down
def scanImage(image,row,column,reverse,rowFirst):
    count = 0
    if reverse:
        row = reversed(row)
        column = column
    for xC in row: # if !rowFirst then this is technically column
        for yC in column:
            if rowFirst:
                if image.transparency_get(xC,yC) == False:
                    return count
            else:
                if image.transparency_get(yC,xC) == False:
                    return count
        count = count + 1

try:
    # Changing icon on window
    win.iconbitmap("./faceu.ico")
    
    # Grabbing image (getting size for boundary detection)
    imageSize = PhotoImage(file='./%s' %(name))
    imgWidth = imageSize.width()/2
    imgHeight = imageSize.height()/2
    dvdImage = Animation('./%s' %(name))

    # Checking for problems
    if imageSize.width() > width or imageSize.height() > height:
        print("Image bigger than window size.")
        exit(1)
except:
    print("Problem with image, exiting.")
    exit(1)

# Creating canvas
canvas = Canvas(win, width=width, height=height, bg=backgroundColor, bd=0, highlightthickness=0)
canvas.pack()

# Placing image
x = imgWidth-dvdImage.bounds[0].leftPad
y = imgHeight-dvdImage.bounds[0].upPad
img = canvas.create_image(x, y, image=dvdImage.frames[0])

# Updating gif frame
def animation(frameTotal):
    global frameCount
    frameCount += 1
    if frameCount >= frameTotal:
        frameCount = 0
    frame = dvdImage.frames[frameCount]
    canvas.itemconfig(img,image=frame)
    win.after(animationSpeed,animation,dvdImage.frameTotal)

# Loop function
def tick(x,y,velX,velY):
    global frameCount
    # Updating position
    x = x + velX
    y = y + velY
    canvas.move(img,velX,velY)
    if x-imgWidth+dvdImage.bounds[frameCount].leftPad < 0:
        canvas.move(img,0-(x-imgWidth+dvdImage.bounds[frameCount].leftPad),0)
        velX = velX * -1
        x = imgWidth - dvdImage.bounds[frameCount].leftPad
    if x+imgWidth-dvdImage.bounds[frameCount].rightPad > width:
        canvas.move(img,width-(x+imgWidth-dvdImage.bounds[frameCount].rightPad),0)
        velX = velX * -1
        x = width - imgWidth + dvdImage.bounds[frameCount].rightPad
    if y-imgHeight+dvdImage.bounds[frameCount].upPad < 0:
        canvas.move(img,0,0-(y-imgHeight+dvdImage.bounds[frameCount].upPad))
        velY = velY * -1
        y = imgHeight - dvdImage.bounds[frameCount].upPad
    if y+imgHeight-dvdImage.bounds[frameCount].downPad > height:
        canvas.move(img,0,height-(y+imgHeight-dvdImage.bounds[frameCount].downPad))
        velY = velY * -1
        y = height - imgHeight + dvdImage.bounds[frameCount].downPad

    win.after(update,tick,x,y,velX,velY)

# Main loop
win.after(0,tick,x,y,velX,velY)

# Animation
if animated:
    win.after(0,animation,dvdImage.frameTotal)

win.mainloop()