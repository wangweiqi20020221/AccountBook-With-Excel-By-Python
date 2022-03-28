import AccountBook


def add_account():
    print("请输入日期，yyyy-mm-dd hh:mm:ss：")
    date = input()
    print("输入所有与账本相关的人员id，用逗号分隔：")
    owners_list = input().split(",")
    for index in range(len(owners_list)):
        owners_list[index] = int(owners_list[index])
    print("请输入购买的地点：")
    location = input()
    items_list = []
    prices_list = []
    purchasers_list = []
    while True:
        print("输入商品名：")
        items_list.append(input())
        print("输入价格：")
        prices_list.append(float(input()))
        print("输入购买此商品的人的id，用&分隔：")
        purchasers_list.append(input().split("&"))
        print("如需停止请按1，按其他键继续：")
        if input() == "1":
            break
    print("请输入税：")
    tax = float(input())
    print(account_book.register_receipt(sheet_name="2022-2",
                                        date=date,
                                        owners_list=owners_list,
                                        location=location,
                                        items_list=items_list,
                                        prices_list=prices_list,
                                        purchasers_list=purchasers_list,
                                        tax=tax))


def check_amount():
    print("请输入账单id:")
    receipt_id = int(input())
    for purchaser in account_book.sheet["所有者名单"][receipt_id]:
        print(f"{purchaser}号购买者购买的金额为{account_book.check_amount(purchaser_id=purchaser, receipt_id=receipt_id)}")


account_book = AccountBook.AccountBook(file_name="Account Book.xlsx", sheet=0)
while True:
    print("功能列表")
    print("1: 添加账单")
    print("2: 查询某个账单每个人分别花了多少钱")
    print("0:退出")
    choice = int(input("请输入："))
    match choice:
        case 0:
            break
        case 1:
            add_account()
        case 2:
            check_amount()
