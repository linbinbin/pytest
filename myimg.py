import time
import SimpleCV

c = SimpleCV.Camera()
d = SimpleCV.Display()
while not d.isDone():
    c.getImage().save(d)
c.getImage().save("simplecv.png")
