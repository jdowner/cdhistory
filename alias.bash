# Over-ride the build cd function so that visited directories can be
# recorded and used to quickly navigate to the most frequently visited.
function cd(){
  if [[ ${1:0:1} = ":" ]]; then
    builtin cd $(cdhistory -r -n 1 -m ${1:1})
  else
    cdhistory -a $1
    builtin cd $1
  fi
}
