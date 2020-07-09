'''
读取公司记账凭证xls总文件，并为每对借贷方生成单独xls文件供打印使用
'''

# 读取需要的库：xlwt用于写xls文件，csv用于读取表头并提取时间
import pandas as pd
import xlwt
import csv
import numpy as np


def LenderChecker(row):
    '''根据row判断此记录是否为借方，是则返回True'''
    if row['借方'] is not np.nan and row['贷方'] is np.nan:
        return True
    else:
        return False


def DateIdenticalChecker(series):
    '''比较series里的值是否相同，是则返回True'''
    a = series.to_numpy()
    return (a[0] == a).all()


class ExcelSheet:
    '''即将导出的Excel表格对象
        attributes:
        time: the sheet's time in string
        lenders: the list of Lender
        borrowers: the list of Borrower'''
    def __init__(self,index,time,lenders,borrowers):
        self.id = index
        self.time = time
        self.lenders = lenders
        self.borrows = borrowers
        self.sum_lend = 0
        self.sum_borrow = 0
        for x in lenders:
            self.sum_lend += x.money
        for x in borrowers:
            self.sum_borrow += x.money

    def to_xls(self):
        '''生成xls文件'''
        generated = xlwt.Workbook()
        ws = generated.add_sheet('凭证页')
        row = self.heading_format(ws)
        row = self.body_format(ws,row)
        self.ending_format(ws, row)
        generated.save(str(int(self.id)) + '.xls')
        print("{}号凭证已生成".format(self.id))

    def heading_format(self,ws):
        '''调整xls表头格式
        :argument
        ws: xlrd.sheet object
        :return row index to begin body writing
        '''
        ws.write_merge(0, 0, 0, 4, "记账凭证")
        ws.write_merge(1, 1, 0, 4, "日期:\t"+self.time)
        ws.write_merge(2, 3, 0, 0, "摘要")
        ws.write_merge(2, 2, 1, 2, "会计科目")
        ws.write_merge(2, 2, 3, 4, "金额")
        ws.write(3, 1, "一级科目")
        ws.write(3, 2, "二级科目")
        ws.write(3, 3, "借")
        ws.write(3, 4, "贷")
        return 4

    def body_format(self,ws,StartRowId):
        row = StartRowId
        for x in self.lenders:
            ws.write(row, 0, x.abs)
            ws.write(row, 1, x.cate1)
            if x.cate2 is not np.nan:
                ws.write(row, 2, x.cate2)
            ws.write(row, 3, x.money)
            row += 1
        for x in self.borrows:
            ws.write(row, 0, x.abs)
            ws.write(row, 1, x.cate1)
            if x.cate2 is not np.nan:
                ws.write(row, 2, x.cate2)
            ws.write(row, 4, x.money)
            row += 1
        return row

    def ending_format(self,ws,StartRowId):
        row = StartRowId
        ws.write(row, 2, "总计：")
        ws.write(row, 3, self.sum_lend)
        ws.write(row, 4, self.sum_borrow)



class Lender:
    '''借方对象'''
    def __init__(self,abstract,cate1,money,cate2=None):
        self.abs = abstract
        self.cate1 = cate1
        self.cate2 = cate2
        self.money = money


class Borrower:
    '''贷方对象'''
    def __init__(self,abstract,cate1,money,cate2=None):
        self.abs = abstract
        self.cate1 = cate1
        self.cate2 = cate2
        self.money = money


FileName = 'example.xls' # 总文件路径
overall = pd.read_excel(FileName, header=1,usecols=['序号','年','月','日','凭证摘要','借方','二级明细','金额','贷方','二级明细.1',
                                                    '金额.1'], sheet_name=0)  # 默认读取第一页工作表

MaxIndex = int(overall['序号'].max())

GroupByIndex = overall.groupby('序号')
for index, group in GroupByIndex:
    Borrowers = []
    Lenders = []
    for _,row in group.iterrows():
        if LenderChecker(row):
            Lenders.append(Lender(abstract=row['凭证摘要'],cate1=row['借方'],cate2=row['二级明细'],money=row['金额']))
        else:
            Borrowers.append(Borrower(abstract=row['凭证摘要'],cate1=row['贷方'],cate2=row['二级明细.1'],money=row['金额.1']))
    if DateIdenticalChecker(group['日']) and DateIdenticalChecker(group['月']) and DateIdenticalChecker(group['年']):
        TimeString = str(int(row['年']))+"年"+str(int(row["月"]))+"年"+str(int(row["日"]))+"日"
    else:
        print("警告：检测到序号{}的记录日期不相同，默认选择序号中第一行记录日期，请稍后手动修改".format(index))
    sum_borrow = 0
    for x in Borrowers:
        sum_borrow += x.money
    sum_lend = 0
    for x in Lenders:
        sum_lend += x.money
    if sum_lend != sum_borrow:
        print("警告：检测到序号{}的金额不匹配——借方金额={},贷方金额={}，请稍后检查手动修改".format(index,sum_lend,sum_borrow))
    ExcelSheet(index, TimeString, Lenders, Borrowers).to_xls()
print("程序完成100%")

