#!/usr/local/anaconda3/bin/python
# encoding: UTF-8

from pprint import pprint
import time

import openpyxl
import copy

class QuotInfo:
    "报价详细信息"

    # time[0] / unixTime[1] / goodCodes[2] / method[3] / id[4] / createTime[5] / netPrice[6] / orgNetPrice[7] /
    # yield[8] / orgYied[9] / price[10] / orgPrice[11] / dealStatus[12] / status[13] / internally[14] / symbol[15] / volume[16] / priceDescription[17]
    def __init__(self, result):
        (self.time, self.unixTime, self.goodCodes, self.method, self.id, self.createTime, self.netPrice,
         self.orgNetPrice, self.yyield, self.orgYied, self.price, self.orgPrice, self.dealStatus, self.status,
         self.internally, self.symbol, self.volume, self.priceDescription) = result

    def toArray(self):
        arr = [self.time, self.unixTime, self.goodCodes, self.method, self.id, self.createTime, self.netPrice,
         self.orgNetPrice, self.yyield, self.orgYied, self.price, self.orgPrice, self.dealStatus, self.status,
         self.internally, self.symbol, self.volume, self.priceDescription]
        return arr

    def isDelete(self):
        if self.method == "methodDelete":
            return True
        if self.dealStatus == "2":
            return True
        if self.status != "1":
            return True
        if self.internally == "2":
            return True
        return False

    def isBid(self):
        return self.symbol=="1"

    def calcBest(self, obj):
        if len(self.price)==0:
            return obj
        elif len(obj.price)==0:
            return self

        try:
            price1 = float(self.price)
            price2 = float(obj.price)
        except ValueError:
            print("invalid price")
            pprint(vars(self))
            pprint(vars(obj))

        if (price1>price2 and self.symbol=="1") or (price1<price2 and self.symbol=="-1"):
            return obj
        elif self.price == obj.price and obj.volume!="0":
            bestquot = copy.deepcopy(self)
            bestquot.volume = obj.volume + "+" + self.volume
            return bestquot
        return self

def calcBest(qi, quotes):
    if qi.id in quotes:
        quotes.pop(qi.id)  # 将之前存在的id删除
    if not qi.isDelete():
        quotes[qi.id] = qi  # 加入新的id

    if len(quotes)==0:
        print(qi.toArray())
        return qi

    quotesval=list(quotes.values())
    bestquot=copy.deepcopy(quotesval[-1])
    for idx in range(len(quotesval)-2, -1, -1):
        bestquot = bestquot.calcBest(quotesval[idx])

    if bestquot.id != qi.id:
        bestquot.time = qi.time
        bestquot.unixtime = qi.time
    print(bestquot.toArray())
    return bestquot

def writeResults(results, params):
    if len(results) == 0:
        print("no results")
        return
    heads = ["time", "unixTime", "goodCodes", "method"]
    heads.extend(params)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(heads)
    fileName = "result-bestprice-" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"
    for result in results:
        ws.append(result.toArray())
    wb.save(fileName)

def calcBestPrice(results, params):
    if len(results) == 0:
        print("no results to calc")
        return

    bidQuotes = {}
    ofrQuotes = {}
    bestquotes=[]
    for result in results:
        qi = QuotInfo(result)
        if qi.isBid():
            bestquotes.append(calcBest(qi, bidQuotes))
        else:
            bestquotes.append(calcBest(qi, ofrQuotes))
    writeResults(bestquotes, params)








