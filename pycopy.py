#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
   
import Foundation
import objc
import AppKit
import sys
import os
import termios
import struct
import fcntl


def set_winsize(row,col):
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=row, cols=col))
    
def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])   

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)

    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
    
global SOURCE_FILENAME
global TARGET_FILENAME

def main(argv):
  global SOURCE_FILENAME
  global TARGET_FILENAME
  row, col = getTerminalSize()
  #print str(rows)+","+str(cols)
  if col<110:
     set_winsize(row,110)
  if(len(argv)>1):
 	 SOURCE_FILENAME=argv[1]
 	 TARGET_FILENAME=argv[2]
  else:
     SOURCE_FILENAME=raw_input("SOURCE:")
     TARGET_FILENAME=raw_input("DEST:")
  source_size = os.stat(SOURCE_FILENAME).st_size
  copied = 0
  source = open(SOURCE_FILENAME, 'rb')
  target = open(TARGET_FILENAME, 'wb')
  i=0
  spinner=['|','/','-','\\']
  while True:
      chunk = source.read(32768)
      if not chunk:
          break
      target.write(chunk)
      copied += len(chunk)
      p=(copied * 100 / source_size)
      print '\r['+'▋'*p+' '*(100-p)+']%02d%%' % p+spinner[i],
      if i>=3:
         i=0
      else:
         i=i+1
  source.close()
  target.close()
if __name__=="__main__":
  try:
      global SOURCE_FILENAME
      global TARGET_FILENAME
      main(sys.argv)
      print "\n\aDone!"
      notify("Copy"," ","Succesful copied "+os.path.splitext(SOURCE_FILENAME)[0]+" from "+os.path.dirname(os.path.abspath(SOURCE_FILENAME))+" to "+os.path.dirname(os.path.abspath(TARGET_FILENAME))+" as "+os.path.splitext(TARGET_FILENAME)[0])
  except KeyboardInterrupt:
      print "Operation terminated!"
  except OSError,IOError:
      print "Could not open file!Check if file exists and you have right permissions."