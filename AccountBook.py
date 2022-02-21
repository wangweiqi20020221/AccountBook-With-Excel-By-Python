"""
作者：玮奇玮帝
作者网址：https://samweiqi.wang
github: wangweiqi20020221

"""

import pandas
import time
import logging


class AccountBook:
    def __init__(self, file_name="", sheet=0):
        """
        初始化账单，读取以及整理某一表格中的数据。
        一张表应该有以下这些数据：
            id: 从0开始递增的自然数列，不同于excel的列数，这个是程序中每个账单的列数；
            date: 购买时间；
            location: 购买地点；
            items_list: 商品清单列表；
            prices_list: 价格清单列表；
            purchasers_list: 购买者列表；
            tax: 税，在一些国家的税是单独算的。
        其中，items_list、prices_list核purchasers_list三个列表的索引是一样的。
        :param file_name: 要读取的excel文件名；
        :param sheet: 要读取的第几张表，从0开始计数。
        """
        # 初始化日志
        self.log_name = "./logs/" + str(time.strftime("%Y-%m-%d")) + ".log"
        logging.basicConfig(filename=self.log_name,
                            level=logging.DEBUG,
                            format="%(asctime)s (%(levelname)s) - %(name)s - %(message)s")
        logging.info("日志初始化完成")
        self.file_name = file_name
        # 读取数据
        self.sheet = pandas.read_excel(io=self.file_name, sheet_name=sheet)
        for index in range(len(self.sheet["商品清单"])):
            self.sheet["所有者名单"][index] = str(self.sheet["所有者名单"][index]).split(",")
            self.sheet["商品清单"][index] = str(self.sheet["商品清单"][index]).split(",")
            self.sheet["价格清单"][index] = str(self.sheet["价格清单"][index]).split(",")
            self.sheet["购买者清单"][index] = str(self.sheet["购买者清单"][index]).split(",")
            for index2 in range(len(self.sheet["商品清单"][index])):
                self.sheet["价格清单"][index][index2] = float(self.sheet["价格清单"][index][index2])
                self.sheet["购买者清单"][index][index2] = str(self.sheet["购买者清单"][index][index2]).split("&")
        logging.info("excel文件加载完毕")

    def check_amount(self, purchaser_id=0, receipt_id=0):
        """
        查询某账单中某个人的消费金额。
        :param purchaser_id:查询一个账本中某个人买的金额。
        :param receipt_id:要查询的账本id。
        :return:{"member_id": amount}
        """
        receipt = self.sheet.loc[receipt_id]
        total = 0
        for index in range(len(receipt["商品清单"])):
            if str(purchaser_id) in receipt["购买者清单"][index]:
                total += receipt["价格清单"][index] / len(receipt["购买者清单"][index])
        return total

    def check_receipt(self, receipt_id):
        """
        列出某个账单里所有的商品名和对应的价格。
        :param receipt_id:账单的id。
        :return:一个形如[{"item": item, "price": price, "purchasers": purchasers}]的列表
        """
        """
        for index in range(len(self.sheetContent[receipt_id]["items_list"])):
            receipt.append({
                "item": self.sheetContent[receipt_id]["items_list"][index],
                "price": self.sheetContent[receipt_id]["prices_list"][index],
                "purchasers": self.sheetContent[receipt_id]["purchasers_list"][index]
            })
        """
        logging.info(f"id为{receipt_id}的账单被查询")
        return self.sheet[self.sheet["id"] == receipt_id]

    def get_receipt(self, content={}):
        """
        查询符合条件的账单，传入的数据为字典，其键是要查询的字段，其值是字段对应的值。支持模糊查询。
        比如要查询item中含有“肉”字的账单的id，content就填{"item": "肉"}
        :param content:
        :return:所有符合结果的账单，数据类型为dataFrame。
        """
        key = list(content.keys())[0]
        value = list(content.values())[0]
        return self.sheet[self.sheet[key].str.contains(value)]

    def register_receipt(self, sheet_name="", date="", owners_list=[], location="", items_list=[], prices_list=[], purchasers_list=[], tax=0):
        """
        创建一个新的账单。
        :param sheet_name:表的名字（而不是第几个表）
        :param date:账单的时间，类似"yyyy-mm-dd hh:mm:ss"
        :param owners_list:账单所有者的id列表。应当把所有在帐本中出现过的id都列入这个列表。
        :param location:购买地点。
        :param items_list:商品类目清单，列出了所有够买的商品。
        :param prices_list:价格清单，列出了这些商品对应的价格。
        :param purchasers_list:购买者清单，列出了这些商品对应的购买者id。若一个商品是多个人一起买的，则用‘&‘来分隔这些人的id。
        :param tax:税。如果你的账单没有额外的税，填写0即可。
        :return:0
        """
        self.sheet = self.sheet.append(pandas.Series([date,
                                                      owners_list,
                                                      location,
                                                      items_list,
                                                      prices_list,
                                                      purchasers_list,
                                                      tax],
                                                     index=["时间", "所有者名单", "地点", "商品清单", "价格清单", "购买者清单", "税"]),
                                       ignore_index=True)
        logging.info("向账单添加了信息：")
        logging.info(f"date={date}, owners_list={owners_list}, location={location}, tax={tax}")
        logging.info(f"items_list={items_list}")
        logging.info(f"prices_list={prices_list}")
        logging.info(f"purchasers_list={purchasers_list}")
        self._save_to_excel(sheet_name=sheet_name)
        return 0

    def _save_to_excel(self, sheet_name):
        """
        保存数据到excel。
        :return:Data saved
        """
        def list_to_str(origin_list):
            """
            把列表转换成字符串，用英文的“,”分隔
            :param origin_list:需要转换的列表
            :return:转换好的字符串
            """
            string = ""
            for item in origin_list:
                string += str(item)
                string += ","
            # 去除最后一位多余的逗号
            string = string[:-1]
            return string

        sheet_for_saved = self.sheet
        for index in range(len(sheet_for_saved["商品清单"])):
            sheet_for_saved["所有者名单"][index] = list_to_str(sheet_for_saved["所有者名单"][index])
            sheet_for_saved["商品清单"][index] = list_to_str(sheet_for_saved["商品清单"][index])
            sheet_for_saved["价格清单"][index] = list_to_str(sheet_for_saved["价格清单"][index])
            sheet_for_saved["购买者清单"][index] = list_to_str(sheet_for_saved["购买者清单"][index])
        sheet_for_saved.to_excel(self.file_name, sheet_name=sheet_name, index=False)
        logging.warning("账本文件被保存")
        return "Data saved."


account_book = AccountBook(file_name="Account Book.xlsx", sheet=0)
# account_book.check_amount(purchaser_id=3, receipt_id=0)
# account_book.register_receipt(sheet_name="2022-02",
#                               date="2022-02-04 14:53:00",
#                               owners_list=[3],
#                               location="天车站",
#                               items_list=["公交卡充值"],
#                               prices_list=[10],
#                               purchasers_list=[3],
#                               tax=0)
# print(account_book.check_receipt(receipt_id=0))
# print(account_book.get_receipt(content={"地点": "天车站"}))