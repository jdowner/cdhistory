## CDHISTORY

[![Build Status](https://travis-ci.org/jdowner/cdhistory.svg)](https://travis-ci.org/jdowner/cdhistory)


This package is used to record the frequency of visits to particular directories
through the 'cd' function. The goal is to use this information to provide
a way to quickly navigate to commonly visited directories.

To incorporate this functionality, install the package in the usual way,


  python setup.py install


This will add the cdhistory packacge to your python install area, and a
cdhistory script to /usr/local/bin. To incorporate cdhistory into your normal
'cd' use, there is a bash script installed in /usr/local/share called
cdhistory.bash that provides an function to wrap 'cd'.

The cdhistory.bash snippet replaces the existing 'cd' function in bash with a
wrapped version. The function behaves like the builtin cd command normally, but
records the directories that are visited. However, if you prepend the first
argument to 'cd' with a colon it will go to the best match using cdhistory, e.g.


  cd :repos


will 'cd' to the path that best matches the string 'repos'. In effect, this is
like creating aliases for commonly visited directories.
