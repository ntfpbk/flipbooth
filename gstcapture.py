#!/usr/bin/env python
def main():
 import time
 from gi.repository import Gst
 from gi.repository import GObject
 import os
 import threading

 os.chdir('/dev/shm')
 dirname = 'd' + str(hex(int(time.time())))
 os.system('mkdir ' + dirname)

 def makemp4():
    os.system('/home/debian/fgst/mkmp4 /home/debian/fgst/'+dirname)

 Gst.init(None)

 # assemble gst command line...
 videosrc = '''v4l2src device=/dev/video1 name=src ! timeoverlay name=tover ! '''
# imgoverlay = ''' gdkpixbufoverlay location=/home/debian/fgst/flipbooth/viewfinder1.png name=pixbufover ! '''
 tplusqueue = ''' tee name=t  t. ! queue ! video/x-raw,width=1280,height=720,framerate=30/1 ! queue name=q ! '''
 videoflip =  '''  videoflip method=4 name=vflip ! '''
 textoverlay = ''' textoverlay text=t valignment=top halignment=center font-desc="calibri 275px" name=txtover ! '''
 vidsink = '''  imxipuvideosink   sync=false  name=sink  '''
 queue2 =  ''' t. ! queue name=q2 ! videorate name=vidrate ! video/x-raw,framerate=4/1 ! queue name=q3 ! '''
 jpegenc = ''' jpegenc name=jpegenc ! '''
 multfilesink = '''  multifilesink location="''' + dirname + '''/frame%04d.jpg" async=false name=mfsink  '''

 commandline = videosrc+tplusqueue+videoflip+textoverlay+vidsink + queue2+jpegenc+multfilesink
 print '\n', commandline, '\n'

 pipe=Gst.parse_launch(commandline)

 # start gst...
 pipe.set_state(Gst.State.PLAYING)

 #ov = pipe.get_by_name('pixbufover')
 txov = pipe.get_by_name('txtover')

 # generate countdown...
 for j in range(5, 0, -1):
      txov.set_property('text', str(j))
      time.sleep(0.75)

 txov.set_property('text', '') # clear countdown text...

 # overlaying image makes time lag waaaaay too long....
 # change overlay so that it has the record dot...
 #imgov = pipe.get_by_name('pixbufover')
 #imgov.set_property('location', '/home/debian/fgst/flipbooth/viewfinder2.png')

 time.sleep(0.4)
 for j in range(9): # use for 0.5 blink rate for text...
# for j in range(10): # use for 0.35 blink rate for viewfinder overlay...
   txov.set_property('color', 0xFFFF0000)
   txov.set_property('font-desc', 'calibiri 100px')
   txov.set_property('text','Recording')
#   imgov.set_property('location', '/home/debian/fgst/flipbooth/viewfinder2.png')
   time.sleep(0.5)
   txov.set_property('text','')
#   imgov.set_property('location', '/home/debian/fgst/flipbooth/viewfinder1.png')
   time.sleep(0.5)

 # stop gst...
 pipe.set_state(Gst.State.NULL)

 os.system('cd /dev/shm/'+dirname+' ; rm frame000* frame001[0-5]*')
 os.system('mv /dev/shm/'+dirname+' /home/debian/fgst/')

 begin =  time.time()
 t = threading.Thread(target=makemp4, args=('') ) 
 t.start()

 play = 'gst-launch-1.0 multifilesrc location=/home/debian/fgst/'+dirname+'/frame%04d.jpg start-index=16 ' +\
        'caps="image/jpeg,framerate=\(fraction\)4/1"   !  jpegdec  ! imxipuvideosink'
 print play

 living = True
 while(living):
   os.system(play)
   living = t.isAlive()

 print time.time() - begin

if __name__ == '__main__':
  main()
