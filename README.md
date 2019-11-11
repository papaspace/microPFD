![alt text](http://www.papaspace.at/images/PAPASPACE_LOGO_NEW.png)
 
# microPFD
![alt text](http://www.papaspace.at/images/microPFD.png)

The microPFD software is a tiny but functional Primary Flight Display (PFD) for iOS, which was developed to demonstrate the capabilities of consumer hardware in aviation. As open-source software it is available for free, however requires Pythonista 3 to be installed. While microPFD may also become a life saver in scenarios where aircraft avionics equipment fails, it is not intended to be used as a primary navigation equipment for aviation.


## Installation and Usage
Installation:
1. Download the iOS App Pythonista 3 to your iOS device (iPhone or iPad).
2. Make a new script (e.g. 'pfd_installer.py'), and copy-paste the following code:
```
import urllib, os

print 'Starting download of microPFD. This may take some time.'
if not os.path.exists('microPFD'):
	os.makedirs('microPFD')
if not os.path.exists('microPFD/navdata'):
	os.makedirs('microPFD/navdata')

gitrepo='https://raw.githubusercontent.com/papaspace/microPFD/master/microPFD/'
files=['Main.py', 'symbolgen.py', 'navutil.py', 'navdata/airports.csv']
for file in files:
	print '  Downloading file: '+str(file)
	fid=urllib.urlopen(gitrepo+file)
	fout=open('microPFD/'+file,'w')
	fout.write(fid.read().decode('utf-8'))
	fout.close()
print 'Done' 
```

3. Run the script by tapping the wrench icon and selecting 'Run Options...', 'Run with Python 2.7'.
   A folder named 'microPFD' will be created, the program and database will be downloaded.

Usage and Help:
1. Run the script 'microPFD/Main.py' with Python 2.7.
2. Tap the digital heading display to switch to GPS track.
3. Tap the digital waypoint information display to make a direct-to leg by entering a 4 letter ICAO airport code.
4. Tap the cross in the top-right corner to exit microPFD and return to the Pythonista console.

## Liability Disclaimer
This program is provided as is, without any representation or warranty of any kind, either expressed or implied, including without any limitation any representations or endorsements regarding the use of, the results of, or performance of the product, its appropriateness, accuracy, reliability, or correctness. The entire risk as to the use of this product is assumed by the user. The owners do not assume liability for the use of this program. In no event will the owners be liable for direct or indirect damages including any lost profits, lost savings, or other incidental or consequential damages arising from any defects, or the use, or inability to use this program, even if the owners have been advised of the possibility of such damages.

## Licensing
This software is licensed under CC BY-NC-SA 4.0
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
See: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

Original author: Michael Braunstingl, 2018-2019 (m.braunstingl[at]papaspace.at)

The navigation database was originally downloaded from http://ourairports.com/data/.

