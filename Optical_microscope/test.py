from SimpleCV import *
x = int(input('Put integer to select camera: '))
cam = Camera(x)
disp = Display()

while disp.isNotDone():
        img = cam.getImage()
        txt = 'Hello world'
        img.drawText(txt, x=0, y=0, fontsize=48)
        if disp.mouseLeft:
                break
        img.save(disp)
