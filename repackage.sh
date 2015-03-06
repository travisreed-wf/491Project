#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage:   $0 <zipname>   <username>"
  echo "example: $0 build-02-05 aguibert"
  exit 1
fi

zip -r $1.zip ./src -x '*/settingslocal.py'

echo "Note: If you're not on the ISU network, don't forget to VPN!"
echo "Transferrring $1.zip to nirwebportal. . ."

scp ./$1.zip $2@nirwebportal.vrac.iastate.edu:/home/nirwebportal/archives

ssh $2@nirwebportal.vrac.iastate.edu
