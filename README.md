## CDHISTORY

This script is used to record the frequency of visits to particular directories
through using the 'cd' function. The goal is to use this information to provide
a way to quickly navigate to commonly visited directories.

To incorporate this functionality, first make sure that cdhistory.py is
available on your path and is executable. I like to create a symlink from the
version in the repo to home/jdowner/bin, where it is called 'cdhistory'. Then
add the following snippet to your .bash_profile or wherever you keep such
things,

    function cd(){
      if [[ ${1:0:1} = ":" ]]; then
        builtin cd $(cdhistory -n 1 -m ${1:1})
      else
        cdhistory -a $1
        builtin cd $1
      fi
    }

This replaces the existing 'cd' function in bash with a wrapped version. The
function behaves like the builtin cd command normally, but records the
directories that are visited. However, if you prepend the first argument to 'cd'
with a colon it will go to the best match using cdhistory, e.g.

  cd :repos

will 'cd' to the path that best matches the string 'repos'. In effect, this is
like creating aliases for commonly visited directories.
