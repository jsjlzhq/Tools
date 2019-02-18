import psutil, time
results = []
while True :
    for p in psutil.process_iter():
        try:
            cmdLine = p.cmdline()
            if (cmdLine[0].find("Secure") != -1 ) :
                item = [cmdLine[0], cmdLine[5], cmdLine[8], cmdLine[10], cmdLine[12], cmdLine[13]]
                #print(item)
                if len(results) == 0 :
                    results.append(item) 
                    print(",".join(item))
                else :
                    bFound = False
                    for i in results :
                        if item[1] == i[1] :
                            bFound = True
                            break
                    if not bFound :
                        results.append(item) 
                        print(",".join(item))
                time.sleep(2)
                p.kill()
        except Exception as e:
            pass
            #print(e)
    time.sleep(2)
