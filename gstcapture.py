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
 imgoverlay = ''' gdkpixbufoverlay location=sqwhite4.png offset-x=300 offset-y=300 name=pixbufover ! '''
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

 for j in range(5, 0, -1):
      #ov.set_property('location', 'sqwhite'+str(j)+'.png')
      txov.set_property('text', str(j))
      time.sleep(0.75)

 time.sleep(0.4)
 for j in range(9):
   txov.set_property('color', 0xFFFF0000)
   txov.set_property('font-desc', 'calibiri 100px')
   txov.set_property('text','Recording')
   time.sleep(0.5)
   txov.set_property('text','')
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
