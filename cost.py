import matplotlib.path as mpath
import matplotlib.patches as mpatches

def Paint(ax):        
    
    Path = mpath.Path
    path_data = [
        (Path.MOVETO, (311.8,-16.3)),
        (Path.LINETO, (288.2,-16.3)),
        (Path.LINETO, (280.9, 6.2)),
        (Path.LINETO, (300,20.1)),
        (Path.LINETO, (319.1,6.2)),
        (Path.CLOSEPOLY, (311.8,-16.3)),
        ]
    codes, verts = zip(*path_data)
    path = mpath.Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)
    ax.add_patch(patch)
    ax.axis('equal')



points =((311.8,-16.3), (288.2,-16.3), (280.9, 6.2), (300,20.1),(319.1,6.2))







def Paint_Q(List, VV, sizes, N, ax):
    Vx= VV[:N]
    Vy= VV[N:]
    for i in List:
        Paint_q(Vx[i],Vy[i],sizes[i], ax)
    

def Paint_q(vx,vy,s, ax):
    Path = mpath.Path
    #print(vx,vy)
    path_data = [
        (Path.MOVETO, (vx, vy)),
        (Path.LINETO, (vx, vy+s[1])),
        (Path.LINETO, (vx+s[0], vy+s[1])),
        (Path.LINETO, (vx+s[0], vy)),
        (Path.LINETO, (vx, vy)),
        (Path.CLOSEPOLY, (vx, vy)),
        ]
    codes, verts = zip(*path_data)
    path = mpath.Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor='b', alpha=0.5)
    ax.add_patch(patch)
    ax.axis('equal')







import math
import random
import numpy as np
def Into(P):
    distances = [math.sqrt((x-P[0])**2+ (y-P[1])**2) for (x,y) in points]
    num = list(zip(distances, range(len(distances))))
    num.sort()
    (x,y) =(num[0][1], num[1][1])
    #print(x,y, P)
    if P[1]<-16.3 or P[1]>319.1:
        return False
      
    if (x,y)==(1,2) or (x,y)==(2,1):
        x1= -P[1]/3.08219 +871.9876/3.08219
        if P[0]<x1:
            return False
    elif (x,y)==(2,3) or (x,y)==(3,2):
        x1= (P[1]+378609/1910)* 191/139
        if P[0]<x1:
            return False
    
    elif (x,y)==(3,4) or (x,y)==(4,3):
        x1= (P[1]-455391/1910)* (-191/139)
        if P[0]>x1:
            return False
        
    elif (x,y)== (4,0) or (x,y)==(0,4):
        x1= (P[1]+713449/730)* (73/225)
        if P[0]>x1 or P[0]<-16.3:
            return False
    elif (x,y)==(0,1) or (y,x)==(1,0) and P[0]<-16.3:
        return False
         
    else:
        return True
    return True


def Fitness(VV, sizes, N):
    Vx= VV[:N]
    Vy= VV[N:]
    index= []
    for i, vx, vy in zip(range(N), Vx, Vy):
        V= [vx, vy]
        #print(V)
        if Into(V)==True:
            p = sizes[i]
            one= [V[0]+p[0], V[1]]
            second= [V[0], V[1]+p[1]]
            third=[V[0]+p[0], V[1]+p[1]]
            c=0
            
            for v in [one, second, third]:
                if Into(v)== False:
                    break
                else:
                    c+=1
            if c==3:
                index.append(i)
       
    
    F= Inter(Vx, Vy, index, sizes)
    a= Area(F, sizes)
    #print(a)
    return a, F
    
    
    
def Area(List, sizes):
   A= [sizes[i][0]*sizes[i][1] for i in List]
   return sum(A)



def Inter(Vx, Vy, index, sizes):
    X=[(Vx[i],i) for i in index]+[(Vx[i]+sizes[i][0],i) for i in index]
    X.sort()
    L= np.array(X)[:,1]
    L_ind= set(range(len(L)))
    no_val=[]
    Total = []
    for i in range(len(L)):
        if i in L_ind and not( L[i] in no_val):
            
            l=L[i]
            j=i+1
            while  L[j]!=l:
                j+=1
            L_ind= L_ind-set([j])
            
            """
            if not( L[i] in no_val):
                f= int(L[i])
                index_y= list(map(int, list(set(L[i+1:j]))))
                print(i, L[i], index_y)
                F = InterY(f, index_y,Vy, sizes)
                if F==[]:
                    Total.append(L[i])
                else:
                    no_val.extend(F)
            """
            f= int(L[i])
            index_y= list(map(int, list(set(L[i+1:j]))))
            F = InterY(f, index_y,Vy, sizes)
            if F==[]:
                Total.append(L[i])
            else:
                no_val.extend(F)
           
    return list(map(int,Total))
            
            
            

def InterY(f, index_y,Vy, sizes):
    if index_y==[]:
        return []
    index_y.append(f)
    Y = [(Vy[k],k) for k in index_y]+[(Vy[k]+sizes[k][1],k) for k in index_y]
    Y.sort()
    
    L_y= [y[1] for y in Y]
    lim1 = L_y.index(f)
    lim2=  L_y[lim1+1:].index(f)+lim1+1
    J=  L_y[lim1+1: lim2]
    if J==[] and lim1>1:
       K=[]
       for h in L_y[:lim1]:
            lim1 = L_y.index(h)
            lim2=  L_y[lim1+1:].index(h)+lim1+1
            if f in L_y[lim1+1: lim2]:
                K.append(h)
       return K
    else:
        return  L_y[lim1+1: lim2]
        
                
                
          
          
          
          
          
          
          

    
    def animate(i):
        global dd
        dd=i
        time.sleep(0.1)
        redDot.set_data(x[i], y[i])
        return redDot,
    
    
    def Ref(elements, best, sizes, Nitem):
        fig, ax = plt.subplots()
        cost.Paint(ax)
        cost.Paint_Q( elements, best, sizes, Nitem, ax)
    fig, ax = plt.subplots()
    ax.set_xlabel("$f_1$", size= 20)
    ax.set_ylabel("$f_2$", size= 20)
   
    #print(i)
    
    redDot, = Ref(elements, best, sizes, Nitem)
    myAnimation = FuncAnimation(fig, animate, frames=np.arange(0, len(x), 1), \
                                      interval=1, blit=True, repeat=True)
    

    writer = PillowWriter(fps=5)  
    myAnimation.save("demo_sine.gif", writer=writer) 
    plt.show()
                
    
    

     
def Animacion(XY):
    from matplotlib import rcParams
    from matplotlib.animation import FuncAnimation, PillowWriter  
    import time
    ## make sure the full paths for ImageMagick and ffmpeg are configured
    rcParams['animation.convert_path'] = r'C:\Program Files\ImageMagick\convert'
    rcParams['animation.ffmpeg_path'] = r'C:\Program Files\ffmpeg\bin\ffmpeg.exe'


    x= [ [ c[0] for c in xy] for xy in XY ]
    y= [ [ c[1] for c in xy] for xy in XY ]
   
    
    def animate(i):
        global dd
        dd=i
        time.sleep(0.1)
        redDot.set_data(x[i], y[i])
        return redDot,
    
    

    fig, ax = plt.subplots()
    ax.set_xlabel("$f_1$", size= 20)
    ax.set_ylabel("$f_2$", size= 20)
   
    #print(i)
    ax = plt.axis([0,1.05,0,1.05])
    redDot, = plt.plot([0], [0], 'o', c='r')
    myAnimation = FuncAnimation(fig, animate, frames=np.arange(0, len(x), 1), \
                                      interval=1, blit=True, repeat=True)
    

    writer = PillowWriter(fps=5)  
    myAnimation.save("demo_sine.gif", writer=writer) 
    plt.show()


    
"""
N = 20
sizes = [[random.randrange(1, 6),random.randrange(1,6)] for _ in range(N)]
Vx = [random.uniform(280.9, 319.1) for _ in range(N)] 
Vy = [random.uniform(-16.3, 20.1) for _ in range(N)]
VV= Vx+Vy
Cost(VV, sizes, N)
"""
    
