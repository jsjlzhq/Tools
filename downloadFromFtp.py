from ftplib import FTP
from datetime import *
import os
import glob
import shutil

host='172.16.16.36'
downloadDir='V3.1'
destDir='d:\\testData\\'
#serverip='180.153.248.154'
#serverip='172.16.8.89'
serverip='172.16.8.85'

desttime=datetime.min
destname=''

def delFiles(pattern):
    for filename in glob.iglob(pattern):
        os.remove(filename)

def delDir(pattern):
    for dirname in glob.iglob(pattern):
        shutil.rmtree(dirname,True)

def lineAnalyse(line):
    global desttime
    global destname
    line.lstrip().rstrip()
    info = line.split()
    if len(info)<3:
        return
    filename = info[len(info)-1]
    filetime=line[0:17]
    dt = datetime.strptime(filetime, '%m-%d-%y  %I:%M%p')
    if dt>desttime:
        destname=filename
        desttime=dt
    return

def download():    
    f=FTP(host)
    f.login('','')
    f.cwd(downloadDir)

    f.retrlines('LIST',lineAnalyse)
        
    if len(destname)==0:
        f.quit()
        return
    
    if os.path.exists(destname):
        print 'has been the lastest file "%s"' % destname
        f.quit()
        return
    
    delFiles('Quoteboard_*.rar')
    delDir('Quoteboard_*')
    
    f.retrbinary('RETR %s' % destname, open(destname,'wb').write)

    print '*** Download "%s" finished' % destname

    f.quit()
    return
    
def unrar():
    dirname=destDir+destname[:-4]
    if os.path.exists(dirname):
        print 'has unrar ',destname
        return
#        shutil.rmtree(dirname,True)
    cmd='unrar x -r -ad '+destDir+destname+' '+destDir
    os.system(cmd)
    print destname,' unrar finished'

def changeServer():
    serverFile=destDir+destname[:-4]+'\\config\\ServerConfig.xml'
    formator='''<?xml version="1.0" encoding="gb2312" ?>
<root>
    <Server Index="0">
    	<Address>%s</Address>
    	<Name>server85</Name>
    	<Port>28899</Port>
    </Server>
    <Server Index="1">
    	<Address>%s</Address>
    	<Name>Server2</Name>
    	<Port>28899</Port>
    </Server>
</root>'''
    content=formator % (serverip,serverip)
    f=open(serverFile,'w')
    f.write(content)
    print 'serverConfig:',content
    f.close()
    

if __name__ == '__main__':
    cwd=os.getcwd()
    os.chdir(destDir)
    download()
    unrar()
    changeServer()
    os.chdir(cwd)
    os.system('pause')
