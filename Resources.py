from SAYX2 import *
from SAYX5 import *

class Res(object):
    def __init__(self):
        self.sprite_res={
            'bg':Sprite('assets/bg.png',500,500,(50,100),-1),
            'tool_bar':Sprite('assets/default/button.png',500,80,(50,10)),
            'temper_bar':Sprite('assets/temper.png',300,20,(200,40))
        }
        self.ui_res={
            'Start_btn':Button(100,50,(130,675),0,'开始',20),
            'Gene_btn':Button(100,50,(370,675),0,'生成',20),
            'ST_btn':Button(100,50,(100,600),0,'峰值模型',20),
            'SA_btn':Button(100,50,(250,600),0,'二维模型',20),
            'TSP_btn':Button(100,50,(400,600),0,'TSP模型',20),
            'Temper':Font('温度T=0',(70,40),20),
            'ST_info':Font('当前峰值=0',(250,120),20),
            'SA_info':Font('当前坐标:(0,0)\t距离和=0',(150,120),20),
            'TSP_info':Font('当前回路长=0',(200,120),20)
        }