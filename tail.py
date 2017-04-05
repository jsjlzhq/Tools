#!/usr/bin/python
#coding:utf-8

import sys
import time
import thread

systype=sys.getfilesystemencoding()

def firstoutput(linenum, filename):
    f=open(filename, "r")
    lines = int(linenum)
    block_size = 1024
    block = ''
    n1_count = 0
    start = 0
    totalsize = 0
    f.seek(0, 2)
    curpos = f.tell()
    totalsize = curpos
    while curpos>0:
        curpos -= block_size
        if curpos<0:
            curpos=0
        f.seek(curpos, 0)
        block = f.read()
        n1_count = block.count('\n')
        if n1_count > lines:
            break
    for n in range(n1_count - lines +1):
        start = block.find('\n', start) +1
    print block[start:].decode('utf-8').encode(systype),
    f.close()
    return totalsize

def tail(filename, totalsize):
    f=open(filename, "r")
    f.seek(totalsize)
    while 1:
        line = f.readline()
        if not line:
            time.sleep(1)
            continue
        print line.decode('utf-8').encode(systype),

def tail_thread(linenum, filename):
    totalsize=firstoutput(linenum, filename)
    tail(filename, totalsize)

if __name__ == '__main__':
    linenum = sys.argv[1]
    filename = sys.argv[2]
    thread.start_new_thread(tail_thread, (linenum, filename))
    while 1:
        try:
            str_input=raw_input()
        except:
            break
