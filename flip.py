#!/usr/bin/env python

from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import GObject
#from gi.repository import GdkX11    # for window.get_xid()
#from gi.repository import GstVideo  # for sink.set_window_handle()

import os, commands
from string import split, join
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
  print 'keyboard:', eventkey.string, repr(eventkey.string)
  if eventkey.string=='q': 
      print 'Quitting...'
      window.destroy()
  if eventkey.string=='c':
      print 'Start capturing...'
      os.system('python gstcapture.py')
      widget.queue_draw()
  if eventkey.string=='r':
      print 'attempted redraw... '
      widget.queue_draw()
  if eventkey.string=='p':
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
  if eventkey.string in ['y','v']:
      a, wb = commands.getstatusoutput('v4l2-ctl -d /dev/video1 -C  white_balance_temperature')
      wb = eval(split(wb, ':')[1])
      if eventkey.string=='y': wb +=20
      if eventkey.string=='v': wb -=20
      if wb<2000: wb=2000
      if wb>6500: wb=6500
      os.system('v4l2-ctl -d /dev/video1 -c white_balance_temperature='+str(wb))
      print 'New white balance:', wb
  if eventkey.string == 'D':
      os.system('v4l2-ctl -d /dev/video1  -C brightness -C contrast -C saturation -C white_balance_temperature_auto -C gain -C power_line_frequency -C white_balance_temperature -C sharpness -C backlight_compensation -C exposure_auto -C exposure_absolute -C exposure_auto_priority -C pan_absolute -C tilt_absolute -C focus_absolute -C focus_auto -C zoom_absolute -C led1_mode -C led1_frequency')
  if eventkey.string == 'd':
      os.system('v4l2-ctl -d /dev/video1  -C white_balance_temperature_auto -C gain -C white_balance_temperature -C exposure_auto -C exposure_absolute -C focus_absolute -C focus_auto')
  if eventkey.string in ['g','G']:
      a, wb = commands.getstatusoutput('v4l2-ctl -d /dev/video1 -C  gain')
      wb = eval(split(wb, ':')[1])
      if eventkey.string=='G': wb +=5
      if eventkey.string=='g': wb -=5
      if wb<0: wb=0
      if wb>255: wb=255
      os.system('v4l2-ctl -d /dev/video1 -c gain='+str(wb))
      print 'New gain:', wb
  if eventkey.string in ['e','E']:
      a, wb = commands.getstatusoutput('v4l2-ctl -d /dev/video1 -C  exposure_absolute')
      wb = eval(split(wb, ':')[1])
      if eventkey.string=='E': wb +=20
      if eventkey.string=='e': wb -=20
      if wb<3: wb=3
      if wb>2047: wb=2047
      os.system('v4l2-ctl -d /dev/video1 -c exposure_absolute='+str(wb))
      print 'New exposure:', wb


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

