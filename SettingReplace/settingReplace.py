#!/usr/bin/python
#coding:utf-8

import sys
import os

def param_config(paramfile, paramval):
    fparam=open(paramfile)
    while 1:
        line=fparam.readline().strip()
        if not line:
            break
        subidx=line.find(":")
        if subidx < 0:
            print "unknown param:",line
            continue
        title=line[0:subidx]
        vals=line[subidx+1:].strip()
        paramval[title]=vals

def replace_line(line, paramconfig):
    lbracket=line.find('{{')
    if lbracket<0:
        return line
    rbracket=line.find('}}',lbracket+2)
    if rbracket<0:
        return line
    pam=line[lbracket+2:rbracket].strip()
    if paramconfig.has_key(pam):
        org_str=line[lbracket:rbracket+2]
        dst_str=paramconfig.get(pam)
        line=line.replace(org_str, dst_str)
        return replace_line(line, paramconfig)
    else:
        print "has no key",pam
        return line



def setting_replace(infile, outfile, paramconfig):
    fin = open(infile, 'r')
    fout = open(outfile, 'w')
    while 1:
        line=fin.readline()
        if not line:
            break
        line=replace_line(line, paramconfig)
        fout.write(line)
    fin.close()
    fout.close()

if __name__=="__main__":
    infile=sys.argv[1]
    outfile=sys.argv[2]
    # 0-开发环境(默认) 1-测试环境 2-生产环境
    dev=0
    if len(sys.argv)>3:
        dev=int(sys.argv[3])
    if dev==0:
        filename="param_config_dev.txt"
    elif dev==1:
        filename="param_config_test.txt"
    else:
        filename="param_config_prd.txt"
    paramval={}
#    param_config(filename, paramval)
    pypath=os.path.split(os.path.realpath(__file__))[0]
    param_config(pypath+"/"+filename, paramval)
    setting_replace(infile, outfile, paramval)


