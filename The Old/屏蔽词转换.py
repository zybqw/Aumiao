from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
# 导入库文件


class Ui(Frame):
    # 定义类(YouLikeMe)、继承于 Frame 框架 (虚拟的矩形框架)
    def __init__(self, master=None):
        # 定义构造函数、并初始化父类为空
        super().__init__(master)
        # 通过 super() 调用父类、并将 master 传进去
        self.master = master
        # 令此类中的 master 等于传入的 window
        self.grid()
        # 布局此窗口

        self.CreateWidget()
        # 调用另一个函数 CreateWidget


    def Shielding(self,content):
        return b'\xe2\x80\xaa'.decode(
            'UTF-8').join([i for i in content])


    def _write(self):
        st2=self.st2
        self.st2['state'] = NORMAL
        st2.delete(0.0, "end")
        print(self.st.get('0.0', 'end'))
        print(self.Shielding(self.st.get('0.0', 'end')))
        st2.insert(0.0, self.Shielding(self.st.get('0.0', 'end')))
        self.st2['state'] = DISABLED


    def copy(self):
        self.st2['state'] = NORMAL
        self.st2.event_generate('<<Copy>>')
        self.st2['state'] = DISABLED

    def CreateWidget(self):
        """
        用途:创建组件
        """
        win=self.master

        win.resizable(width=False, height=False)
        win.wm_attributes('-topmost', 0)
        Label(win, text='内\n容', font=(10)).grid(row=0, column=0, rowspan=3)
        self.st = ScrolledText(win, height=10, width=20)
        self.st.grid(row=0, column=1, columnspan=3, rowspan=3)
        Label(win, text='转\n换', font=(10)).grid(row=4, column=0, rowspan=3)
        self.st2 = ScrolledText(win, height=10, width=20, state=DISABLED)
        self.st2.grid(row=4, column=1, columnspan=3, rowspan=3)

        Button(win, text='转换', command=self._write, width=10,
            height=6).grid(row=0, column=5, rowspan=4)

        Button(win, text='复制 选中状态', command=self.copy, width=10,
            height=3).grid(row=5, column=5, rowspan=1)
        Button(win, text='退出', command=exit, width=10,
            height=3).grid(row=6, column=5, rowspan=1)

        mainloop()




if __name__ == "__main__":

    win = Tk()
    win.title('防喵工具')
    app = Ui(master=win)
    # 调用新创建的类、并进行初始化、将 master = window (主窗口)传递进去

    win.mainloop()
    # 调用 mainloop 方法、启用窗口并进入事件循环
