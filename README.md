# pycopy
Simple utility to copy files in mac os x console with progress.<br></br>
<br>
<b>License:GNU/GPL 3.0</b><br>
https://www.gnu.org/licenses/gpl-3.0.html
<br>
<b>Usage:pycopy.py /path/to/source/file /path/to/destanation/file<br>
      pycopy.py</b><br>
For example:<br>
```sh
./pycopy.py ~/image.img /dev/disk1
```
<br>
will burn image.img to /dev/disk1.<br>
Also you could run it like this:<br>
```sh
./pycopy.py
```
<br>
After this you will be asked to input source and target file:<br>
```sh
SOURCE:/home/User/greenoctocat.txt<br>
DEST:/home/User/redoctocat.txt<br>
```
<br>
After this source file willbe copied to destanatrion file.<br>

```sh
./pycopy.py -u http://domain.extension/path/to/file greenoctocat.txt
```
<br>
This will download file from internet as greenocotocat.txt

