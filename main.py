# -*- coding:utf-8 -*-
from tkinter import *
import random
import time
import pymysql
import hashlib

def 加盐加密(data,secret):
    hash = hashlib.md5(data.encode('utf-8'))
    hash.update(secret.encode("utf-8"))
    return hash.hexdigest()


def 哈希_64位加密算法(user_id, secret_key):
    # 用于生成防伪认证码的字符串
    data = str(user_id) + str(secret_key) + str(int(time.time()))
    random_suffix = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))
    data += random_suffix

    # 使用sha256算法生成防伪认证码
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    authentication_code = 加盐加密(sha256.hexdigest(), secret_key) + 加盐加密(sha256.hexdigest(), user_id)

    # 返回64位哈希值
    return authentication_code


# 清空 登录界面输入框内容
def 清空账号密码输入框():
    # 清空 登录界面输入账号内容
    entry1.delete(0, "end")
    # 清空 登录界面输入密码内容
    entry2.delete(0, "end")


def 登录():
    def 生成():
        def 生成防伪标签():
            # 调用哈希算法
            authentication_code = 哈希_64位加密算法(账号, 密码)

            # 更新数据库
            host = "localhost"
            port = 3306  # 端口名称
            user = "root"
            password = "123456"
            db = "my"  # 数据库名称
            charset = "utf8"

            # 创建数据库连接对象，并建立连接
            db = pymysql.Connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
            # 打印数据库是不是正常连接
            print("数据库已连接.....")

            # 创建游标对象(1.执行sql语句，2.处理数据查询结果)
            cursor = db.cursor()
            # 编写sql
            sql = f"UPDATE data set 密钥='{authentication_code}' WHERE id='{账号}'"

            # 执行sql
            cursor.execute(sql)

            # 提交
            db.commit()

            # 关闭
            cursor.close()
            db.close()

            # 更新输出框
            # 删除数据
            text22.delete("1.0", "end")
            # 显示密钥
            text22.insert(END, authentication_code)

        def 生成清空():
            # 清空 登录界面输入账号内容
            text22.delete("1.0", "end")

        # 创建生成界面窗口
        生成界面 = Toplevel()

        # 登录窗口大小宽*高
        生成界面.geometry('900x300+400+0')

        # 设置窗口名称
        生成界面.title(f'防伪码生成')

        # 生成标签
        Navigation22 = Label(生成界面,  # 便签放在主界面界面
                             # 设置标签内容区大小
                             width=20,
                             height=20,
                             # 设置填充区距离、边框宽度和其样式
                             padx=0,
                             pady=0,
                             borderwidth=1,
                             relief="groove"
                             )
        Navigation22.place(x=0,
                           y=0,
                           width=900,
                           height=300)  # 标签的右上角坐标和宽高

        # 文本标签
        labe22 = Label(Navigation22,
                       text="生成防伪便签："
                       )
        labe22.place(x=100, y=100)

        # 文本框
        text22 = Text(Navigation22,
                      width=100,
                      height=1
                      )
        text22.place(x=100,
                     y=145
                     )

        # 创建按钮
        butto22_1 = Button(Navigation22,
                           text="清空",
                           width=10,
                           command=生成清空
                           )
        butto22_1.place(x=300,
                        y=200
                        )

        # 创建按钮
        butto22_2 = Button(Navigation22,
                           text="确认",
                           width=10,
                           command=生成防伪标签
                           )
        butto22_2.place(x=500,
                        y=200
                        )

        # 显示窗口
        主界面.mainloop()

        pass

    def 查询():
        def 查询防伪便签():
            # 创建一个数据库，再连接
            host = "localhost"
            port = 3306  # 端口名称
            user = "root"
            password = "123456"
            db = "my"  # 数据库名称
            charset = "utf8"

            # 创建数据库连接对象，并建立连接
            db = pymysql.Connect(host=host,
                                 port=port,
                                 user=user,
                                 passwd=password,
                                 db=db,
                                 charset=charset
                                 )
            # 打印数据库是不是正常连接
            print("数据库已连接.....")

            # 创建游标对象(1.执行sql语句，2.处理数据查询结果)
            cursor = db.cursor()

            # 编写sql
            sql = "SELECT * FROM data;"

            # 执行sql
            cursor.execute(sql)

            # 获取多行数据
            data = cursor.fetchall()

            # 打印数据库
            # print(data)

            # 关闭
            cursor.close()
            db.close()

            # 获得用户对应的数据库密钥
            密钥 = ""
            for i in data:
                if i[0] == 账号:
                    密钥 = i[3]
                    break

            # 打印密钥
            # print([密钥])

            # 打印密钥长度
            # print(len(密钥))

            # 打印查询的密钥
            查询的密钥 = str(text23_1.get("1.0", "end")).replace("\n", "")

            # 打印查询的密钥
            # print([text23_1.get("1.0", "end")])

            # 对比密钥
            if len(密钥) != 64:
                # 更新输出框
                # 删除数据
                text23_2.delete("1.0",
                                "end"
                                )
                # 显示密钥
                text23_2.insert(END,
                                "数据库无密钥，请先生成"
                                )

            elif len(查询的密钥) != 64:
                # 更新输出框
                # 删除数据
                text23_2.delete("1.0",
                                "end"
                                )
                # 显示密钥
                text23_2.insert(END,
                                "输入的密钥长度错误！"
                                )

            elif 密钥 == 查询的密钥:
                # 更新输出框
                # 删除数据
                text23_2.delete("1.0",
                                "end"
                                )
                # 显示密钥
                text23_2.insert(END,
                                "真防伪标签"
                                )

            else:
                # 更新输出框
                # 删除数据
                text23_2.delete("1.0",
                                "end"
                                )
                # 显示密钥
                text23_2.insert(END,
                                "假防伪标签"
                                )

        def 查询清空():
            # 清空 登录界面输入账号内容
            text23_1.delete("1.0",
                            "end"
                            )
            # 清空 登录界面输入账号内容
            text23_2.delete("1.0",
                            "end"
                            )

        # 创建生成界面窗口
        查询界面 = Toplevel()

        # 登录窗口大小宽*高
        查询界面.geometry('900x300+400+400')

        # 设置窗口名称
        查询界面.title(f'防伪码查询')

        # 查询标签
        Navigation23 = Label(查询界面,  # 便签放在主界面界面
                             # 设置标签内容区大小
                             width=20,
                             height=20,
                             # 设置填充区距离、边框宽度和其样式
                             padx=0,
                             pady=0,
                             borderwidth=1,
                             relief="groove"
                             )
        Navigation23.place(x=0,
                           y=0,
                           width=900,
                           height=300
                           )  # 标签的右上角坐标和宽高

        # 文本标签
        labe23_1 = Label(Navigation23,
                         text="查询防伪便签："
                         )
        labe23_1.place(x=100,
                       y=50
                       )

        # 文本框
        text23_1 = Text(Navigation23,
                        width=100,
                        height=1
                        )
        text23_1.place(x=100,
                       y=80
                       )

        # 文本标签
        labe23_2 = Label(Navigation23,
                         text="查询结果："
                         )
        labe23_2.place(x=100,
                       y=110
                       )

        # 文本框
        text23_2 = Text(Navigation23,
                        width=100,
                        height=1
                        )
        text23_2.place(x=100,
                       y=140
                       )

        # 创建按钮
        butto23_1 = Button(Navigation23,
                           text="清空",
                           width=10,
                           command=查询清空
                           )
        butto23_1.place(x=300,
                        y=200
                        )

        # 创建按钮
        butto23_2 = Button(Navigation23,
                           text="查询",
                           width=10,
                           command=查询防伪便签
                           )
        butto23_2.place(x=500,
                        y=200
                        )

        # 显示窗口
        查询界面.mainloop()

        pass

    # 处理登录校验
    # 校验密码
    if entry1.get() == "":
        print("账号为空，请输入账号")
    # 检测密码是不是空白
    elif entry2.get() == "":
        print("密码为空，请输入密码")
    else:
        # 读取用户信息文件
        # 创建数据库连接对象，并建立连接
        host = "localhost"
        port = 3306  # 端口名称
        user = "root"
        password = "123456"
        db = "my"  # 数据库名称
        charset = "utf8"
        db = pymysql.Connect(host=host,
                             port=port,
                             user=user,
                             passwd=password,
                             db=db,
                             charset=charset
                             )

        cursor = db.cursor()  # 创建游标对象
        sql = f"SELECT * FROM data;"  # 编写sql
        cursor.execute(sql)  # 执行sql
        data = cursor.fetchall()  # 获取多行数据

        # 关闭
        cursor.close()
        db.close()
        # print(data)

        # 初始化登录状态
        登录状态 = False

        # 初始化用户状态
        用户状态 = False

        # 检测用户名是否存在
        for i in data:
            if i[0] == entry1.get():
                # 用户存在
                用户状态 = True
                if i[1] == entry2.get():
                    登录状态 = True
                    break
                else:
                    print("密码错误！")
                    break

        # 判断用户是否存在
        if 用户状态 == False:
            print("用户不存在！")
        # 判断用户是否存在
        elif 登录状态 == True:
            print("登录成功！")

            # 把按键传递给变量 避免窗口名称出错
            账号 = entry1.get()
            密码 = entry2.get()

            # 关闭登录界面
            window.destroy()

            # 创建主界面窗口
            主界面 = Tk()

            # 设置窗口名称
            主界面.title(f'防伪码验证页面            账号：{账号} 密码：{密码}')

            # 登录窗口大小宽*高
            主界面.geometry('500x400')

            # 主标签
            Navigation01 = Label(主界面,  # 便签放在主界面界面
                                 # 设置标签内容区大小
                                 width=20,
                                 height=20,
                                 # 设置填充区距离、边框宽度和其样式
                                 padx=0,
                                 pady=0,
                                 borderwidth=1,
                                 relief="groove"
                                 )
            # 标签的右上角坐标和宽高
            Navigation01.place(x=0,
                               y=0,
                               width=500,
                               height=400
                               )

            # 创建按钮
            butto0_1 = Button(Navigation01,
                              text="生成防伪码",
                              width=10,
                              command=生成
                              )
            butto0_1.place(x=100,
                           y=180
                           )

            # 创建按钮
            butto0_1 = Button(Navigation01,
                              text="查询防伪码",
                              width=10,
                              command=查询
                              )
            butto0_1.place(x=300,
                           y=180
                           )

            # 显示窗口
            主界面.mainloop()


if __name__ == '__main__':
    # 初始化登录状态
    登录状态 = False

    # 创建登录窗口
    window = Tk()

    # 设置窗口标题
    window.title('登录')

    # 登录窗口大小宽*高
    window.geometry('360x200')

    # 窗口不能被拉伸
    window.resizable(0, 0)

    # 标签--导航
    Navigation0 = Label(window,
                        # 设置标签内容区大小
                        width=20,
                        height=20,
                        # 设置填充区距离、边框宽度和其样式
                        padx=0,
                        pady=0,
                        borderwidth=0,
                        relief="sunken"
                        )
    Navigation0.place(x=20,
                      y=20,
                      width=320,
                      height=260
                      )

    # 标签--导航
    Navigation1 = Label(Navigation0,
                        # 设置标签内容区大小
                        width=20,
                        height=20,
                        # 设置填充区距离、边框宽度和其样式
                        padx=0,
                        pady=0,
                        borderwidth=0,
                        relief="sunken"
                        )
    # 设置标签位置
    Navigation1.place(x=0,
                      y=0,
                      width=320,
                      height=40
                      )

    # 设定标题
    labe0 = Label(Navigation1,
                  text=" 防伪码验证系统",
                  fg='red',
                  font=("微软雅黑", 20)
                  )
    # 设定标题位置
    labe0.place(x=0,
                y=0,
                width=320,
                height=40
                )

    # 标签--导航
    Navigation2 = Label(Navigation0,
                        # 设置标签内容区大小
                        width=20,
                        height=20,
                        # 设置填充区距离、边框宽度和其样式
                        padx=0,
                        pady=0,
                        borderwidth=0,
                        relief="sunken"
                        )
    # 设置标签位置
    Navigation2.place(x=0,
                      y=50,
                      width=320,
                      height=80
                      )

    # 新建文本标签
    labe1 = Label(Navigation2,
                  text="\t用户名：")
    labe2 = Label(Navigation2,
                  text="\t密   码：")

    # 新建文本标签设定顺序
    labe1.grid(row=1,
               column=1
               )
    labe2.grid(row=2,
               column=1
               )

    # 输入框1、2
    entry1 = Entry(Navigation2)
    entry2 = Entry(Navigation2)

    # 输入框1、2设定顺序
    entry1.grid(row=1,
                column=2
                )
    entry2.grid(row=2,
                column=2
                )

    # 标签--导航
    Navigation3 = Label(Navigation0,
                        # 设置标签内容区大小
                        width=20,
                        height=20,
                        # 设置填充区距离、边框宽度和其样式
                        padx=0,
                        pady=0,
                        borderwidth=0,
                        relief="sunken"
                        )
    # 设置标签位置
    Navigation3.place(x=60,
                      y=120,
                      width=320,
                      height=140
                      )

    # 创建按钮
    button12 = Button(Navigation3,
                      text="登录",
                      width=10,
                      command=登录
                      )
    # 设定按钮位置
    button12.grid(row=3,
                  column=1,
                  sticky="e",
                  padx=10,
                  pady=5
                  )

    # 创建按钮
    button3 = Button(Navigation3,
                     text="清空",
                     width=10,
                     command=清空账号密码输入框
                     )
    # 设定按钮位置
    button3.grid(row=3,
                 column=2,
                 sticky="e",
                 padx=10,
                 pady=5
                 )

    # 显示窗口
    window.mainloop()
