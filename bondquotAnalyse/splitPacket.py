#!/usr/local/anaconda3/bin/python

# JMS2QPID.FANOUT.FULL队列消息分包
# param1 输入文件名
# param2 输出文件名

import os
import sys
import re

if __name__=="__main__":
    f=open(sys.argv[1])
    fw = open(sys.argv[2],'w')

    stack = []
    maplinecount=-1
    
    stype = "[Type]"
    sBondOfferMessage="<MAP>[bondOfferMessage]"
    sBondDealMessage="<MAP>[bondDealMessage]"
    sBondMarketStream="<MAP>[bondMarketStreamMessage]"
    smethodAdd="<MAP>[methodAdd]"
    smethodUpdate="<MAP>[methodUpdate]"
    smethodDelete="<MAP>[methodDelete]"
    smethodRefer="<MAP>[methodRefer]"
    sbondOffer="<LIST>[bondOffer]"
    sbondDeal="<LIST>[bondDeal]"
    sMarketStream="<LIST>[marketStream]"
    pattern=re.compile("<MAP>\[\d")
    
    while 1:
        line=f.readline().strip()
        if line=='':
            break
        if line.find(stype)!=-1:
            del stack[:]
            stack.append(line)
            maplinecount=-1
        elif line.find(sBondOfferMessage)!=-1 or line.find(sBondDealMessage)!=-1 or line.find(sBondMarketStream)!=-1:
            if stack[-1].find(stype)==-1:
                del stack[1:]
            stack.append(line)
        elif line.find(smethodAdd)!=-1 or line.find(smethodUpdate)!=-1 or line.find(smethodDelete)!=-1 or line.find(smethodRefer)!=-1:
            del stack[2:]
            stack.append(line)
        elif line.find(sbondOffer)!=-1 or line.find(sbondDeal)!=-1 or line.find(sMarketStream)!=-1:
            stack.append(line)
        elif pattern.search(line)!=None:
            for stk in stack:
                fw.write(stk)
                fw.write('\n')
            fw.write(line)
            fw.write('\n')
            maplinecount=line.count('-')
        elif maplinecount>=0 and line.count('-',None,line.find('<'))>=maplinecount+2:
            fw.write(line)
            fw.write('\n')
