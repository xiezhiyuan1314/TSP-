#-*-   coding:   utf-8   -*-
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import random
import threading
from queue import Queue
import time
import matplotlib.pyplot as plt
import math
import ACOYX
import GAYX
import PSOYX
import SOMYX
import TSYX
import SAYX
import os
from tkinter import filedialog
from PIL import ImageTk, Image
import  tkinter.messagebox
import  pickle

srt1 = '优点：1.较强的鲁棒性——稍加修改即可应用于其他问题，2.分布式计算——本质上具有并行性，3. 易于与其他启发式算法结合。\n' \
       '缺点：1、收敛速度慢，2、易于陷入局部最优。'
srt2 = '优点：1、 通过变异机制避免算法陷入局部最优，搜索能力强，2、 引入自然选择中的概率思想，个体的选择具有随机性，3、 可拓展性强，易于与其他算法进行结合使用。\n' \
       '缺点：1、 遗传算法编程较为复杂，涉及到基因编码与解码，2、 算法内包含的交叉率、变异率等参数的设定需要依靠经验确定，3、 对于初始种群的优劣依赖性较强。'
srt3 = '优点: 1.收敛速度较快，2.需要调整的参数少，原理简单，容易实现，这是PSO的最大优点，3.协同搜索，同时利用个体局部信息和群体全局信息进行指导搜索。\n' \
       '缺点：1.算法局部搜索能力较差，搜索精度不高，2算法不能保证搜索到全局最优解，主要有一下两个方面：①有时粒子群在俯冲过程中会错失全局最优解，②应用PSO算法处理高位复杂问题是，算法可能过早收敛，3.PSO算法是一种概率算法。'
srt4 = '优点：1.易于实施和使用，2.可以为各种问题提供最佳解决方案。\n' \
       '缺点：1.如果退火计划很长，运行可能需要很长时间，2.有许多需要调的参数。'
srt5 = '优点：1.自适应权值，极大方便寻找最优解。\n' \
       '缺点：1.在初始条件较差时，易陷入局部极小值。'
srt6 = '优点：1.搜索过程中可以接受劣解,因此具有较强的“爬山”能力,搜索时能够跳出局部最优解,转向解空间的其他区域,从而增加获得更好的全局最优解的概率2.新解不是在当前解的邻域中随机产生,而或是优于“best fso far”的解,或是非禁忌的最佳解,因此选取优良解的概率远远大于其它。\n' \
       '缺点：1.初始值敏感，即对初始解的依赖性较强,好的初始解有助于搜索很快的达到最优解,而较坏的初始解往往会使搜索很难或不能够达到最优解，2.迭代搜索过程是串行的,仅是单一状态的移动,而非并行搜索。'



window = tk.Tk()
window.title('登录界面')
window.geometry('400x300')
# 登陆界面
tk.Label(window, text='账户：').place(x=100,y=100)
tk.Label(window, text='密码：').place(x=100, y=140)

var_usr_name = tk.StringVar()
enter_usr_name = tk.Entry(window, textvariable=var_usr_name)
enter_usr_name.place(x=160, y=100)

var_usr_pwd = tk.StringVar()
enter_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
enter_usr_pwd.place(x=160, y=140)


# 登陆
def usr_log_in():
    # 输入框内容
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()

    try:
        with open('usr_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except:
        with open('usr_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)

    # 判断
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tsp_main()

        else:
            tk.messagebox.showerror(message='ERROR!')
    # 用户名密码不能为空
    elif usr_name == '' or usr_pwd == '':
        tk.messagebox.showerror(message='用户名不能为空！')


def usr_sign_quit():
    window.destroy()


def usr_sign_up():
    def signtowcg():
        NewName = new_name.get()
        NewPwd = new_pwd.get()
        ConfirPwd = pwd_comfirm.get()
        try:
            with open('usr_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            exist_usr_info = {}
        if NewName in exist_usr_info:
            tk.messagebox.showerror(message='用户名存在！')
        elif NewName == '' and NewPwd == '':
            tk.messagebox.showerror(message='用户名和密码不能为空！')
        elif NewPwd != ConfirPwd:
            tk.messagebox.showerror(message='密码前后不一致！')
        else:
            exist_usr_info[NewName] = NewPwd
            with open('usr_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo(message='注册成功！')
                window_sign_up.destroy()

    # 新建注册窗口
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('400x300')
    window_sign_up.title('sign_up')

    # 注册编辑框
    new_name = tk.StringVar()
    new_pwd = tk.StringVar()
    pwd_comfirm = tk.StringVar()

    tk.Label(window_sign_up, text='账户名：').place(x=90, y=50)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=160, y=50)

    tk.Label(window_sign_up, text='密码：').place(x=90, y=100)
    tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=160, y=100)

    tk.Label(window_sign_up, text='确认密码：').place(x=90, y=150)
    tk.Entry(window_sign_up, textvariable=pwd_comfirm, show='*').place(x=160, y=150)
    # 确认注册
    bt_confirm = tk.Button(window_sign_up, text='确定', command=signtowcg).place(x=180, y=220)


def tsp_main():
    global root,input1,text_show, best_length,srt
    window.destroy()
    root = tk.Tk()
    root.title('TSP最优化求解算法全复现')
    root.geometry('1200x670')
    w=tk.Canvas(root,bg='gray',heigh=670,width=1200)
    w.pack(side='top')

    tf = tk.Canvas(root, width=520, height=622, bg='red')
    tf.place(x=365, y=35)

    word1 = tk.Label(root,  bg='gray', fg='black', font=('宋体', 12),
                     width=148, height=1)
    word1.place(x=0, y=5)
    word2 = tk.Label(root,text='1-蚁群算法', bg='white', fg='black', font=('宋体', 8),
                     width=20, height=2)
    word2.place(x=45, y=45)
    word3 = tk.Label(root, text='2-遗传算法',bg='white', fg='black', font=('宋体', 8),
                     width=20, height=2)
    word3.place(x=180, y=45)
    word4 = tk.Label(root, text='3-粒子群算法',bg='white', fg='black', font=('宋体', 8),
                     width=20, height=2)
    word4.place(x=45, y=125)
    word5 = tk.Label(root, text='4-模拟退火算法',bg='white', fg='black', font=('宋体', 8),
                     width=20, height=2)
    word5.place(x=180, y=125)
    word6 = tk.Label(root, text='5-自组织神经网络算法',bg='white', fg='black', font=('宋体', 8),
                     width=20, height=2)
    word6.place(x=45, y=205)
    word7 = tk.Label(root, text='6-禁忌搜索算法',bg='white', fg='black', font=('宋体', 8),
                     width=20, height=2)
    word7.place(x=180, y=205)
    #左边的框
    w.create_line(5, 30, 350, 30, fill='blue')
    w.create_line(5, 665, 350, 665, fill='blue')
    w.create_line(5, 30, 5, 665, fill='blue')
    w.create_line(350, 30, 350, 665, fill='blue')
    #右边的框
    w.create_line(360, 30, 1195, 30, fill='blue')
    w.create_line(360, 665, 1195, 665, fill='blue')
    w.create_line(360, 30, 360, 665, fill='blue')
    w.create_line(1195, 30, 1195, 665, fill='blue')
   #左边框内两条线
    w.create_line(5, 400, 350, 400, fill='blue')
    w.create_line(5, 300, 350, 300, fill='blue')
    w.create_line(5, 500, 350, 500, fill='blue')
    w.create_line(895, 30, 895, 665, fill='blue')

    # w.create_line(360, 450, 995, 450, fill='blue')




    button1 = tk.Button(root, text='系统介绍', fg='black', font=('宋体', 10), width=8,command=jieshao)
    button1.place(x=5, y=5)
    button9 = tk.Button(root, text='图像分析', fg='black', font=('宋体', 10), width=8)
    button9.place(x=365, y=5)
    button10 = tk.Button(root, text='结果分析', fg='black', font=('宋体', 10), width=8)
    button10.place(x=900, y=5)
    button3 = tk.Button(root, text='退出', fg='black', font=('宋体', 10), width=10, command=quit_root)
    button3.place(x=180, y=5)
    button4 = tk.Button(root, text='数据选择', fg='black', font=('宋体', 10), width=10, command=openfiles1)
    button4.place(x=20, y=340)
    button5 = tk.Button(root, text='算法运行', fg='black', font=('宋体', 10), width=10,command=yunxing)
    button5.place(x=35, y=560)
    button7 = tk.Button(root, text='算法应用', fg='black', font=('宋体', 10), width=10,command=youxi)
    button7.place(x=235, y=560)
    button8 = tk.Button(root, text='请选择算法', fg='black', font=('宋体', 10), width=10)
    button8.place(x=20, y=440)
    button8 = tk.Button(root, text='清空', fg='black', font=('宋体', 10), width=10,command=cleartext)
    button8.place(x=85, y=5)
    var_username = tk.StringVar()
    input1 = tk.Entry(root, textvariable=var_username,show=None,font=('宋体', 15), width=20)
    input1.place(x=130, y=440)
    text_show = tk.Text(root, font=('宋体', 10), width=40, height=48)
    text_show.place(x=905, y=35)
    # tf = tk.Canvas(root1, width=30, height=20, bg='red')
    # tf.place(x=365, y=35)



    root.mainloop()

def yunxing():
    global best_length,srt,key
    tf = tk.Canvas(root, width=520, height=622, bg='red')
    tf.place(x=365, y=35)

    srt1 = '优点：1.较强的鲁棒性——稍加修改即可应用于其他问题，2.分布式计算——本质上具有并行性，3. 易于与其他启发式算法结合。\n' \
           '缺点：1、收敛速度慢，2、易于陷入局部最优。'
    srt2 = '优点：1、 通过变异机制避免算法陷入局部最优，搜索能力强，2、 引入自然选择中的概率思想，个体的选择具有随机性，3、 可拓展性强，易于与其他算法进行结合使用。\n' \
           '缺点：1、 遗传算法编程较为复杂，涉及到基因编码与解码，2、 算法内包含的交叉率、变异率等参数的设定需要依靠经验确定，3、 对于初始种群的优劣依赖性较强。'
    srt3 = '优点: 1.收敛速度较快，2.需要调整的参数少，原理简单，容易实现，这是PSO的最大优点，3.协同搜索，同时利用个体局部信息和群体全局信息进行指导搜索。\n' \
           '缺点：1.算法局部搜索能力较差，搜索精度不高，2算法不能保证搜索到全局最优解，主要有一下两个方面：①有时粒子群在俯冲过程中会错失全局最优解，②应用PSO算法处理高位复杂问题是，算法可能过早收敛，3.PSO算法是一种概率算法。'
    srt4 = '优点：1.易于实施和使用，2.可以为各种问题提供最佳解决方案。\n' \
           '缺点：1.如果退火计划很长，运行可能需要很长时间，2.有许多需要调的参数。'
    srt5 = '优点：1.自适应权值，极大方便寻找最优解。\n' \
           '缺点：1.在初始条件较差时，易陷入局部极小值。'
    srt6 = '优点：1.搜索过程中可以接受劣解,因此具有较强的“爬山”能力,搜索时能够跳出局部最优解,转向解空间的其他区域,从而增加获得更好的全局最优解的概率2.新解不是在当前解的邻域中随机产生,而或是优于“best fso far”的解,或是非禁忌的最佳解,因此选取优良解的概率远远大于其它。\n' \
           '缺点：1.初始值敏感，即对初始解的依赖性较强,好的初始解有助于搜索很快的达到最优解,而较坏的初始解往往会使搜索很难或不能够达到最优解，2.迭代搜索过程是串行的,仅是单一状态的移动,而非并行搜索。'

    if input1.get() != '':
        str_number = input1.get()
        a = str_number.split(',')    #   str_number="1,2,3"   a=['1','2','3'],  split可以帮助字符串变成其他例如列表

        if len(a)>1:
            #一个数据，多算法
            ytime,srt,cnt,best_length= show_tu(a, file_paths[0])


            for key,value in ytime.items():
                text_show.insert(tk.END,"算法")
                text_show.insert(tk.END, key)
                text_show.insert(tk.END, "运行时间")
                text_show.insert(tk.END, ":")
                text_show.insert(tk.END, value)
                text_show.insert(tk.END, "\n")




            for i in range(len(cnt)):
                text_show.insert(tk.END, "\n算法{}迭代次数:".format(list(ytime.keys())[i]))
                text_show.insert(tk.END, cnt[i])
                text_show.insert(tk.END, " ")
                text_show.insert(tk.END, "\n算法{}最佳路程:".format(list(ytime.keys())[i]))
                text_show.insert(tk.END, best_length[i])



            for i in range(len(srt)):
                text_show.insert(tk.END, "\n\n算法{}优缺点:\n".format(list(ytime.keys())[i]))
                text_show.insert(tk.END,srt[i])




        elif len(a) == 1:
            # 多个数据，一算法
            ytime,cnt,best_length = shuju(a, file_paths)
            for key, value in ytime.items():
                text_show.insert(tk.END, "数据")
                text_show.insert(tk.END, key)
                text_show.insert(tk.END, "运行时间")
                text_show.insert(tk.END, ":")
                text_show.insert(tk.END, value)
                text_show.insert(tk.END, "\n")

            for i in range(len(cnt)):
                text_show.insert(tk.END, "\n数据{}迭代次数:".format(list(ytime.keys())[i]))
                text_show.insert(tk.END, cnt[i])
                text_show.insert(tk.END, "\n数据{}最佳路程:".format(list(ytime.keys())[i]))
                text_show.insert(tk.END, best_length[i])


        else:
            print("笨蛋，写错了")

def shuju(lists,path):
    global best_length
    tf = tk.Canvas(root, width=500, height=552, bg='red')
    tf.place(x=365, y=35)

    length = len(lists)
    fig = plt.figure(figsize=(5, 6),dpi=105)
    ax1 = plt.subplot(4, 2, 1)
    # 第一行第二列图形
    ax2 = plt.subplot(4, 2, 2)
    # 第一行第三列图形
    ax3 = plt.subplot(4, 2, 3)
    # 第二行第一列图形
    ax4 = plt.subplot(4, 2, 4)
    # 第二行第二列图形
    ax5 = plt.subplot(4, 2, 5)
    # 第二行第三列图形
    ax6 = plt.subplot(4, 2, 6)
    # 第三行
    ax7 = plt.subplot(4, 1, 4)

    axlist = [ax1, ax2, ax3, ax4, ax5, ax6, ax7]

    time_list = {}
    cnt_list = []
    length_list = []

    for i in range(len(path)):
        start_time = time.time()

        st = path[i].split('/')[-1][:-4]
        if lists[0] == '1':

            Best_path1, model1,best_length,cnt = aco_main(path[i])
            plt.sca(axlist[i])
            plt.plot(Best_path1[:, 0], Best_path1[:, 1], 'r-.')
            iterations1 = model1.iter_x
            Best_record1 = model1.iter_y
            ax7.plot(iterations1, Best_record1,label=st)
            axlist[i].set_title(st)

        elif lists[0] == '2':
            Best_path2, model2,best_length,cnt = ga_main(path[i])
            plt.sca(axlist[i])
            plt.plot(Best_path2[:, 0], Best_path2[:, 1], 'p-.')
            iterations2 = model2.iter_x
            Best_record2 = model2.iter_y
            ax7.plot(iterations2, Best_record2,label=st)
            axlist[i].set_title(st)

        elif lists[0] == '3':
            Best_path3, model3,best_length,cnt = pso_main(path[i])
            plt.sca(axlist[i])
            plt.plot(Best_path3[:, 0], Best_path3[:, 1], 'g-.')
            iterations3 = model3.iter_x
            Best_record3 = model3.iter_y
            ax7.plot(iterations3, Best_record3,label=st)
            axlist[i].set_title(st)

        elif lists[0] == '4':
            Best_path4, model4,best_length,cnt = sa_main(path[i])
            plt.sca(axlist[i])
            plt.plot(Best_path4[:, 0], Best_path4[:, 1], 'b-.')
            iterations4 = model4.iter_x
            Best_record4 = model4.iter_y
            ax7.plot(iterations4, Best_record4,label=st)
            axlist[i].set_title(st)

        elif lists[0] == '5':
            Best_path5, model5,best_length,cnt= som_main(path[i])
            plt.sca(axlist[i])
            plt.plot(Best_path5[:, 0], Best_path5[:, 1], 'y-.')
            iterations5 = model5.iter_x
            Best_record5 = model5.iter_y
            ax7.plot(iterations5, Best_record5,label=st)
            axlist[i].set_title(st)

        elif lists[0] == '6':
            Best_path6, model6,best_length,cnt = ts_main(path[i])
            plt.sca(axlist[i])
            plt.plot(Best_path6[:, 0], Best_path6[:, 1], 'c-.')
            iterations6 = model6.iter_x
            Best_record6 = model6.iter_y
            ax7.plot(iterations6, Best_record6,label=st)
            axlist[i].set_title(st)

        end_time = time.time()
        time_list[i+1]= end_time - start_time
        cnt_list.append(cnt)
        length_list.append(best_length)
    ax7.legend()
    Canvas = FigureCanvasTkAgg(fig, master=tf)
    Canvas.draw()  # 注意show方法已经过时了,这里改用draw
    Canvas.get_tk_widget().pack(side=tk.TOP,  # 上对齐
                                fill=tk.BOTH,  # 填充方式
                                expand=tk.YES)
    return time_list,cnt_list,length_list

#多算法一种数据
def show_tu(lists,path):
    global best_length,srt
    tf = tk.Canvas(root, width=520, height=622, bg='red')
    tf.place(x=365, y=35)

    length = len(lists)

    srt1 = '优点：1.较强的鲁棒性——稍加修改即可应用于其他问题，2.分布式计算——本质上具有并行性，3. 易于与其他启发式算法结合。\n' \
           '缺点：1、收敛速度慢，2、易于陷入局部最优。'
    srt2 = '优点：1、 通过变异机制避免算法陷入局部最优，搜索能力强，2、 引入自然选择中的概率思想，个体的选择具有随机性，3、 可拓展性强，易于与其他算法进行结合使用。\n' \
           '缺点：1、 遗传算法编程较为复杂，涉及到基因编码与解码，2、 算法内包含的交叉率、变异率等参数的设定需要依靠经验确定，3、 对于初始种群的优劣依赖性较强。'
    srt3 = '优点: 1.收敛速度较快，2.需要调整的参数少，原理简单，容易实现，这是PSO的最大优点，3.协同搜索，同时利用个体局部信息和群体全局信息进行指导搜索。\n' \
           '缺点：1.算法局部搜索能力较差，搜索精度不高，2算法不能保证搜索到全局最优解，主要有一下两个方面：①有时粒子群在俯冲过程中会错失全局最优解，②应用PSO算法处理高位复杂问题是，算法可能过早收敛，3.PSO算法是一种概率算法。'
    srt4 = '优点：1.易于实施和使用，2.可以为各种问题提供最佳解决方案。\n' \
           '缺点：1.如果退火计划很长，运行可能需要很长时间，2.有许多需要调的参数。'
    srt5 = '优点：1.自适应权值，极大方便寻找最优解。\n' \
           '缺点：1.在初始条件较差时，易陷入局部极小值。'
    srt6 = '优点：1.搜索过程中可以接受劣解,因此具有较强的“爬山”能力,搜索时能够跳出局部最优解,转向解空间的其他区域,从而增加获得更好的全局最优解的概率2.新解不是在当前解的邻域中随机产生,而或是优于“best fso far”的解,或是非禁忌的最佳解,因此选取优良解的概率远远大于其它。\n' \
           '缺点：1.初始值敏感，即对初始解的依赖性较强,好的初始解有助于搜索很快的达到最优解,而较坏的初始解往往会使搜索很难或不能够达到最优解，2.迭代搜索过程是串行的,仅是单一状态的移动,而非并行搜索。'


    fig = plt.figure(figsize=(5, 6),dpi=105)

    # 第一行第一列图形
    ax1 = plt.subplot(4, 2, 1)
    # 第一行第二列图形
    ax2 = plt.subplot(4, 2, 2)
    # 第一行第三列图形
    ax3 = plt.subplot(4, 2, 3)
    # 第二行第一列图形
    ax4 = plt.subplot(4, 2, 4)
    # 第二行第二列图形
    ax5 = plt.subplot(4, 2, 5)
    # 第二行第三列图形
    ax6 = plt.subplot(4, 2, 6)
    # 第三行
    ax7 = plt.subplot(4, 1, 4)


    axlist = [ax1,ax2,ax3,ax4,ax5,ax6,ax7]

    time_list={}

    srt_list = [srt1,srt2,srt3,srt4,srt5,srt6]
    cnt_list = []
    length_list = []

    for i in range(0,length):
        start_time = time.time()
        if lists[i] == '1':  #ACO
            Best_path1, model1,best_length,cnt = aco_main(path)
            plt.sca(axlist[int(lists[i])-1])
            plt.plot(Best_path1[:, 0], Best_path1[:, 1], 'r-.')
            iterations1 = model1.iter_x
            Best_record1 = model1.iter_y
            ax7.plot(iterations1, Best_record1, color='red', label='aco')
            ax1.set_title('ACO')


        elif lists[i] == '2':  #GA
            Best_path2, model2,bset_length,cnt= ga_main(path)
            plt.sca(axlist[int(lists[i])-1])
            plt.plot(Best_path2[:, 0], Best_path2[:, 1], 'p--')
            iterations2 = model2.iter_x
            Best_record2 = model2.iter_y
            ax7.plot(iterations2, Best_record2, color='purple', label='ga')
            ax2.set_title('GA')


        elif lists[i] == '3':  # PSO
            Best_path3, model3,best_length,cnt= pso_main(path)
            plt.sca(axlist[int(lists[i])-1])
            plt.plot(Best_path3[:, 0], Best_path3[:, 1], 'g--')
            iterations3 = model3.iter_x
            Best_record3 = model3.iter_y
            ax7.plot(iterations3, Best_record3, color='gold', label='pso')
            ax3.set_title('PSO')


        elif lists[i] == '4':  #SA
            Best_path4, model4,best_length,cnt = sa_main(path)
            plt.sca(axlist[int(lists[i])-1])
            plt.plot(Best_path4[:, 0], Best_path4[:, 1], 'b--')
            iterations4 = model4.iter_x
            Best_record4 = model4.iter_y
            ax7.plot(iterations4, Best_record4, color='blue', label='sa')
            ax4.set_title('SA')

        elif lists[i] == '5':  # SOM
            Best_path5, model5,best_length,cnt= som_main(path)
            plt.sca(axlist[int(lists[i])-1])
            plt.plot(Best_path5[:, 0], Best_path5[:, 1], 'y--')
            iterations5 = model5.iter_x
            Best_record5 = model5.iter_y
            ax7.plot(iterations5, Best_record5, color='yellow', label='som')
            ax5.set_title('SOM')

        elif lists[i] == '6':  # TS
            Best_path6, model6,best_length,cnt= ts_main(path)
            plt.sca(axlist[int(lists[i])-1])
            plt.plot(Best_path6[:, 0], Best_path6[:, 1], 'c--')
            iterations6 = model6.iter_x
            Best_record6 = model6.iter_y
            ax7.plot(iterations6, Best_record6, color='cyan', label='ts')
            ax6.set_title('TS')
        cnt_list.append(cnt)
        length_list.append(best_length)
        end_time = time.time()
        time_list[lists[i]]= end_time - start_time
        ax7.set_title('iterations')

    ax7.legend()

    Canvas = FigureCanvasTkAgg(fig, master=tf)
    Canvas.draw()  # 注意show方法已经过时了,这里改用draw
    Canvas.get_tk_widget().pack(side=tk.TOP,  # 上对齐
                                fill=tk.BOTH,  # 填充方式
                                expand=tk.YES)

    return time_list ,srt_list,cnt_list,length_list


def youxi():
    if input1.get() != '':
        str_number = input1.get()
        a = str_number.split(',')
        print(a)
        for i in range(len(a)):
            if a[i] == '1':
                acoyx_name =ACOYX.acoyx_main()
            if a[i] == '2':
                gayx_name = GAYX.gayx_main()
            if a[i] == '3':
                psoyx_name =PSOYX.psoyx_main()
            if a[i] == '4':
                sayx_name = SAYX.sayx_main()
            if a[i] == '5':
                somyx_name = SOMYX.somyx_main()
            if a[i] == '6':
                tsyx_name = TSYX.tsyx_main()

def openfiles1():
    global file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[('text files', '.tsp'), ('pythonfiles', ('.py', '.pyw'))],
                 initialdir=(os.path.expanduser('D:/数据')))

    file_label = tk.Label(root, text=file_paths,bg='gray', fg='red', font=('宋体', 9),width=30, height=5)
    file_label.place(x=120, y=320)

#ACO
class ACO(object):
    def __init__(self, num_city, data):
        self.m = 50  # 蚂蚁数量
        self.alpha = 1  # 信息素重要程度因子
        self.beta = 5  # 启发函数重要因子
        self.rho = 0.1  # 信息素挥发因子
        self.Q = 1  # 常量系数
        self.num_city = num_city  # 城市规模
        self.location = data  # 城市坐标
        self.Tau = np.zeros([num_city, num_city])  # 信息素矩阵
        self.Table = [[0 for _ in range(num_city)] for _ in range(self.m)]  # 生成的蚁群
        self.iter = 1
        self.iter_max = 500
        self.dis_mat = self.compute_dis_mat(num_city, self.location)  # 计算城市之间的距离矩阵
        self.Eta = 10. / self.dis_mat  # 启发式函数
        self.paths = None  # 蚁群中每个个体的长度
        # 存储存储每个温度下的最终路径，画出收敛图
        self.iter_x = []
        self.iter_y = []
        # self.greedy_init(self.dis_mat,100,num_city)
    def greedy_init(self, dis_mat, num_total, num_city):
        start_index = 0
        result = []
        for i in range(num_total):
            rest = [x for x in range(0, num_city)]
            # 所有起始点都已经生成了
            if start_index >= num_city:
                start_index = np.random.randint(0, num_city)
                result.append(result[start_index].copy())
                continue
            current = start_index
            rest.remove(current)
            # 找到一条最近邻路径
            result_one = [current]
            while len(rest) != 0:
                tmp_min = math.inf
                tmp_choose = -1
                for x in rest:
                    if dis_mat[current][x] < tmp_min:
                        tmp_min = dis_mat[current][x]
                        tmp_choose = x

                current = tmp_choose
                result_one.append(tmp_choose)
                rest.remove(tmp_choose)
            result.append(result_one)
            start_index += 1
        pathlens = self.compute_paths(result)
        sortindex = np.argsort(pathlens)
        index = sortindex[0]
        result = result[index]
        for i in range(len(result)-1):
            s = result[i]
            s2 = result[i+1]
            self.Tau[s][s2]=1
        self.Tau[result[-1]][result[0]] = 1
        # for i in range(num_city):
        #     for j in range(num_city):
        # return result

    # 轮盘赌选择
    def rand_choose(self, p):
        x = np.random.rand()
        for i, t in enumerate(p):
            x -= t
            if x <= 0:
                break
        return i

    # 生成蚁群
    def get_ants(self, num_city):
        for i in range(self.m):
            start = np.random.randint(num_city - 1)
            self.Table[i][0] = start
            unvisit = list([x for x in range(num_city) if x != start])
            current = start
            j = 1
            while len(unvisit) != 0:
                P = []
                # 通过信息素计算城市之间的转移概率
                for v in unvisit:
                    P.append(self.Tau[current][v] ** self.alpha * self.Eta[current][v] ** self.beta)
                P_sum = sum(P)
                P = [x / P_sum for x in P]
                # 轮盘赌选择一个一个城市
                index = self.rand_choose(P)
                current = unvisit[index]
                self.Table[i][j] = current
                unvisit.remove(current)
                j += 1

    # 计算不同城市之间的距离
    def compute_dis_mat(self, num_city, location):
        dis_mat = np.zeros((num_city, num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    dis_mat[i][j] = np.inf
                    continue
                a = location[i]
                b = location[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                dis_mat[i][j] = tmp
        return dis_mat

    # 计算一条路径的长度
    def compute_pathlen(self, path, dis_mat):
        a = path[0]
        b = path[-1]
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result

    # 计算一个群体的长度
    def compute_paths(self, paths):
        result = []
        for one in paths:
            length = self.compute_pathlen(one, self.dis_mat)
            result.append(length)
        return result

    # 更新信息素
    def update_Tau(self):
        delta_tau = np.zeros([self.num_city, self.num_city])
        paths = self.compute_paths(self.Table)
        for i in range(self.m):
            for j in range(self.num_city - 1):
                a = self.Table[i][j]
                b = self.Table[i][j + 1]
                delta_tau[a][b] = delta_tau[a][b] + self.Q / paths[i]
            a = self.Table[i][0]
            b = self.Table[i][-1]
            delta_tau[a][b] = delta_tau[a][b] + self.Q / paths[i]
        self.Tau = (1 - self.rho) * self.Tau + delta_tau

    def aco(self):
        best_lenth = math.inf
        best_path = None
        for cnt in range(self.iter_max):
            # 生成新的蚁群
            self.get_ants(self.num_city)  # out>>self.Table
            self.paths = self.compute_paths(self.Table)
            # 取该蚁群的最优解
            tmp_lenth = min(self.paths)
            tmp_path = self.Table[self.paths.index(tmp_lenth)]
            # 可视化初始的路径
            if cnt == 0:
                init_show = self.location[tmp_path]
                init_show = np.vstack([init_show, init_show[0]])
            # 更新最优解
            if tmp_lenth < best_lenth:
                best_lenth = tmp_lenth
                best_path = tmp_path
            # 更新信息素
            self.update_Tau()

            # 保存结果
            self.iter_x.append(cnt)
            self.iter_y.append(best_lenth)
            print(cnt,best_lenth)
        return best_lenth, best_path,cnt

    def run(self):
        best_length, best_path ,cnt= self.aco()
        return self.location[best_path], best_path,best_length,cnt


# 读取数据
def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data

def aco_main(path):
    global best_length
    data = read_tsp(path)
    data = np.array(data)
    data = data[:, 1:]
    model1 = ACO(num_city=data.shape[0], data=data.copy())
    Best_path1,Best_path, Best_length ,cnt= model1.run()
    Best_path1 = np.vstack([Best_path1, Best_path1[0]])

    return Best_path1,model1,Best_length,cnt


#Ga
class GA(object):
    def __init__(self, num_city, num_total, iteration, data):
        self.num_city = num_city
        self.num_total = num_total
        self.scores = []
        self.iteration = iteration
        self.location = data
        self.ga_choose_ratio = 0.2
        self.mutate_ratio = 0.05
        # fruits中存每一个个体是下标的list
        self.dis_mat = self.compute_dis_mat(num_city, data)
        self.fruits = self.greedy_init(self.dis_mat,num_total,num_city)
        # 显示初始化后的最佳路径
        scores = self.compute_adp(self.fruits)
        sort_index = np.argsort(-scores)
        init_best = self.fruits[sort_index[0]]
        init_best = self.location[init_best]

        # 存储每个iteration的结果，画出收敛图
        self.iter_x = [0]
        self.iter_y = [1. / scores[sort_index[0]]]

    def random_init(self, num_total, num_city):
        tmp = [x for x in range(num_city)]
        result = []
        for i in range(num_total):
            random.shuffle(tmp)
            result.append(tmp.copy())
        return result

    def greedy_init(self, dis_mat, num_total, num_city):
        start_index = 0
        result = []
        for i in range(num_total):
            rest = [x for x in range(0, num_city)]
            # 所有起始点都已经生成了
            if start_index >= num_city:
                start_index = np.random.randint(0, num_city)
                result.append(result[start_index].copy())
                continue
            current = start_index
            rest.remove(current)
            # 找到一条最近邻路径
            result_one = [current]
            while len(rest) != 0:
                tmp_min = math.inf
                tmp_choose = -1
                for x in rest:
                    if dis_mat[current][x] < tmp_min:
                        tmp_min = dis_mat[current][x]
                        tmp_choose = x

                current = tmp_choose
                result_one.append(tmp_choose)
                rest.remove(tmp_choose)
            result.append(result_one)
            start_index += 1
        return result
    # 计算不同城市之间的距离
    def compute_dis_mat(self, num_city, location):
        dis_mat = np.zeros((num_city, num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    dis_mat[i][j] = np.inf
                    continue
                a = location[i]
                b = location[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                dis_mat[i][j] = tmp
        return dis_mat

    # 计算路径长度
    def compute_pathlen(self, path, dis_mat):
        try:
            a = path[0]
            b = path[-1]
        except:
            import pdb
            pdb.set_trace()
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result

    # 计算种群适应度
    def compute_adp(self, fruits):
        adp = []
        for fruit in fruits:
            if isinstance(fruit, int):
                import pdb
                pdb.set_trace()
            length = self.compute_pathlen(fruit, self.dis_mat)
            adp.append(1.0 / length)
        return np.array(adp)

    def swap_part(self, list1, list2):
        index = len(list1)
        list = list1 + list2
        list = list[::-1]
        return list[:index], list[index:]

    def ga_cross(self, x, y):
        len_ = len(x)
        assert len(x) == len(y)
        path_list = [t for t in range(len_)]
        order = list(random.sample(path_list, 2))
        order.sort()
        start, end = order

        # 找到冲突点并存下他们的下标,x中存储的是y中的下标,y中存储x与它冲突的下标
        tmp = x[start:end]
        x_conflict_index = []
        for sub in tmp:
            index = y.index(sub)
            if not (index >= start and index < end):
                x_conflict_index.append(index)

        y_confict_index = []
        tmp = y[start:end]
        for sub in tmp:
            index = x.index(sub)
            if not (index >= start and index < end):
                y_confict_index.append(index)

        assert len(x_conflict_index) == len(y_confict_index)

        # 交叉
        tmp = x[start:end].copy()
        x[start:end] = y[start:end]
        y[start:end] = tmp

        # 解决冲突
        for index in range(len(x_conflict_index)):
            i = x_conflict_index[index]
            j = y_confict_index[index]
            y[i], x[j] = x[j], y[i]

        assert len(set(x)) == len_ and len(set(y)) == len_
        return list(x), list(y)

    def ga_parent(self, scores, ga_choose_ratio):
        sort_index = np.argsort(-scores).copy()
        sort_index = sort_index[0:int(ga_choose_ratio * len(sort_index))]
        parents = []
        parents_score = []
        for index in sort_index:
            parents.append(self.fruits[index])
            parents_score.append(scores[index])
        return parents, parents_score

    def ga_choose(self, genes_score, genes_choose):
        sum_score = sum(genes_score)
        score_ratio = [sub * 1.0 / sum_score for sub in genes_score]
        rand1 = np.random.rand()
        rand2 = np.random.rand()
        for i, sub in enumerate(score_ratio):
            if rand1 >= 0:
                rand1 -= sub
                if rand1 < 0:
                    index1 = i
            if rand2 >= 0:
                rand2 -= sub
                if rand2 < 0:
                    index2 = i
            if rand1 < 0 and rand2 < 0:
                break
        return list(genes_choose[index1]), list(genes_choose[index2])

    def ga_mutate(self, gene):
        path_list = [t for t in range(len(gene))]
        order = list(random.sample(path_list, 2))
        start, end = min(order), max(order)
        tmp = gene[start:end]
        # np.random.shuffle(tmp)
        tmp = tmp[::-1]
        gene[start:end] = tmp
        return list(gene)

    def ga(self):
        # 获得优质父代
        scores = self.compute_adp(self.fruits)
        # 选择部分优秀个体作为父代候选集合
        parents, parents_score = self.ga_parent(scores, self.ga_choose_ratio)
        tmp_best_one = parents[0]
        tmp_best_score = parents_score[0]
        # 新的种群fruits
        fruits = parents.copy()
        # 生成新的种群
        while len(fruits) < self.num_total:
            # 轮盘赌方式对父代进行选择
            gene_x, gene_y = self.ga_choose(parents_score, parents)
            # 交叉
            gene_x_new, gene_y_new = self.ga_cross(gene_x, gene_y)
            # 变异
            if np.random.rand() < self.mutate_ratio:
                gene_x_new = self.ga_mutate(gene_x_new)
            if np.random.rand() < self.mutate_ratio:
                gene_y_new = self.ga_mutate(gene_y_new)
            x_adp = 1. / self.compute_pathlen(gene_x_new, self.dis_mat)
            y_adp = 1. / self.compute_pathlen(gene_y_new, self.dis_mat)
            # 将适应度高的放入种群中
            if x_adp > y_adp and (not gene_x_new in fruits):
                fruits.append(gene_x_new)
            elif x_adp <= y_adp and (not gene_y_new in fruits):
                fruits.append(gene_y_new)

        self.fruits = fruits

        return tmp_best_one, tmp_best_score

    def run(self):
        BEST_LIST = None
        best_length = -math.inf
        self.best_record = []
        for cnt in range(1, self.iteration + 1):
            tmp_best_one, tmp_best_score = self.ga()
            self.iter_x.append(cnt)
            self.iter_y.append(1. / tmp_best_score)
            if tmp_best_score > best_length:
                best_length = tmp_best_score
                BEST_LIST = tmp_best_one
            self.best_record.append(1./best_length)
            print(cnt,1./best_length)
        print(1./best_length)
        return self.location[BEST_LIST],cnt,1./best_length


# 读取数据

def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data

def ga_main(path):
    global best_length
    data = read_tsp(path)
    data = np.array(data)
    data = data[:, 1:]
    Best, Best_path2 = math.inf, None
    model2 = GA(num_city=data.shape[0], num_total=25, iteration=500, data=data.copy())
    path,cnt,best_length = model2.run()
    if best_length < Best:
        Best = best_length
        Best_path2 = path
    # 加上一行因为会回到起点

    return Best_path2,model2,best_length,cnt

#PSO
class PSO(object):
    def __init__(self, num_city, data):
        self.iter_max = 500  # 迭代数目
        self.num = 200  # 粒子数目
        self.num_city = num_city  # 城市数
        self.location = data # 城市的位置坐标
        # 计算距离矩阵
        self.dis_mat = self.compute_dis_mat(num_city, self.location)  # 计算城市之间的距离矩阵
        # 初始化所有粒子
        # self.particals = self.random_init(self.num, num_city)
        self.particals = self.greedy_init(self.dis_mat,num_total=self.num,num_city =num_city)
        self.lenths = self.compute_paths(self.particals)
        # 得到初始化群体的最优解
        init_l = min(self.lenths)
        init_index = self.lenths.index(init_l)
        init_path = self.particals[init_index]
        # 画出初始的路径图
        init_show = self.location[init_path]
        # 记录每个个体的当前最优解
        self.local_best = self.particals
        self.local_best_len = self.lenths
        # 记录当前的全局最优解,长度是iteration
        self.global_best = init_path
        self.global_best_len = init_l
        # 输出解
        self.best_length = self.global_best_len
        self.best_path = self.global_best
        # 存储每次迭代的结果，画出收敛图
        self.iter_x = [0]
        self.iter_y = [init_l]
    def greedy_init(self, dis_mat, num_total, num_city):
        start_index = 0
        result = []
        for i in range(num_total):
            rest = [x for x in range(0, num_city)]
            # 所有起始点都已经生成了
            if start_index >= num_city:
                start_index = np.random.randint(0, num_city)
                result.append(result[start_index].copy())
                continue
            current = start_index
            rest.remove(current)
            # 找到一条最近邻路径
            result_one = [current]
            while len(rest) != 0:
                tmp_min = math.inf
                tmp_choose = -1
                for x in rest:
                    if dis_mat[current][x] < tmp_min:
                        tmp_min = dis_mat[current][x]
                        tmp_choose = x

                current = tmp_choose
                result_one.append(tmp_choose)
                rest.remove(tmp_choose)
            result.append(result_one)
            start_index += 1
        return result

    # 随机初始化
    def random_init(self, num_total, num_city):
        tmp = [x for x in range(num_city)]
        result = []
        for i in range(num_total):
            random.shuffle(tmp)
            result.append(tmp.copy())
        return result

    # 计算不同城市之间的距离
    def compute_dis_mat(self, num_city, location):
        dis_mat = np.zeros((num_city, num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    dis_mat[i][j] = np.inf
                    continue
                a = location[i]
                b = location[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                dis_mat[i][j] = tmp
        return dis_mat

    # 计算一条路径的长度
    def compute_pathlen(self, path, dis_mat):
        a = path[0]
        b = path[-1]
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result

    # 计算一个群体的长度
    def compute_paths(self, paths):
        result = []
        for one in paths:
            length = self.compute_pathlen(one, self.dis_mat)
            result.append(length)
        return result

    # 评估当前的群体
    def eval_particals(self):
        min_lenth = min(self.lenths)
        min_index = self.lenths.index(min_lenth)
        cur_path = self.particals[min_index]
        # 更新当前的全局最优
        if min_lenth < self.global_best_len:
            self.global_best_len = min_lenth
            self.global_best = cur_path
        # 更新当前的个体最优
        for i, l in enumerate(self.lenths):
            if l < self.local_best_len[i]:
                self.local_best_len[i] = l
                self.local_best[i] = self.particals[i]

    # 粒子交叉
    def cross(self, cur, best):
        one = cur.copy()
        l = [t for t in range(self.num_city)]
        t = np.random.choice(l,2)
        x = min(t)
        y = max(t)
        cross_part = best[x:y]
        tmp = []
        for t in one:
            if t in cross_part:
                continue
            tmp.append(t)
        # 两种交叉方法
        one = tmp + cross_part
        l1 = self.compute_pathlen(one, self.dis_mat)
        one2 = cross_part + tmp
        l2 = self.compute_pathlen(one2, self.dis_mat)
        if l1<l2:
            return one, l1
        else:
            return one, l2


    # 粒子变异
    def mutate(self, one):
        one = one.copy()
        l = [t for t in range(self.num_city)]
        t = np.random.choice(l, 2)
        x, y = min(t), max(t)
        one[x], one[y] = one[y], one[x]
        l2 = self.compute_pathlen(one,self.dis_mat)
        return one, l2

    # 迭代操作
    def pso(self):
        for cnt in range(1, self.iter_max):
            # 更新粒子群
            for i, one in enumerate(self.particals):
                tmp_l = self.lenths[i]
                # 与当前个体局部最优解进行交叉
                new_one, new_l = self.cross(one, self.local_best[i])
                if new_l < self.best_length:
                    self.best_length = tmp_l
                    self.best_path = one

                if new_l < tmp_l or np.random.rand()<0.1:
                    one = new_one
                    tmp_l = new_l

                # 与当前全局最优解进行交叉
                new_one, new_l = self.cross(one, self.global_best)

                if new_l < self.best_length:
                    self.best_length = tmp_l
                    self.best_path = one

                if new_l < tmp_l or np.random.rand()<0.1:
                    one = new_one
                    tmp_l = new_l
                # 变异
                one, tmp_l = self.mutate(one)

                if new_l < self.best_length:
                    self.best_length = tmp_l
                    self.best_path = one

                if new_l < tmp_l or np.random.rand()<0.1:
                    one = new_one
                    tmp_l = new_l

                # 更新该粒子
                self.particals[i] = one
                self.lenths[i] = tmp_l
            # 评估粒子群，更新个体局部最优和个体当前全局最优
            self.eval_particals()
            # 更新输出解
            if self.global_best_len < self.best_length:
                self.best_length = self.global_best_len
                self.best_path = self.global_best
            print(cnt, self.best_length)
            self.iter_x.append(cnt)
            self.iter_y.append(self.best_length)
        return self.best_length, self.best_path,cnt

    def run(self):
        best_length, best_path,cnt= self.pso()
        # 画出最终路径
        return self.location[best_path], best_path,best_length,cnt


# 读取数据
def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data

def pso_main(path):
    global best_length
    data = read_tsp(path)
    data = np.array(data)
    data = data[:, 1:]
    model3 = PSO(num_city=data.shape[0], data=data.copy())
    Best_path3, Best ,best_length,cnt= model3.run()

    Best_path3 = np.vstack([Best_path3, Best_path3[0]])
    return Best_path3,model3,best_length,cnt

#SA
class SA(object):
    def __init__(self, num_city, data):
        self.T0 = 4000
        self.Tend = 1e-3
        self.rate = 0.9995
        self.num_city = num_city
        self.scores = []
        self.location = data
        # fruits中存每一个个体是下标的list
        self.fires = []
        self.dis_mat = self.compute_dis_mat(num_city, data)
        self.fire = self.greedy_init(self.dis_mat,100,num_city)
        # 显示初始化后的路径
        init_pathlen = 1. / self.compute_pathlen(self.fire, self.dis_mat)
        init_best = self.location[self.fire]
        # 存储存储每个温度下的最终路径，画出收敛图
        self.iter_x = [0]
        self.iter_y = [1. / init_pathlen]
    def greedy_init(self, dis_mat, num_total, num_city):
        start_index = 0
        result = []
        for i in range(num_total):
            rest = [x for x in range(0, num_city)]
            # 所有起始点都已经生成了
            if start_index >= num_city:
                start_index = np.random.randint(0, num_city)
                result.append(result[start_index].copy())
                continue
            current = start_index
            rest.remove(current)
            # 找到一条最近邻路径
            result_one = [current]
            while len(rest) != 0:
                tmp_min = math.inf
                tmp_choose = -1
                for x in rest:
                    if dis_mat[current][x] < tmp_min:
                        tmp_min = dis_mat[current][x]
                        tmp_choose = x

                current = tmp_choose
                result_one.append(tmp_choose)
                rest.remove(tmp_choose)
            result.append(result_one)
            start_index += 1
        pathlens = self.compute_paths(result)
        sortindex = np.argsort(pathlens)
        index = sortindex[0]
        return result[index]

    # 初始化一条随机路径
    def random_init(self, num_city):
        tmp = [x for x in range(num_city)]
        random.shuffle(tmp)
        return tmp

    # 计算不同城市之间的距离
    def compute_dis_mat(self, num_city, location):
        dis_mat = np.zeros((num_city, num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    dis_mat[i][j] = np.inf
                    continue
                a = location[i]
                b = location[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                dis_mat[i][j] = tmp
        return dis_mat

    # 计算路径长度
    def compute_pathlen(self, path, dis_mat):
        a = path[0]
        b = path[-1]
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result

    # 计算一个温度下产生的一个群体的长度
    def compute_paths(self, paths):
        result = []
        for one in paths:
            length = self.compute_pathlen(one, self.dis_mat)
            result.append(length)
        return result

    # 产生一个新的解：随机交换两个元素的位置
    def get_new_fire(self, fire):
        fire = fire.copy()
        t = [x for x in range(len(fire))]
        a, b = np.random.choice(t, 2)
        fire[a:b] = fire[a:b][::-1]
        return fire

    # 退火策略，根据温度变化有一定概率接受差的解
    def eval_fire(self, raw, get, temp):
        len1 = self.compute_pathlen(raw, self.dis_mat)
        len2 = self.compute_pathlen(get, self.dis_mat)
        dc = len2 - len1
        p = max(1e-1, np.exp(-dc / temp))
        if len2 < len1:
            return get, len2
        elif np.random.rand() <= p:
            return get, len2
        else:
            return raw, len1

    # 模拟退火总流程
    def sa(self):
        cnt = 0
        # 记录最优解
        best_path = self.fire
        best_length = self.compute_pathlen(self.fire, self.dis_mat)

        while self.T0 > self.Tend:
            cnt += 1
            # 产生在这个温度下的随机解
            tmp_new = self.get_new_fire(self.fire.copy())
            # 根据温度判断是否选择这个解
            self.fire, file_len = self.eval_fire(best_path, tmp_new, self.T0)
            # 更新最优解
            if file_len < best_length:
                best_length = file_len
                best_path = self.fire
            # 降低温度
            self.T0 *= self.rate
            # 记录路径收敛曲线
            self.iter_x.append(cnt)
            self.iter_y.append(best_length)
            print(cnt, best_length)
        return best_length, best_path,cnt

    def run(self):
        best_length, best_path,cnt = self.sa()
        return self.location[best_path], best_length,cnt


# 读取数据
def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data

def sa_main(path):
    global best_length
    data = read_tsp(path)
    start_time = time.time()
    data = np.array(data)
    data = data[:, 1:]
    show_data = np.vstack([data, data[0]])
    Best, Best_path = math.inf, None

    model4 = SA(num_city=data.shape[0], data=data.copy())
    path, best_length,cnt = model4.run()
    if best_length < Best:
        Best = best_length
        Best_path4 = path
    # 加上一行因为会回到起点
    Best_path4 = np.vstack([Best_path4, Best_path4[0]])
    return Best_path4, model4,best_length,cnt

#SOM
class SOM(object):
    def __init__(self, num_city, data):
        self.num_city = num_city
        self.location = data.copy()
        self.iteraton = 500
        self.learning_rate = 0.8
        self.dis_mat = self.compute_dis_mat(num_city, self.location)
        self.best_path = []
        self.best_length = math.inf
        self.iter_x = []
        self.iter_y = []

    def normalize(self, points):
        """
        Return the normalized version of a given vector of points.
        For a given array of n-dimensions, normalize each dimension by removing the
        initial offset and normalizing the points in a proportional interval: [0,1]
        on y, maintining the original ratio on x.
        """
        ratio = (points[:, 0].max() - points[:, 1].min()) / (points[:, 1].max() - points[:, 1].min()), 1
        ratio = np.array(ratio) / max(ratio)
        m = lambda c: (c - c.min()) / (c.max() - c.min())
        norm = m(points)
        # norm = points.apply(lambda c: (c - c.min()) / (c.max() - c.min()))
        m = lambda p: ratio * p
        return m(norm)
        # return norm.apply(lambda p: ratio * p, axis=1)

    def generate_network(self, size):
        """
        Generate a neuron network of a given size.
        Return a vector of two dimensional points in the interval [0,1].
        """
        return np.random.rand(size, 2)

    def get_neighborhood(self, center, radix, domain):
        """Get the range gaussian of given radix around a center index."""

        # Impose an upper bound on the radix to prevent NaN and blocks
        if radix < 1:
            radix = 1

        # Compute the circular network distance to the center
        deltas = np.absolute(center - np.arange(domain))
        distances = np.minimum(deltas, domain - deltas)

        # Compute Gaussian distribution around the given center
        return np.exp(-(distances * distances) / (2 * (radix * radix)))

    def get_route(self, cities, network):
        """Return the route computed by a network."""
        f = lambda c: self.select_closest(network, c)
        dis = []
        for city in cities:
            dis.append(f(city))
        index = np.argsort(dis)
        return index

    def select_closest(self, candidates, origin):
        """Return the index of the closest candidate to a given point."""
        return self.euclidean_distance(candidates, origin).argmin()

    def euclidean_distance(self, a, b):
        """Return the array of distances of two numpy arrays of points."""
        return np.linalg.norm(a - b, axis=1)

    def route_distance(self, cities):
        """Return the cost of traversing a route of cities in a certain order."""
        points = cities[['x', 'y']]
        distances = self.euclidean_distance(points, np.roll(points, 1, axis=0))
        return np.sum(distances)

    # 随机初始化
    def random_init(self, num_total, num_city):
        tmp = [x for x in range(num_city)]
        result = []
        for i in range(num_total):
            random.shuffle(tmp)
            result.append(tmp.copy())
        return result

    # 计算不同城市之间的距离
    def compute_dis_mat(self, num_city, location):
        dis_mat = np.zeros((num_city, num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    dis_mat[i][j] = np.inf
                    continue
                a = location[i]
                b = location[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                dis_mat[i][j] = tmp
        return dis_mat

    # 计算一条路径的长度
    def compute_pathlen(self, path, dis_mat):
        a = path[0]
        b = path[-1]
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result

    def smo(self):
        citys = self.normalize(self.location)
        n = citys.shape[0] * 8
        network = self.generate_network(n)

        for i in range(self.iteraton):
            index = np.random.randint(self.num_city - 1)
            city = citys[index]
            winner_idx = self.select_closest(network, city)

            gaussian = self.get_neighborhood(winner_idx, n // 10, network.shape[0])

            network += gaussian[:, np.newaxis] * self.learning_rate * (city - network)

            self.learning_rate = self.learning_rate * 0.99997
            n = n * 0.9997
            if n < 1:
                break
            route = self.get_route(citys, network)
            route_l = self.compute_pathlen(route, self.dis_mat)
            if route_l < self.best_length:
                self.best_length = route_l
                self.best_path = route
            self.iter_x.append(i)
            self.iter_y.append(self.best_length)
            print(i, self.iteraton, self.best_length)
            # 画出初始化的路径
            # if i == 0:
            #     plt.subplot(2, 2, 2)
            #     plt.title('convergence curve')
            #     show_data = self.location[self.best_path]
            #     show_data = np.vstack([show_data, show_data[0]])
            #     plt.plot(show_data[:, 0], show_data[:, 1])

        return self.best_length, self.best_path

    def run(self):
        self.best_length, self.best_path = self.smo()
        return self.location[self.best_path], self.best_length,self.iteraton


# 读取数据
def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data

def som_main(path):
    global best_length
    data = read_tsp(path)
    start_time = time.time()
    data = np.array(data)
    data = data[:, 1:]
    show_data = np.vstack([data, data[0]])
    Best, Best_path = math.inf, None

    model5 = SOM(num_city=data.shape[0], data=data.copy())
    path, best_length,cnt= model5.run()
    if best_length < Best:
        Best = best_length
        Best_path5 = path
    # 加上一行因为会回到起点
    Best_path5 = np.vstack([Best_path5, Best_path5[0]])
    return Best_path5, model5,best_length,cnt


#TS
class TS(object):
    def __init__(self, num_city, data):
        self.taboo_size = 5
        self.iteration = 500
        self.num_city = num_city
        self.location = data
        self.taboo = []

        self.dis_mat = self.compute_dis_mat(num_city, data)
        self.path = self.greedy_init(self.dis_mat,100,num_city)
        self.best_path = self.path
        self.cur_path = self.path
        self.best_length = self.compute_pathlen(self.path, self.dis_mat)

        # 显示初始化后的路径
        init_pathlen = 1. / self.compute_pathlen(self.path, self.dis_mat)
        # 存储结果，画出收敛图
        self.iter_x = [0]
        self.iter_y = [1. / init_pathlen]
    def greedy_init(self, dis_mat, num_total, num_city):
        start_index = 0
        result = []
        for i in range(num_total):
            rest = [x for x in range(0, num_city)]
            # 所有起始点都已经生成了
            if start_index >= num_city:
                start_index = np.random.randint(0, num_city)
                result.append(result[start_index].copy())
                continue
            current = start_index
            rest.remove(current)
            # 找到一条最近邻路径
            result_one = [current]
            while len(rest) != 0:
                tmp_min = math.inf
                tmp_choose = -1
                for x in rest:
                    if dis_mat[current][x] < tmp_min:
                        tmp_min = dis_mat[current][x]
                        tmp_choose = x

                current = tmp_choose
                result_one.append(tmp_choose)
                rest.remove(tmp_choose)
            result.append(result_one)
            start_index += 1
        pathlens = self.compute_paths(result)
        sortindex = np.argsort(pathlens)
        index = sortindex[0]
        return result[index]
        # return result[0]

    # 初始化一条随机路径
    def random_init(self, num_city):
        tmp = [x for x in range(num_city)]
        random.shuffle(tmp)
        return tmp

    # 计算不同城市之间的距离
    def compute_dis_mat(self, num_city, location):
        dis_mat = np.zeros((num_city, num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    dis_mat[i][j] = np.inf
                    continue
                a = location[i]
                b = location[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                dis_mat[i][j] = tmp
        return dis_mat

    # 计算路径长度
    def compute_pathlen(self, path, dis_mat):
        a = path[0]
        b = path[-1]
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result

    # 计算一个群体的长度
    def compute_paths(self, paths):
        result = []
        for one in paths:
            length = self.compute_pathlen(one, self.dis_mat)
            result.append(length)
        return result

    # 产生随机解
    def ts_search(self, x):
        moves = []
        new_paths = []
        while len(new_paths)<400:
            i = np.random.randint(len(x))
            j = np.random.randint(len(x))
            tmp = x.copy()
            tmp[i:j] = tmp[i:j][::-1]
            new_paths.append(tmp)
            moves.append([i, j])
        return new_paths, moves

    # 禁忌搜索
    def ts(self):
        for i in range(self.iteration):
            new_paths, moves = self.ts_search(self.cur_path)
            new_lengths = self.compute_paths(new_paths)
            sort_index = np.argsort(new_lengths)
            min_l = new_lengths[sort_index[0]]
            min_path = new_paths[sort_index[0]]
            min_move = moves[sort_index[0]]

            # 更新当前的最优路径
            if min_l < self.best_length:
                self.best_length = min_l
                self.best_path = min_path
                self.cur_path = min_path
                # 更新禁忌表
                if min_move in self.taboo:
                    self.taboo.remove(min_move)

                self.taboo.append(min_move)
            else:
                # 找到不在禁忌表中的操作
                while min_move in self.taboo:
                    sort_index = sort_index[1:]
                    min_path = new_paths[sort_index[0]]
                    min_move = moves[sort_index[0]]
                self.cur_path = min_path
                self.taboo.append(min_move)
            # 禁忌表超长了
            if len(self.taboo) > self.taboo_size:
                self.taboo = self.taboo[1:]
            self.iter_x.append(i)
            self.iter_y.append(self.best_length)
            print(i, self.best_length)

        print(self.best_length)
        return  i

    def run(self):
        i = self.ts()
        return self.location[self.best_path], self.best_length,i


# 读取数据
def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data

def ts_main(path):
    global best_length
    data = read_tsp(path)
    start_time = time.time()
    data = np.array(data)
    data = data[:, 1:]
    show_data = np.vstack([data, data[0]])
    Best, Best_path = math.inf, None

    model6 = TS(num_city=data.shape[0], data=data.copy())
    path, best_length,cnt = model6.run()
    if best_length < Best:
        Best = best_length
        Best_path6 = path
    # 加上一行因为会回到起点
    Best_path6 = np.vstack([Best_path6, Best_path6[0]])
    return Best_path6, model6,best_length,cnt




def cleartext():
    text_show.delete(1.0,tk.END)
def jieshao():
    root2 = tk.Tk()
    root2.title('对比系统')
    root2.geometry('450x500')
    op = tk.Label(root2, text='操作手册', bg='gray', fg='black', font=('楷体', 20), width=32, height=2)
    op.pack()
    bz = tk.Text(root2, font=('楷体', 12), width=54, height=23)
    bz.place(x=5, y=65)
    bz.insert(tk.END, "  本设计系统解决TSP最优化算法的相关问题，选择对应的数据，进行路程图，迭代次数图形成"
                      "以及最终的结果分析展示，展示内容有算法运行时间，迭代次数，最佳路程，以及算法优缺点，使用步骤：\n")
    bz.insert(tk.END, "=====================================================\n")
    bz.insert(tk.END, "  1、点击数据选择:这里的数据有六种，但是建议您这里之选择前五种数据；\n")
    bz.insert(tk.END, "  2、选择算法:这里您如果数据选择的是多种请只输入一种算法，如果您选择一种数据则可以选择多种算法；\n")
    bz.insert(tk.END, "  3、点击算法运行:右侧文本框中将会显示分析结果，以及图像形成；\n")
    bz.insert(tk.END, "====================================================\n")
    bz.insert(tk.END, " 注意事项：\n")
    bz.insert(tk.END, "  1、不可以同时选择两种以上数据和多种算法运行否则系统会报错；\n")
    bz.insert(tk.END, "  2、在使用算法之前请先选择数据否则系统会报错；\n")
    bz.insert(tk.END, "  3、算法游戏不需要进行数据选择，但这里只能选择一种算法；\n")
    bz.insert(tk.END, "  4、这里的算法有对应的数字，请直接输入数字并用英文”，“隔开；\n")
    bz.insert(tk.END, "====================================================\n")
    bz.insert(tk.END, " 使用建议：\n")
    bz.insert(tk.END, "  1、在完成一次算法对比后请点击清空按钮，方便您直接观察结果；\n")
    bz.insert(tk.END, "  2、在使用算法之前请先选择数据否则系统会报错；\n")
    bz.insert(tk.END, "====================================================\n")
    bz.insert(tk.END, " 致歉：\n")
    bz.insert(tk.END, "  本系统在操作结果上无任何问题，但还存在许多细节上的问题，比如："
                      "  图片大小无法调节、数据选择太过简洁、数据过大时运行算法非常缓慢等，"
                      "  对此，感到抱歉！，本人会继续加大对系统的改善方便大家友好使用。\n")








def quit_root():
    root.quit()
#多数据一种算法

#登录 注册按钮
bt_login = tk.Button(window,text='登录',command=usr_log_in)
bt_login.place(x=120,y=230)

bt_signup = tk.Button(window,text='注册',command=usr_sign_up)
bt_signup.place(x=190,y=230)

bt_logquit = tk.Button(window,text='退出',command=usr_sign_quit)
bt_logquit.place(x=260,y=230)

window.mainloop()









