#!/usr/bin/python
# -*- coding: utf-8 -*-


class ReportInfo:
    def __init__(self):
        self.cashflow = None            # 销售商品、提供劳务收到的现金
        self.revenue = None             # 营业总收入
        self.roe = None                 # 净资产收益率
        self.cash_revenue_ratio = None  # 现金收入比

    def setCashFlow(self, cashflow):
        self.cashflow = cashflow
        self.updateRatio()

    def setRevenue(self, revenue):
        self.revenue = revenue
        self.updateRatio()

    def setRoe(self, roe):
        self.roe = roe

    def updateRatio(self):
        if self.revenue and self.cashflow and self.revenue != 0:
            self.cash_revenue_ratio = int(self.cashflow * 100 / self.revenue)

    def is_output(self):
        if not self.cash_revenue_ratio or self.cash_revenue_ratio > 100:
            return True
        if not self.roe or self.roe > 12:
            return True
        return False


class StockInfo:
    def __init__(self, id, symbol):
        self.id = id
        self.symbol = symbol
        self.reports = {}

    def get_report(self, name):
        if not self.reports.get(name):
            self.reports[name] = ReportInfo()
        return self.reports[name]

    def add_cashflow(self, name, cash):
        self.get_report(name).setCashFlow(cash)

    def add_revenue(self, name, revenue):
        self.get_report(name).setRevenue(revenue)

    def add_roe(self, name, roe):
        self.get_report(name).setRoe(roe)

    def is_output(self):
        for report in list(self.reports.values()):
            if report.is_output():
                return True
        return False
