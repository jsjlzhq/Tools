import sys

def extractMsg(i, lines, strStart, strCmpyId, messages):
    msg = []
    msg.append(lines[i])
    i += 1
    bMatch = False
    while i<len(lines) :
        if lines[i].find(strStart) == -1 :
            if lines[i].find(strCmpyId) != -1 :
                bMatch = True
            msg.append(lines[i])
        else :
            if bMatch :
                messages.append(msg)
            break
        i += 1
        
    bRet = True if i>=len(lines)-1 else False
    if bRet and len(msg) != 0 and bMatch:
        messages.append(msg)
    
    return bRet, i

def extractMsgs(fileName, companyId, results) :
    with open(fileName, encoding = "UTF-8") as f:
        lines = f.readlines()

    strCmpyId = "<STR>[companyId](%s)" %(companyId)
    strStart = "[Type]()"
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
       done, i = extractMsg(i, lines, strStart, strCmpyId, results)

if __name__ == "__main__" :
    if len(sys.argv) != 3 :
        print("usage: splitByCompanyId file companyId")
        exit(0)
    
    fileName = sys.argv[1]
    companyId = sys.argv[2]
#    with open(fileName, encoding = "UTF-8") as f:
#        lines = f.readlines()
    results = []
    extractMsgs(fileName, companyId, results)
    print("total messages: " + str(len(results)))
    
    if len(results) == 0 :
        exit(0)
        
    outFile = fileName + "_" + str(companyId)
    with open(outFile, "w") as f2 :
        for result in results :
            for i in result :
                f2.write(i)
