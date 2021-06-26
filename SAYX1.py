import random
import math

def Sa(x)->float:
    return (math.cos(math.pi*x/15)+1)*(30-abs(x/2))
def standard(p):
    return (int(p[0]*100)/100,int(p[1]*100)/100)
def dist(p,q)->float:
    return math.sqrt(abs(p[0]-q[0])**2+abs(p[1]-q[1])**2)

class ST:
    def __init__(self,T=100,threshold=1e-3,r=0.9995):
        self.n=0
        self.i=0
        self.y=[0]
        self.running=False
        self.T=0
        self.Tmax=T
        self.threshold=threshold*T
        self.r=r
        self.cnt=0
    def clear(self):
        self.n = 0
        self.i = 0
        self.y = [0]
        self.running = False
        self.T = 0
    def restart(self):
        self.i=0
        self.T=self.Tmax
        self.running=True
        self.bound=(0,0)
        self.cnt=0
    def genedata(self):
        self.y.clear()
        self.n = 100
        self.i = 0
        self.cnt=0
        self.T=0
        self.running = False
        phi=random.randint(30,70)
        for j in range(self.n):
            self.y.append(int(Sa(j-phi))+random.randint(-2,2))
    def next(self):
        if not self.running:
            return
        # 0.5概率向后转移，或者无法向前转移时也向后转移
        if self.i<=self.bound[1] or (self.i<self.n-1 and random.random()<0.5):
            self.forward()
        # 否则向前转移
        else:
            self.back()
        self.T *= self.r
        if self.T<self.threshold:
            self.running=False
    # 向后转移，仅当劣解时候降温
    def back(self):
        j=self.i-1
        delta=self.y[j]-self.y[self.i]
        if delta>=0:
            self.i=j
            self.cnt = 0
        else:
            if math.exp(delta/self.T)*100>random.randint(0,100):
                self.i=j
                self.cnt = 0
            else:
                self.cnt+=1
    # 向前转移，仅当劣解时候降温
    def forward(self):
        j = self.i + 1
        delta = self.y[j] - self.y[self.i]
        if delta >= 0:
            self.i = j
            self.cnt=0
            # if self.y[j]>self.bound[0]:
            #     self.bound=(self.y[j],j)
        else:
            if math.exp(delta / self.T) > random.random():
                self.i = j
                self.cnt = 0
            else:
                self.cnt+=1

class _2D_SA:
    def __init__(self,T=100,threshold=0.01,r=0.999):
        self.n=0
        self.p=set()
        self.T=0
        self.Tmax=T
        self.threshold=threshold
        self.r=r
        self.cnt=0
        self.pos=(0,0)
        self.dis=0
        self.running=False
    def clear(self):
        self.n=0
        self.p.clear()
        self.T=0
        self.pos=(0,0)
        self.dis=0
        self.running=False
    def restart(self):
        self.T=self.Tmax
        self.pos=(random.randint(1,9),random.randint(1,9))
        self.dis=self.dissum(self.pos)
        self.cnt=0
        self.running=True
    def genedata(self,n):
        self.clear()
        for i in range(n):
            self.p.add((random.randint(1,9),random.randint(1,9)))
        self.n=len(self.p)
    def dissum(self,p):
        s=0
        for q in self.p:
            s+=math.sqrt(abs(q[0]-p[0])**2+abs(q[1]-p[1])**2)
        return s
    def in_range(self,p):
        return p[0]>0 and p[0]<10 and p[1]>0 and p[1]<10
    def next(self):
        if not self.running:
            return
        ang=random.random()*2*math.pi
        v=(math.cos(ang),math.sin(ang))
        newpos=standard((self.pos[0]+v[0],self.pos[1]+v[1]))
        newpos=(min(newpos[0],9),min(newpos[1],9))
        newpos=(max(newpos[0],1),max(newpos[1],1))
        newdis=self.dissum(newpos)
        d=newdis-self.dis
        if d<0:
            self.pos=newpos
            self.dis=newdis
            self.cnt=0
        else:
            if math.exp(-d/self.T)>random.random():
                self.pos=newpos
                self.dis=newdis
                self.cnt=0
            else:
                self.cnt+=1
        self.T*=self.r
        if self.T<self.threshold:
            self.running=False

class TSP:
    def __init__(self,T=100,threshold=0.1,r=0.999):
        self.n=0
        self.city=list()
        self.T=0
        self.Tmax=T
        self.threshold=threshold
        self.r=r
        self.running=False
        self.cur=list()
        self.dis=0
    def clear(self):
        self.n=0
        self.city=list()
        self.T=0
        self.cur=list()
        self.dis=0
        self.running=False
    def restart(self):
        self.T=self.Tmax
        self.cur=[i for i in range(self.n)]
        self.dis=self.wsum(self.cur)
        self.running=True
    def genedata(self,n=10):
        self.clear()
        s=set()
        for i in range(n):
            s.add((random.randint(1,9),random.randint(1,9)))
        self.n=len(s)
        self.city=list(s)
        self.d=[[0 for i in range(self.n)] for j in range(self.n)]
        for i in range(self.n):
            for j in range(i+1,self.n):
                self.d[i][j]=self.d[j][i]=dist(self.city[i],self.city[j])
    def wsum(self,path):
        rt=0
        for i in range(len(path)):
            rt+=self.d[path[i-1]][path[i]]
        return rt
    def next(self):
        if not self.running:
            return
        tmp=self.cur.copy()
        l=random.randint(1,self.n-2)
        r=random.randint(l+1,self.n-1)
        tmp[l]=self.cur[r]
        tmp[r]=self.cur[l]
        tmpdis=self.wsum(tmp)
        d=(tmpdis-self.dis)*10
        if d<0:
            self.cur=tmp.copy()
            self.dis=tmpdis
        elif math.exp(-d/self.T)>random.random():
            self.cur=tmp.copy()
            self.dis=tmpdis
        self.T*=self.r
        if self.T<self.threshold:
            self.running=False
