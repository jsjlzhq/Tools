#!/usr/local/anaconda3/bin/python

# BOND_OFFER_PUSH_V5 BOND_DEAL_PUSH_V5 队列消息分包
# param1 输入文件名
# param2 输出文件名

import os
import sys
import re

if __name__=="__main__":
    f=open(sys.argv[1])
    fw = open(sys.argv[2],'w')

    stack = []
    maplinecount = -1
    
    stype = "[Type]"
    sAckMsgBody="<MAP>[AckMsgBody]"
    sOUTCOME="<LIST>[IMQ_OUTCOME]"
    pattern=re.compile("<MAP>\[\d")

    while 1:
        line=f.readline().strip()
        if line=='':
            break
        if line.find(stype)!=-1:
            del stack[:]
            stack.append(line)
            maplinecount=-1
        elif line.find(sAckMsgBody)!=-1:
            if stack[-1].find(stype)==-1:
                del stack[1:]
            stack.append(line)
        elif line.find(sOUTCOME)!=-1:
            stack.append(line)
        elif pattern.search(line)!=None:
            for stk in stack:
                fw.write(stk)
                fw.write('\n')
            fw.write(line)
            fw.write('\n')
            maplinecount=line.count('-');
        elif maplinecount>=0 and line.count('-',None,line.find('<'))>=maplinecount+2:
            fw.write(line)
            fw.write('\n')
