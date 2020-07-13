#!/bin/bash

url="https://sc.ftqq.com/SCU69199T10cf07dff058d8fc834c59e83834c1f05df86cecdf649.send"
logfile="nohup.log"

thisDir="$(cd `dirname "$0"` && pwd )"
cd $thisDir

sendToWechat(){
    curl -G -d 'text='$1 -d 'desp='$2 $url
}

rawurlencode() {
  local string="${1}"
  local strlen=${#string}
  local encoded=""
  local pos c o

  for (( pos=0 ; pos<strlen ; pos++ )); do
     c=${string:$pos:1}
     case "$c" in
        [-_.~a-zA-Z0-9] ) o="${c}" ;;
        * )               printf -v o '%%%02x' "'$c"
     esac
     encoded+="${o}"
  done
#  echo "${encoded}"    # You can either set a return variable (FASTER) 
  REPLY="${encoded}"   #+or echo the result (EASIER)... or both... :p
}

rawurldecode() {
  printf -v REPLY '%b' "${1//%/\\x}" # You can either set a return variable (FASTER)
  echo "${REPLY}"  #+or echo the result (EASIER)... or both... :p
}

dump=false
title='dm_news服务异常'
check_results=`ps aux | grep python3 | grep dm_news | wc -l`
if [[ $check_results != 1 ]]
then
    dump=true
    title="dm_news服务挂掉了"
fi

check_results=`grep -n Traceback $logfile`
if [[ $check_results =~ 'Traceback' ]]
then
    line_num=`echo $check_results | awk -F ':' '{print $1}'`
    err_desc=`tail -n +$line_num $logfile | sed -e 's/$/\r\n\r/'` #注意要达到换行效果需多加一个换行
    rawurlencode "$err_desc"
    sendToWechat $title ${REPLY}
else
    if [[ "$dump" = true ]]
    then
        sendToWechat $title "无异常日志"
    fi
fi


