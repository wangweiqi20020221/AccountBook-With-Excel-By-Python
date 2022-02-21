# AccountBook With Excel By Python
这是一个用python制作的多人账本程序，数据存储在excel表格中。

#### 设计初衷
当我们和别人一起去超市买东西时，有时并不能分开结账。比如我们去买吃火锅用的材料，然后拿到一个人的家里去吃，我们一起买了一份鱼丸，最后算帐的时候每个人应该出鱼丸1/3的钱。但是我还买了一些只有我自己吃的东西，这个东西不需要和其他两个人算钱。

这个程序是为更高效的解决这类问题而开发的。在使用这个程序时，我们设置“鱼丸”的购买者是我们三个人，程序就会自动把鱼丸的价格除以三，再算到我们个人的帐上。在输入账单以后，你可以很方便的用这个程序显示出每个人分别花了多少钱。


#### 使用方法
在当前版本中，你只能通过`import AcountBook`的方式来使用这些代码。由于我使用了pandas来读取excel及处理数据，所以你要确保你的python安装了pandas。使用`pip install pandas`来安装pandas。

在开始使用这个账本程序时，使用`account_book = AccountBook.AccountBook(file_name="file.xlsx", sheet=sheet_number)`来实例化AccountBook类。其中file.xlsx是你使用的账本excel表格的名字，sheet_number是你要读取的表，要读取第一张表就填0，第二张表就填1。

##### 添加账单
如果要为账本添加一个账单，要使用`account_book.register_receipt()`方法。这个方法需要的参数有：
- sheet_name:表的名字（而不是第几个表）
- date:账单的时间，类似"yyyy-mm-dd hh:mm:ss"
- owners_list:账单所有者的id列表。应当把所有在帐本中出现过的id都列入这个列表。
- location:购买地点。
- items_list:商品类目清单，列出了所有够买的商品。
- prices_list:价格清单，列出了这些商品对应的价格。
- purchasers_list:购买者清单，列出了这些商品对应的购买者id。若一个商品是多个人一起买的，则用‘&‘来分隔这些人的id。
- tax:税。如果你的账单没有额外的税，填写0即可。

示例：
```python
account_book.register_receipt(sheet_name="2022-02",
                               date="2022-02-04 14:53:00",
                               owners_list=[3],
                               location="天车站",
                               items_list=["公交卡充值"],
                               prices_list=[10],
                               purchasers_list=[3],
                               tax=0)
```

**注意**：tems_list、prices_list和purchasers_list三个列表的顺序应该是一样的。即三个列表相同的索引应该表示同一件商品。比如items_list[3]是牛肉，那么prices_list[3]是牛肉的价格，purchasers_list[3]是所有买牛肉的人的id。

在运行register_receipt方法后，程序会把新输入的账单保存在excel表格中。

##### 查询账单
使用`account_book.check_receipt(receipt_id=0)`可以列出某特定id的账单的商品清单、价格清单和购买者清单。

使用`account_book.get_receipt(content={"key": "value"})`可以查询某账单的id，支持模糊查询。其中key有如下值可用：
- 时间
- 所有者名单
- 地点
- 商品清单
- 价格清单
- 购买者清单
- 税

value是查询的key所对应的值。

示例：
```python
# 查询所有在盒马鲜生消费的账单。
account_book.get_receipt(content={"地点": "盒马鲜生"})

# 查询所有含有五花肉的账单
account_book.get_receipt(content={"商品清单": "五花肉"})
```

使用`account_book.check_amount(purchaser_id=3, receipt_id=0)`可以查询user_id为3的消费者在本账单中的支出。

#### 更新计划
在下个版本中，会更新一个叫做User的类，用于处理用户相关的操作，主要为对用户的增删改查。

在未来的版本中，会使用reportlab来生成pdf的账单文件。

(2022/2/20 16:48)