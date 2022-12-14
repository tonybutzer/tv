#!/bin/bash

IP=`hostname -I | awk '{print $2}'`
#echo "ssh -N -L 8888:`hostname`:8888  `whoami`@`hostname`"
cd $HOME
echo ${IP}
jupyter lab --no-browser --ip=${IP} --port=2376 --NotebookApp.token=''
