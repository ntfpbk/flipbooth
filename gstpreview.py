#!/usr/bin/env python

import time
from gi.repository import Gst
from gi.repository import GObject
import os

Gst.init(None)

 # assemble gst command line...
videosrc = '''v4l2src device=/dev/video1 name=src ! timeoverlay name=tover ! '''
imgoverlay = ''' gdkpixbufoverlay location=sqwhite4.png offset-x=300 offset-y=300 name=pixbufover ! '''
tplusqueue = ''' tee name=t  t. ! queue ! video/x-raw,width=1280,height=720,framerate=30/1 ! queue name=q ! '''
videoflip =  '''  videoflip method=4 name=vflip ! '''
textoverlay = ''' textoverlay text=t valignment=top halignment=center font-desc="calibri 275px" name=txtover ! '''
vidsink = '''  imxipuvideosink   sync=false  name=sink  '''

commandline = videosrc+tplusqueue+videoflip+textoverlay+vidsink 
print '\n', commandline, '\n'

pipe=Gst.parse_launch(commandline)

def main():
 # start gst...
 pipe.set_state(Gst.State.PLAYING)

 #ov = pipe.get_by_name('pixbufover')
 txov = pipe.get_by_name('txtover')

# for j in range(15):
 while (1):
   txov.set_property('color', 0xFF00FF00)
   txov.set_property('font-desc', 'calibiri 65px')
   txov.set_property('text','Adjust camera')
   time.sleep(1)
   txov.set_property('text','')
   time.sleep(1)
   if os.path.exists('/dev/shm/die'):
      os.remove('/dev/shm/die')
      break
 
 # stop gst...
 pipe.set_state(Gst.State.NULL)

 commandline = 'gst-launch-1.0 filesrc location=/home/debian/fgst/black.jpg ! jpegdec ! videoconvert ! imxipuvideosink'
 os.system(commandline)

if __name__ == '__main__':
  main()
