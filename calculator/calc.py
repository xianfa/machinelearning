#!/user/bin/python
# coding=utf-8

import Tkinter

def OnClickbtn0(value):
    print 'OnClickbut0 called'
    #清空内容
    if('C' == value):
        default_value.set('0')
        return
    #删除最后一个字符
    if('D' == value):
        return
    str = default_value.get()
    if('=' == value):
        default_value.set(eval(str))
        return
    #添加一个字符
    if('0' == str):
        str = ''
    str += value
    default_value.set(str)

def Run():

    win.title('计算器')
    win.resizable(0,0)
    win.geometry('400x600')

    #构造Edit显示
    default_value.set('1234')
    text = Tkinter.Text(win, state=Tkinter.DISABLED, height=100, width=400)
    #text.place(x=0, y=0);
    entry = Tkinter.Entry(win, state=Tkinter.DISABLED, width=400, font=("Arial", 20), textvariable=default_value)
    entry.place(x=0, y=0)

    #构造按钮
    btntextlist = ['C','(',')','D','7','8','9','+','4','5','6','-','1','2','3','*','.','0','=','/']
    for i in range(0,5):
        for j in range(0,4):
            cvalue = btntextlist[4*i+j]
            print 'cvalue is :' + cvalue
            btn = Tkinter.Button(win, bitmap="info", text=cvalue, font=("Arial", 50), width=100, height=100, compound=Tkinter.LEFT, command=lambda value=cvalue : OnClickbtn0(value))
            btn.place(x=j*100, y=100+i*100);

    # 进入消息循环
    win.mainloop()

if __name__ == '__main__':
    win = Tkinter.Tk()
    default_value = Tkinter.StringVar()
    Run()