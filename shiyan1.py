#!-*-coding:utf-8 -*-
#!@Author : 'xuran'
#!@Time   : 19-4-1 上午10:44


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
# 关键字
keywords = {'cahr':101,'int':102,'float':103,'break':104,'const':105,'return':106,'void':107,'continue':108,'do':109,
            'while':110,'if':111,'else':112,'for':113}
# 运算符
operators = {'(':201,')': 202,'[':203,']':204,'!':205,'*':206,'/':207,'%':208,'+':209,'-':210,'<':211,'<=':212,'>':213,
             '>=':214,'==':215,'!=':216,'&&':217,'||':218,'=':219,'.':220}
# 界符
delimiters = {'{':301, '}':302, ';':303,',':304,'\"':305}

# 文件内容
content = None

class Lexer(object):
    # 初始化
    def __init__(self):
        self.savetoken=[]

    # 判断是否为空白字符
    @staticmethod
    def is_blank(index):
        return content[index] == ' ' or content[index] == '\t' or content[index] == '\n' or content[index] == '\r'
    # 跳过空白字符
    def skip_blank(self, index):
        while index < len(content) and self.is_blank(index):
            index += 1
        return index

    # 判断是否为关键字
    @staticmethod
    def is_keyword(value):
        for item in keywords:
            if value == item:
                return True
        return False

    # 词法分析主程序
    def main(self):
        i = 0
        while i < len(content):
            i = self.skip_blank(i)
            # 如果是字母或者是以下划线开头
            if content[i].isalpha() or content[i] == '_':
                # 找到该字符串
                temp = ''
                while i < len(content) and (
                                content[i].isalpha() or content[i] == '_' or content[i].isdigit() or content[
                        i] == '*' or content[i] == '.'):
                    temp += content[i]
                    i += 1
                # 判断该字符串
                if self.is_keyword(temp):
                    print("关键字:%25s--------->种别码:%d"%(temp,keywords[temp]))
                    self.savetoken.append(["关键字",temp,keywords[temp]])

                else:
                    print("标识符:%25s--------->种别码:%d" % (temp, 700))
                    self.savetoken.append(["标识符", temp, 700])
                i = self.skip_blank(i)
            # 如果是数字开头
            elif content[i].isdigit():
                temp = ''
                while i < len(content):
                    if content[i].isdigit() or (content[i] == '.' and content[i + 1].isdigit()):
                        temp += content[i]
                        i += 1
                    elif not content[i].isdigit():
                        if content[i] == '.':
                            print('float number error!')
                            exit()
                        else:
                            break
                if '.' not in temp:
                    print("整数:%25s--------->种别码:%d" % (temp, 400))
                    self.savetoken.append(["整数", temp, 400])
                else:
                    print("实数:%25s--------->种别码:%d" % (temp, 800))
                    self.savetoken.append(["实数", temp, 800])
                i = self.skip_blank(i)
            # 如果是界符
            elif content[i] in delimiters:
                print("界符:%25s--------->种别码:%d" % (content[i], delimiters[content[i]]))
                self.savetoken.append(["界符", content[i], delimiters[content[i]]])
                # 如果是字符串常量
                if content[i] == '\"':
                    i += 1
                    temp = ''
                    while i < len(content):
                        if content[i] != '\"':
                            temp += content[i]
                            i += 1
                        else:
                            break
                    else:
                        print('error:lack of \"')
                        exit()
                    print("字符串:%25s--------->种别码:%d" % (temp, 600))
                    self.savetoken.append(["字符串", temp, 600])
                    print("界符:%25s--------->种别码:%d" % ('\"', delimiters['\"']))
                    self.savetoken.append(["界符",'\"', delimiters['\"']])
                i = self.skip_blank(i + 1)
            # 如果是运算符
            elif content[i] or content[i]+content[i+1] in operators:
                # 两个字符的运算符
                temp = content[i]+content[i+1]
                if temp in operators:
                    print("运算符:%25s--------->种别码:%d" % (temp, operators[temp]))
                    self.savetoken.append(["运算符", temp, operators[temp]])
                    i = self.skip_blank(i + 2)
                # 其他
                else:
                    temp = content[i]
                    print("运算符:%25s--------->种别码:%d" % (temp, operators[temp]))
                    self.savetoken.append(["运算符", temp, operators[temp]])
                    i = self.skip_blank(i + 1)
        return self.savetoken

class UI():
    def __init__(self):
        root = Tk()
        self.create_content(root)
        self.search_key
        root.title("xuran")
        root.update()

        #屏幕中心居中
        curWidth = root.winfo_width()
        curHeight = root.winfo_height()
        scnWidth, scnHeight = root.maxsize()
        tmpcnf = '+%d+%d' % ((scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
        root.geometry(tmpcnf)
        root.mainloop()

    def create_content(self, root):

        lf = ttk.LabelFrame(root, text="词法分析器")
        lf.pack(fill=X, padx=15, pady=8)

        top_frame = Frame(lf)
        top_frame.pack(fill=X,expand=YES,side=TOP,padx=15,pady=8)

        self.search_key = StringVar()

        bottom_frame = Frame(lf)
        bottom_frame.pack(fill=BOTH, expand=YES, side=TOP, padx=15, pady=8)

        tree = ttk.Treeview(bottom_frame)  # 表格
        tree["columns"] = ("类型", "内容", "种别码")

        tree.column("类型", width=100)  # 表示列,不显示
        tree.column("内容", width=200)
        tree.column("种别码", width=100)

        tree.heading("类型", text="类型")  # 显示表头
        tree.heading("内容", text="内容")
        tree.heading("种别码", text="种别码")

        ttk.Entry(top_frame, textvariable=self.search_key,width=50).pack(fill=X,expand=YES,side=LEFT)
        ttk.Button(top_frame,text="打开文件",command=self.open_file,width=10).pack(padx=15,fill=X,expand=YES)
        ttk.Button(top_frame, text="执行代码",command=lambda :self.process(tree)).pack(padx=15, fill=X, expand=YES)
        tree.pack()

    def open_file(self):
        path_ = askopenfilename()
        self.search_key.set(path_)

    def process(self,tree):
        source_file = open(str(self.search_key.get()))
        global content
        content = source_file.read()
        source_file.close()
        lexer = Lexer()
        text = lexer.main()
        for i in range(len(text)):
            tree.insert("", i, text=i, values=text[i])  # 插入数据


if __name__ == '__main__':
    UI()




