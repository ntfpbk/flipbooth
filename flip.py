#!/usr/bin/env python

from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import GObject
#from gi.repository import GdkX11    # for window.get_xid()
#from gi.repository import GstVideo  # for sink.set_window_handle()

import os, commands
from string import split, join, lower, upper
import time
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class MyWindow(Gtk.Window):
   def __init__(self):
      Gtk.Window.__init__(self)
    
def window_closed (widget, event):
      widget.hide()
      Gtk.main_quit()

def on_clicked (widget, eventkey):
  print "Clicked!!"

def on_key_release (widget, eventkey):
  # set up a dictionary for maniupating camera settings...
  camctl = {}
  camctl['f'] = camctl['F'] = ['focus_absolute', 5, 0, 250]
  camctl['e'] = camctl['E'] = ['exposure_absolute', 1, 3, 2047]
  camctl['w'] = camctl['W'] = ['white_balance_temperature', 1, 2000, 6500]
  camctl['g'] = camctl['G'] = ['gain', 1, 0, 255]
  camctl['z'] = camctl['Z'] = ['zoom_absolute', 1, 100, 500]

  print 'keyboard:', eventkey.string, repr(eventkey.string)
  if eventkey.string=='q': 
      print 'Quitting...'
      window.destroy()
  if eventkey.string in ['k', 'K']:
      # write semaphore file to tell preview to stop...
      open('/dev/shm/die','w').write('die')
  if eventkey.string=='c':
      print 'Start capturing...'
      os.system('python gstcapture.py')
      widget.queue_draw()
  if eventkey.string=='r': # redraw screen...
      print 'attempted redraw... '
      widget.queue_draw()
  if eventkey.string=='p': # open camera preview to adjust settings...
      print 'Preview (for adjusting camra)...'
      os.system('python gstpreview.py &')
      widget.queue_draw()
  if eventkey.string=='t':
      # lock camera settings...
      print 'Lock camera settings...'
      os.system('v4l2-ctl -d /dev/video1 -c focus_auto=0,exposure_auto=1,white_balance_temperature_auto=0,exposure_auto_priority=0')
  if eventkey.string=='u':
      # unlock camera settings...
      print 'Unlock camera settings...'
      os.system('v4l2-ctl -d /dev/video1 -c focus_auto=1,exposure_auto=3,white_balance_temperature_auto=1,exposure_auto_priority=1')
  # do camera stuff...
  if eventkey.string in camctl.keys():
      a, value = commands.getstatusoutput('v4l2-ctl -d /dev/video1 -C  ' + camctl[eventkey.string][0] )
      value = eval(split(value, ':')[1])
      if lower(eventkey.string)==eventkey.string: 
         value += camctl[eventkey.string][1] 
      else: 
         value -= camctl[eventkey.string][1]
      if value<camctl[eventkey.string][2]: value=camctl[eventkey.string][2]
      if value>camctl[eventkey.string][3]: value=camctl[eventkey.string][3]
      os.system('v4l2-ctl -d /dev/video1 -c ' + camctl[eventkey.string][0] + '=' + str(value))
      print 'New '+camctl[eventkey.string][0], value

if __name__=="__main__":
    Gdk.init([])
    Gtk.init([])

    window = MyWindow()
    window.connect("delete-event", window_closed)
    window.connect("destroy", Gtk.main_quit)
    window.set_default_size (1280,720)

    drawing_area = Gtk.DrawingArea()
    drawing_area.set_double_buffered(True)
    window.add(drawing_area)

    # make window black (which is really full screen...
    drawing_area.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(red=0, green=0, blue=0))

    drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
    drawing_area.connect('button-press-event', on_clicked)
    window.add_events(Gdk.EventMask.KEY_RELEASE_MASK)
    window.connect('key-release-event', on_key_release)

    window.show_all()
    window.realize()
    window.fullscreen()

    Gtk.main()

