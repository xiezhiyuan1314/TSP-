import SAYX4
import Resources
import SAYX1
from SAYX3 import *
from SAYX5 import *

def tr(i,j,d=0)->tuple:
    return (50+i*5+d,500-j*5+d)
def trsa(p,d=0)->tuple:
    return (50+int(p[0]/0.02)+d,100+int(p[1]/0.02)+d)

class App(object):
    def __init__(self):
        self.game=SAYX4.Game(600,750,'模拟退火')
        self.id=0
        self.st=SAYX1.ST()
        self.sa=SAYX1._2D_SA()
        self.tsp=SAYX1.TSP()
        self.res=Resources.Res()
        #bind event handler
        self.res.ui_res['Start_btn'].button_clicked=self.Start_clicked
        self.res.ui_res['Gene_btn'].button_clicked=self.Gene_clicked
        self.res.ui_res['ST_btn'].button_clicked=self.ST_clicked
        self.res.ui_res['SA_btn'].button_clicked=self.SA_clicked
        self.res.ui_res['TSP_btn'].button_clicked=self.TAP_clicked
        #load to pool
        self.game.static_ui_pool=[
            self.res.ui_res['Start_btn'],
            self.res.ui_res['Gene_btn'],
            self.res.ui_res['ST_btn'],
            self.res.ui_res['SA_btn'],
            self.res.ui_res['TSP_btn']
        ]
        self.game.static_sprite_pool = [
            self.res.sprite_res['bg'],
            self.res.sprite_res['tool_bar']
        ]
    def exec(self,tick_flip):
        while True:
            self.game.clock.tick(tick_flip)
            self.game.Event_Handle()
            self.update()
            self.game.Render()
            self.lines_render()
    def update(self):
        if self.id==0:
            for k in range(10):
                self.st.next()
        elif self.id==1:
            for k in range(10):
                self.sa.next()
        else:
            for k in range(10):
                self.tsp.next()
        self.res_upd()
    def res_upd(self):
        if self.id==0:
            self.res.sprite_res['temper_bar'].scale(1+int(self.st.T+1)*299//self.st.Tmax,20)
            self.res.ui_res['Temper'].set_content('温度T={:.1f}'.format(self.st.T))
            self.res.ui_res['ST_info'].set_content('当前峰值={0}'.format(self.st.y[self.st.i]))
            self.game.sprite_pool=[
                self.res.sprite_res['temper_bar']
            ]
            self.game.ui_pool=[
                self.res.ui_res['Temper'],
                self.res.ui_res['ST_info']
            ]
        elif self.id==1:
            self.res.sprite_res['temper_bar'].scale(1+int(self.sa.T+1)*299//self.st.Tmax,20)
            self.res.ui_res['Temper'].set_content('温度T={:.2f}'.format(self.sa.T))
            self.res.ui_res['SA_info'].set_content(
                '当前坐标:({:.2f},{:.2f})\t距离和={:.2f}'.format(self.sa.pos[0],self.sa.pos[1],self.sa.dis))
            self.game.sprite_pool = [
                self.res.sprite_res['temper_bar']
            ]
            self.game.ui_pool = [
                self.res.ui_res['Temper'],
                self.res.ui_res['SA_info']
            ]
            for q in self.sa.p:
                self.game.sprite_pool.append(Sprite('assets/black.png',5,5,trsa(q,-2)))
            if self.sa.running:
                self.game.sprite_pool.append(Sprite('assets/red.png',5,5,trsa(self.sa.pos,-2)))
            else:
                self.game.sprite_pool.append(Sprite('assets/green.png', 5, 5, trsa(self.sa.pos, -2)))
        else:
            self.res.sprite_res['temper_bar'].scale(1 + int(self.tsp.T + 1) * 299 // self.tsp.Tmax, 20)
            self.res.ui_res['Temper'].set_content('温度T={:.1f}'.format(self.tsp.T))
            self.res.ui_res['TSP_info'].set_content('当前回路长={:.2f}'.format(self.tsp.dis))
            self.game.sprite_pool = [
                self.res.sprite_res['temper_bar']
            ]
            self.game.ui_pool = [
                self.res.ui_res['Temper'],
                self.res.ui_res['TSP_info']
            ]
            for q in self.tsp.city:
                self.game.sprite_pool.append(Sprite('assets/black.png', 5, 5, trsa(q, -2)))
    def Start_clicked(self):
        if self.id==0:
            if len(self.st.y)>0:
                self.st.restart()
        elif self.id==1:
            if self.sa.n>0:
                self.sa.restart()
        else:
            if self.tsp.n>0:
                self.tsp.restart()
    def Gene_clicked(self):
        if self.id==0:
            self.st.genedata()
            self.res_upd()
        elif self.id==1:
            self.sa.genedata(10)
            self.res_upd()
        else:
            self.tsp.genedata()
            self.res_upd()
    def ST_clicked(self):
        self.id=0
        self.st.clear()
    def SA_clicked(self):
        self.id=1
        self.sa.clear()
    def TAP_clicked(self):
        self.id=2
        self.tsp.clear()
    def lines_render(self):
        if self.id==0:
            for j in range(1,self.st.n):
                self.game.Line(tr(j-1,self.st.y[j-1]),tr(j,self.st.y[j]),(0,0,0))
            if self.st.running:
                self.game.Line((50+self.st.i*5,600),(50+self.st.i*5,100),(255,0,0))
            else:
                self.game.Line((50 + self.st.i * 5, 600), (50 + self.st.i * 5, 100), (0,255,0))
        elif self.id==1:
            if self.sa.running:
                tmp = trsa(self.sa.pos)
                self.game.Line((tmp[0],100),(tmp[0],600),(255,0,0))
                self.game.Line((50,tmp[1]),(550,tmp[1]),(255,0,0))
            else:
                tmp = trsa(self.sa.pos)
                self.game.Line((tmp[0], 100), (tmp[0], 600), (0, 255, 0))
                self.game.Line((50, tmp[1]), (550, tmp[1]), (0, 255, 0))
        else:
            if self.tsp.running:
                for i in range(len(self.tsp.cur)):
                    self.game.Line(trsa(self.tsp.city[self.tsp.cur[i-1]]),
                                   trsa(self.tsp.city[self.tsp.cur[i]]),(255,0,0))
            else:
                for i in range(len(self.tsp.cur)):
                    self.game.Line(trsa(self.tsp.city[self.tsp.cur[i - 1]]),
                                   trsa(self.tsp.city[self.tsp.cur[i]]), (0,255, 0))
        pygame.display.flip()