# encoding: UTF-8
#!/usr/local/anaconda3/bin/python

# 前提输入的文件已经是JMS2QPID.FANOUT.FULL 按照broker 分好
#python filterCompanyFullPacket.py 20170112-full_4 offer 136692.SH id createTime netPrice orgNetPrice yield orgYied price orgPrice dealStatus status internally symbol priceDescription
#python filterCompanyFullPacket.py 20170227_4 deal 111693042 id createTime status dealStatus internally price netPrice fullPrice
# para1 文件名
# para2 offer/deal
# para3 goodsCode
# para4 之后为过滤输出的字段

import sys
import re, time

import openpyxl

class Message :
    def __init__(self, type_, method):
        self.type = type_
        self.method = method
        self.lines = []
        self.goodsCode = ""
        
def extraceValue(line):
    pos1 = line.find("(")
    pos2 = line.find(")")
    return line[pos1+1:pos2]

def extractMapTag(line):
    toFind = "<MAP>["
    pos = line.find(toFind)
#    pos2=  len(line)-1;
    return line[pos+len(toFind) : -1]

def extractValueTag(line): 
    pos1 = line.rfind("[")
    pos2 = line.rfind("]")
    return line[pos1+1 : pos2]

def splitMessageFile(fileName)  :
    with open(fileName) as f:
        product = f.read()
    jmsqpidlines=product.strip().splitlines()
    splitMessages(jmsqpidlines)
        
def splitMessages(jmsqpidlines):
    stack = []
    maplinecount=-1
    messages = []
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
    for line in jmsqpidlines:
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
            m = Message(extractMapTag(stack[1]),extractMapTag(stack[2]))
            for stk in stack:
                m.lines.append(stk)
            m.lines.append(line)
            maplinecount=line.count('-')
            messages.append(m)
        elif maplinecount>=0 and line.count('-',None,line.find('<'))>=maplinecount+2:
            m = messages[-1]
            m.lines.append(line)
            if line.find("goodsCode") != -1:
                m.goodsCode = extraceValue(line)
    
    return messages

def extractTime(line, orgTime) :
    #[18:18:24.862]--------<STR>[createTime](1484216301000)
    timeValue = line[1:9]
    import time
    dt = time.strftime("%Y-%m-%d", time.localtime(int(orgTime)))
    strTime = dt + " " + timeValue
    t = time.strptime(strTime, "%Y-%m-%d %X") 
    unixTime = time.mktime(t)   
    
    return timeValue, str(int(unixTime))

def extractMessage(msg, params):
    valueMap = {}
    timeValue = " "
    unixTimeValue = " "
    for line in msg.lines :
        valueTag = extractValueTag(line)
        if valueTag == "createTime":
            value = extraceValue(line)
            value = value[:-3]
            timeValue, unixTimeValue = extractTime(line, value)
            
        if valueTag in params :
            value = extraceValue(line)
            valueMap[valueTag] = value
    
    ret = []
    if len(valueMap) != 0 :
        ret.append(timeValue)
        ret.append(unixTimeValue)
        for param in params :
            if param in valueMap :
                ret.append(valueMap[param])
            else :
                ret.append(" ")
            
    return ret    

def filterMessages(messages, goodsCode, type_, params):
    results =[]

    for msg in messages :
        if msg.goodsCode == goodsCode and msg.type == type_ :
            lineResult = extractMessage(msg, params)
            if len(lineResult) != 0 :
                lineResult.insert(2, msg.method)
                lineResult.insert(2, msg.goodsCode)
                results.append(lineResult)
                
    return results

def writeResults(results, params) :
    if len(results) == 0:
        print("no results")
    else :
        heads = ["time", "unixTime", "goodCodes", "method"]
        heads.extend(params)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(heads)        
        print(",".join(heads))
        fileName = "result-" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"
        for result in results :
            print(",".join(result))
            ws.append(result)
        wb.save(fileName)

if __name__=="__main__":
    #python splitPacket.py 20170112-full_4 offer 136692.SH id createTime netPrice orgNetPrice yield orgYied price orgPrice dealStatus status internally symbol priceDescription
    fileName = sys.argv[1]
    messages = splitMessages(fileName)
    type_ = sys.argv[2]
    if type_.lower() == "offer" :
        type_ = "bondOfferMessage"
        params = ["id", "createTime", "netPrice", "orgNetPrice", "yield", "orgYied", "price", "orgPrice", "dealStatus", "status", "internally", "symbol", "volume","priceDescription"]
    elif type_.lower() == "deal" :
        params = ["id", "createTime", "status", "dealStatus", "internally", "price", "netPrice", "fullPrice"]
        type_ = "bondDealMessage"
      
    goodCode = sys.argv[3]
#    params = sys.argv[4:]
    results = filterMessages(messages, goodCode, type_, params)
    writeResults(results, params)
    

        

       
    
    

            

        
        
            
        
    
