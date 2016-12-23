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
    import time
except ImportError:
    print "This script could be runned only on Mac OS X 10.7 and later."

def set_winsize(row,col):#Sets terminal size
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=row, cols=col))
def download(link,file_name):
    try:
          import requests
    except ImportError:
          ans=raw_input("This feature requires requests library.Would you like install it now?[Y/N]:").lower()
          if ans=="y":
            from subprocess import call
            sys.exit(call(["sudo","easy_install","requests"]))
    start=time.clock()#we need it to measure speed
    with open(file_name, "wb") as f:
          print "Downloading to %s" % file_name
          response = requests.get(link, stream=True)
          total_length = response.headers.get('content-length')

          if total_length is None: # no content length header
              f.write(response.content)
          else:
              dl = 0 #downloaded length
              total_length = int(total_length)
              i=0
              spinner=['|','/','-','\\']
              for data in response.iter_content(chunk_size=4096):
                  dl += len(data)
                  f.write(data)# writing to file
                  done = int(100 * dl / total_length)#average of percents done
                  sys.stdout.write("\r["+'▋'*done+' '*(100-done)+"]%02d%%"%done+"("+str(dl//1024//1024)+"/"+str(total_length//1024//1024)+"Mb),"+str(dl//(time.clock() - start)//1024)+"Kb/s"+spinner[i] )    
                  sys.stdout.flush()
                  if i>=3:
                    i=0
                  else:
                    i=i+1
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
def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):#notifier function
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
  if col<140:
     set_winsize(row,140)
  if "-u" in argv:
     download(argv[2],argv[3])
     print "Download complete!"
     sys.exti(0)
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