#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

##############################################
#(C)Copyrighting Andrey Zaitsew 2016         #
#Licensed under GNU/GPL 3.0                  #
#https://www.gnu.org/licenses/gpl-3.0.html   #
##############################################

###############################
#This script is for python 2.7#
#Branch for linux computers   #
###############################
try:
    import sys
    import os
    import time
except ImportError as e:
    print "Could not run script:library not found("+str(e)+")"


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
                  sys.stdout.write("\r["+'▋'*done+' '*(100-done)+"]%02d%%"%done+"("+str(dl//1024//1024)+"/"+str(total_length//1024//1024)+"Mb),"+str((dl//(time.clock() - start))//1024)+"Kb/s"+spinner[i] )    
                  sys.stdout.flush()
                  if i>=3:
                    i=0
                  else:
                    i=i+1
                    
global SOURCE_FILENAME#name of source filename
global TARGET_FILENAME#name of target filename
#commit me

def ver():
  print "Version:1.0.0-prerelease"
  sys.exit(0)
ver()
def main(argv):#main function
  global SOURCE_FILENAME
  global TARGET_FILENAME
  if "-v" in argv:
     ver()
  if "-u" in argv:
     download(argv[2],argv[3])
     print "\nDownload complete!"
     sys.exit(0)
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
  except KeyboardInterrupt:
      print "Operation terminated!"
  except OSError,IOError:
      print "Could not open file!Check if file exists and you have right permissions."
  except Exception as e:
      print str(e)
