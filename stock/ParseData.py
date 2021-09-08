#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import openpyxl
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from CommonRequest import *

market_price_url = "https://market2.cnfic.com.cn/quote/v1/real?en_prod_code={}&fields=last_px"


class Stock:
    def __init__(self, id, symbol):
        self.id = id
        self.symbol = symbol
        self.price = 0
        self.cash_ratios = []
        self.roes = []

    def addCashRatio(self, ratio):
        if not ratio:
            return
        self.cash_ratios.append(ratio)

    def addRoe(self, roe):
        if not roe:
            return
        self.roes.append(roe)

    def setPrice(self, price):
        self.price = price

    def cashRatioFilter(self):
        for ratio in self.cash_ratios:
            if ratio == "--":
                continue
            val = float(ratio)
            if val < 90:
                return False
        return True

    def last_cash_ratio_filter(self):
        last_cash_ratio = self.cash_ratios[0]
        if last_cash_ratio == "--":
            return False
        val = float(last_cash_ratio)
        if val < 80:
            return False
        return True

    def RoeFilter(self):
        for roe in self.roes:
            if roe == "--":
                continue
            val = float(roe)
            if val < 15:
                return False
        return True

    def last_roe_filter(self):
        last_roe = self.roes[0]
        if last_roe == "--":
            return False
        val = float(last_roe)
        if val < 15:
            return False
        return True


if __name__ == "__main__":
    filename = sys.argv[1]
    wb = openpyxl.load_workbook(filename)
    for sheet in wb:
        if len(list(sheet.rows)) == 0:
            continue
        print(sheet.title)

        for row in list(sheet.rows)[2:]:
            code = row[0].value
            stk = Stock(code, row[1].value)
            start = 2
            step = 4
            while start < len(row):
                stk.addCashRatio(row[start + 2].value)
                stk.addRoe(row[start + 3].value)
                start += step

            if not stk.last_cash_ratio_filter():
                continue
            if not stk.last_roe_filter():
                continue

            full_code = stk.id + "." + sheet.title
            price_json = CommonRequest().get_data(market_price_url.format(full_code)).json()
            try:
                prs = price_json["data"]["snapshot"][full_code][2]
                if prs <= 30:
                    continue
                stk.setPrice(prs)
            except:
                print("request error.{} {}".format(full_code, price_json))
            print(stk.__dict__)

