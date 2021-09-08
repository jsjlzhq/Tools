#!/bin/bash

thisDir="$(cd `dirname "$0"` && pwd )"
cd "$thisDir"

if [ ! -d log ]; then
    mkdir log
fi

filepath="./log/"

current=`date +%Y%m%d%H%M`
top -bn 1 > ${filepath}${current}

if [ ${current:8} == "1625" ]; then
#    ls -l ${filepath} | grep -vE `date +%Y%m%d`'|total|'`date +'%Y%m%d' -d '-1 days'` | awk '{print $9}' | xargs -i rm ${filepath}{}
    find ${filepath} -mtime +2 -type f -exec rm -Rf {} \;
fi
