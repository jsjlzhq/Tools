#encoding: UTF-8
import sys

#分割bond_deal_push/bond_offer_push 为不同的companyId


def extractMsg(i, lines, strStart, strCmpyId, goodsCode, results):
    msg = []
    msg.append(lines[i])
    i += 1
    bMatch = False
    bCompanyIdMatch = False
    bGoodsCodeMatch = False
    while i<len(lines) :
        if lines[i].find(strStart) == -1 :
            if lines[i].find(strCmpyId) != -1 :
                bCompanyIdMatch = True
            elif lines[i].find(goodsCode) != -1 :
                bGoodsCodeMatch = True
            bMatch = bCompanyIdMatch and bGoodsCodeMatch
            msg.append(lines[i])
        else :
            if bMatch :
                results.append(msg)
            break
        i += 1
        
    bRet = True if i>=len(lines)-1 else False
    if bRet and len(msg) != 0 and bMatch:
        results.append(msg)
    
    return bRet, i

def extractMsgs(lines, type_, companyId, goodsCode, results) :
#    strCmpyId = "<STR>[cid](%s)" %(companyId)
    if type_.lower() == "ms" :
        strCmpyId = "<STR>[MS_COMPANY_ID](%s)" %(companyId)   
        strGoodsCode = "<STR>[MS_GOODS_CODE](%s)" %(goodsCode)
    elif type_.lower() == "offer" :
        strCmpyId = "<STR>[cid](%s)" %(companyId)   
        strGoodsCode = "<STR>[gc](%s)" %(goodsCode)
        
    strStart = "[Type]"
    i = 0
    while i<len(lines):
        if lines[i].find(strStart) != -1 :
            break
        else:
            i += 1
    
    done = False
    if i>=len(lines) :
        done = True

    while  not done :
       done, i = extractMsg(i, lines, strStart, strCmpyId, strGoodsCode, results)

if __name__ == "__main__" :
    if len(sys.argv) != 5 :
        print("usage: splitPushByCid file ms/offer companyId goodsCode")
        exit(0)
    
    fileName = sys.argv[1]
    type_ = sys.argv[2]
    companyId = sys.argv[3]
    goodsCode = sys.argv[4]
    with open(fileName, encoding = "UTF-8") as f:
        lines = f.readlines()
    results = []
    extractMsgs(lines, type_, companyId, goodsCode, results)
    print("total messages: " + str(len(results)))
    
    if len(results) == 0 :
        exit(0)
        
    outFile = fileName + "_" + str(companyId)
    print(fileName)
    with open(outFile, "w") as f2 :
        for result in results :
            for i in result :
                f2.write(i)
