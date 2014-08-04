import time
import SimpleCV

c = SimpleCV.Camera()
vs = SimpleCV.VideoStream("out.avi", 15, False)

framecount = 0
while(framecount < 15 * 20): #record for 5 minutes @ 15fps
    c.getImage().save(vs)
    time.sleep(0.1)
    framecount += 1
