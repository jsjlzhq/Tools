#!/home/ouyang/local/bin/python
import subprocess, time, smtplib, sys
from qpid.messaging import Connection

sys.path.append("/home/ouyang/utils/qpid-tools")
from qpidtoollibs import BrokerAgent

def checkOverStockedQueues(host) :
    connection = Connection.establish(host)
    broker = BrokerAgent(connection)
    queues = broker.getAllQueues()
    result = list()
    for q in queues :
        if (q.msgDepth != 0) :
            print(q.name + " " + str(q.msgDepth))
            result.append([q.name, q.msgDepth])
    return result

def sendoutMail(results) :
    if len(results) == 0 :
        return
    fromAddress = "datafeeds.alert@sumscope.com"
#    toAddrList = ["yingxiu.ouyang@sumscope.com", "jianxin.du@sumscope.com","qing.fang@sumscope.com","xiaobo.hu@sumscope.com","hongbin.li@sumscope.com","yinfei.li@sumscope.com","lingyun.wang@sumscope.com","xiaoxing.wu@sumscope.com","xiaolong.zhang@sumscope.com","xin.zhou@sumscope.com","daniel.zhang@sumscope.com","xiaohua.zhu@sumscope.com", "binson.qian@sumscope.com"]
    toAddrList = ["yingxiu.ouyang@sumscope.com"]
    subject = "Duplicated queue detected "+ time.strftime("%Y-%m-%d %X", time.localtime())
    header = "Content-type: text;charset=GBK\n"          
    header  += 'From: %s\n' % fromAddress
    header += 'To: %s\n' % ','.join(toAddrList)
    header += 'Subject: %s\n\n' % subject
    
    message = "Duplicate queue with different mode will cause unexpected behavior on msgbus. Please clean these duplicated queues\n"
    for result in results :
        message += "host: " + result[0] + "\n"
        for i in result[1] :
            message += "\t" + i + "\n"
    message += "\nNotes: please use the following way to clean these duplicated queues" + "\n\n"
    message += "To delete a direct mode queue:\n"
    message += "\t" + "qpid-config --force del queue queueName" + "\n\n"
    message += "To delete a fanout mode queue:\n"
    message += "\t" + "qpid-config --force del exchange queueName\n"
    message = header + message
    
    smtpServer = "127.0.0.1"
    try :
        server = smtplib.SMTP(smtpServer, timeout = 20)
        problems = server.sendmail(fromAddress, toAddrList, message.encode(encoding="GBK", errors='strict'))
        server.quit()
        print("send mail successfully. " +  time.strftime("%Y-%m-%d %X", time.localtime()))   
    except  Exception as e    :
        print("send mail error " + str(e))
    
if __name__=="__main__" :
    bMailResult = False
    for a in sys.argv  :
        if a.find("-m") != -1 :
            bMailResult = True
            
 #   hosts = ["192.168.1.234", "192.168.1.238","172.16.8.85", "172.16.8.191", "172.16.8.196", "172.16.8.197", "172.16.16.43"]
    hosts = ["172.16.8.85", "172.16.8.196"]
    
    results = list()
    for h in hosts :
        result = checkOverStockedQueues(h)
        if len(result) != 0 :
            results.append([h, result])
            
    if len(results) == 0 :
        print("No overStocked queue detected")
    else :
        if bMailResult: 
            sendoutMail(results)
        else :
            print(results)
            
