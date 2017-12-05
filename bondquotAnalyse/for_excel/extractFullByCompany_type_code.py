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
        
if __name__=="__main__":
    if len(sys.argv) != 5 :
        print("usage: \n\tpython extractFullByCompany_type_code.py fileName companyId, offer/deal goodsCode")
        exit(0)
        
    from splitByCompanyId import extractMsgs
    from filterCompanyFullPacket import filterMessages, writeResults, splitMessages
    from bestPriceCalc import calcBestPrice
 #   python extractFullByCompany_type_code.py fileName companyId, offer/deal goodsCode
    #python splitPacket.py 20170112-full_4 offer 136692.SH id createTime netPrice orgNetPrice yield orgYied price orgPrice dealStatus status internally symbol priceDescription
    fileName = sys.argv[1]
    companyId = sys.argv[2]
    type_ = sys.argv[3]
    if type_.lower() == "offer" :
        type_ = "bondOfferMessage"
        params = ["id", "createTime", "netPrice", "orgNetPrice", "yield", "orgYied", "price", "orgPrice", "dealStatus", "status", "internally", "symbol", "volume", "priceDescription"]
    elif type_.lower() == "deal" :
        params = ["id", "createTime", "status", "dealStatus", "internally", "price", "netPrice", "fullPrice"]
        type_ = "bondDealMessage"
    goodCode = sys.argv[4]
    messages = []
    extractMsgs(fileName, companyId, messages)
    print(len(messages))
    lines = []
    
    for m in messages :
        for line in m:
            lines.append(line.strip())
            
    messages = splitMessages(lines)    
    results = filterMessages(messages, goodCode, type_, params)

    writeResults(results, params)

    if type_ == "bondOfferMessage":
        calcBestPrice(results, params)
        

       
    
    

            

        
        
            
        
    
