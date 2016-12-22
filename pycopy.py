#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#####################################
#(C)Copyrighting Andrey Zaitsew 2016#
#####################################
try:
    import Foundation
    import objc
    import AppKit
    import sys
    import os
    import termios
    import struct
    import fcntl
except ImportError:
    print "This script could be runned only on Mac OS X 10.7 and later."
    
def set_winsize(row,col):#Sets terminal size
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=row, cols=col))
    
def getTerminalSize():#get terminal size
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
    return int(cr[1]), int(cr[0])   

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):#notifier functiob
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)

    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
    
global SOURCE_FILENAME#name of source filename
global TARGET_FILENAME#name of target filename

def main(argv):#main function
  global SOURCE_FILENAME
  global TARGET_FILENAME
  row, col = getTerminalSize()
  #print str(rows)+","+str(cols)
  if col<110:
     set_winsize(row,110)
  if(len(argv)>1):# if enough arguments we're going to use them
 	 SOURCE_FILENAME=argv[1]
 	 TARGET_FILENAME=argv[2]
  else:#not enough arguments so asking user usin manual input
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
          break#EOF
      target.write(chunk)
      copied += len(chunk)
      p=(copied * 100 / source_size)#counting progress
      print '\r['+'▋'*p+' '*(100-p)+']%02d%%' % p+spinner[i],#printing progress
      if i>=3:
         i=0
      else:
         i=i+1
  source.close()#Closing files
  target.close()
if __name__=="__main__":#if running as script
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
  except Exception as e:
      print str(e)