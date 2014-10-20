# Over-ride the build cd function so that visited directories can be
# recorded and used to quickly navigate to the most frequently visited.
function cd(){
  if [[ ${1:0:1} = ":" ]]; then
    builtin cd $(cdhistory -r -n 1 -m ${1:1})
    echo $(pwd)
  else
    cdhistory -a $1
    builtin cd $1
  fi
}

_cd_completion()
{
  local cur=${COMP_WORDS[COMP_CWORD]}
  if [[ "${COMP_CWORD}" -gt 2 ]]; then
    COMPREPLY=()
  elif [[ "${COMP_WORDS[1]}" == ":" ]]; then
    COMPREPLY=( $(cdhistory -n 1 -m ${cur:1}) )
  fi
}

complete -o dirnames -o nospace -F _cd_completion cd
