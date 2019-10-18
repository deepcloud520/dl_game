import random as rd
def die(nb=6):
    return rd.randint(1,nb)
class kapai:
    def __init__(self,name,info,owner,**ksx):
        self.name=name
        self.info=info
        self.owner=owner
        self.ksx=ksx
    def get(self,name,de=0):return self.ksx.get(name,de)
    def use(self,ps):
        ps.calcsxs('att',self.get('att'))
        ps.calcsxs('dev',self.get('dev'))
        ps.calcsxs('mov',self.get('mov'))
        ps.calcsxs('hel',self.get('hel'))
        ps.xg.append(self.get('xg'))
class penson:
    def __init__(self,name,kps,gol,lev=1,**sxs):
        self.xg=[]
        self.name=name
        self.passkp=[]
        self.kps=kps
        self.sxs=sxs
    def get(self,name,de=0):return self.sxs.get(name,de)
    def set(self,name,value):self.sxs.update({name:value})
    def calcsxs(self,name,value):
        self.set(name,self.get(name)-value)
    def getatt(self):
        return self.get('att')+die(6)
    def getdev(self,att):
        dev=self.get('dev')+die(6)-self.get('att')
        return dev if dev>=0 else 0
    def getmov(self,att):
        mov=self.get('mov')+die(6)
        return att if mov<att else 0
    def kp_add(self,kp):
        if len(self.kps)<6:
            self.kps.append(kp)
        else:
            return False
        return True
    def add_hel(self,hel):
        self.set('hel',self.get('hel')+hel)
        if self.get('hel')>self.get('maxhel'):
            self.set('hel',self.get('maxhel'))
    def calc_xg(self):
        if self.get('xg'):
            info=[]
            for dd in self.xg:
                if dd=='fire':
                    info.append(('fire',-1))
                    self.calcsxs('hel',1)
                    self.xg.remove('fire')
    def clean_kp(self):
        self.passkp=[]
    def __str__(self):
        return ' str:'+self.name+' passkp:'+str(self.passkp)+' sxs:'+str(self.sxs)

class dl_game:
    def __init__(self,plname,kps=[kapai('火剑攻击','带火的剑！','you',hel=3,xg='fire')]):
        self.layer=1
        self.map=[]
        self.mons=[penson('slm',[kapai('普通攻击','','you',hel=2)],3,lev=self.layer,att=1,hel=3,maxhel=3,dev=2,mov=1)]
        self.rmft=0         #room foots
        self.kps=kps        #kapais
        self.hh='player'
        self.player=penson(plname,self.kps,0,att=2,dev=1,mov=0,hel=5,maxhel=5)
        self.nms=[]         #now monters
        self.nowm=''        #now monter
    def mapend(self,st):
        self.map.append(st)
    def gen_map(self):      #gen the map
        self.map=[]
        bx=self.layer//4+1
        gw=self.layer
        xx=bx//2+1
        self.mapend('start')
        for i in range(bx+gw+xx):
            r=[]
            if bx>0:r.append('bx')
            if gw>0:r.append('gw')
            if xx>0:r.append('xx')
            xz=rd.choice(r)
            if xz=='bx':
                self.mapend('bx')
                bx-=1
            elif xz=='gw':
                self.mapend('gw')
                gw-=1
            else:
                self.mapend('xx')
                xx-=1
        self.mapend('end')
    def __gen_mons(self):
        gs=self.layer//6+1
        for nb in range(gs):
            self.nms.append(rd.choice(self.mons))
    def __openbox(self):
        return rd.choice(self.kps[self.player.get('lev'):])
    def __xxroom(self):
        self.player.add_hel(1)
    def pass_kp(self,no):
        if self.hh=='player':
            self.player.passkp.append(self.player.kps[no])
        else:
            if self.nowm:
                self.nowm.passkp.append(self.player.kps[no])
    def pass_hh(self,cl=None):
        if self.nowm.get('hel')<=0:
            if nms:
                self.nms.remove(self.nowm)
                self.nowm=self.nms[0]
            else:
                return 'end'
        if self.hh=='player':
            for kp in self.player.kps:
                if kp.owner=='me':kp.use(self.player)
                else:kp.use(self.nowm)
            self.player.clean_kp()
            self.hh='monter'
        else:
            for kp in self.nowm.kps:
                if kp.owner=='me':kp.use(self.nowm)
                else:kp.use(self.player)
            self.nowm.clean_kp()
            self.hh='player'
    def go(self):
        nroom=self.map[self.rmft]
        info=''
        if nroom=='bx':
            if not self.player.kp_add(self.__openbox()):
                info='remove'
            else:
                self.player.kp_add(self.__openbox())
                info='bx'
        elif nroom=='xx':
            self.__xxroom()
            info='xx'
        elif nroom=='start':
            info='start'
        elif nroom=='end':
            self.gen_map()
            info='end'
        elif nroom=='gw':
            info='fight'
            self.__gen_mons()
            self.nowm=self.nms[0]
        else:
            pass
        if info:self.rmft+=1
        return info
    def __str__(self):
        return 'layer:'+str(self.layer)+' player:'+self.player.__str__()
m=dl_game('swwm')
m.layer=3
m.gen_map()
print(m.map)
print(m.go())
print(m.go())
print(m)
m.pass_kp(0)
m.pass_hh()
print(m.nowm)
