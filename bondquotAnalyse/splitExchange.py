#!/usr/local/anaconda3/bin/python

# 队列消息分包
# param1 输入文件名
# param2 输出文件名

import os
import sys
import re

if __name__ == "__main__":
    f=open(sys.argv[1])
    fw = open(sys.argv[2], 'w')

    stack = []
    maplinecount = -1
    packet=""

    stype = "[Type]"
    sLIST = "<LIST>[List]"
    sCode = "[Code](600030)"
    pattern = re.compile("<MAP>\[\d")

    done = 0
    while 1:
        line=f.readline().strip()
        if line=='':
            break
        if line.find(stype) != -1:
            del stack[:]
            stack.append(line)
            maplinecount = -1
        elif line.find(sLIST) != -1:
            stack.append(line)
        elif pattern.search(line) != None:
            if packet.find(sCode) != -1:
                fw.write(packet)
            packet = ""
            for stk in stack:
                packet+=stk+"\n"
            packet+=line+"\n"
            maplinecount = line.count('-');
        elif maplinecount >= 0 and line.count('-', None, line.find('<')) >= maplinecount + 2:
            packet+=line+"\n"

    if packet.find(sCode) != -1:
        fw.write(packet)
        packet=""





