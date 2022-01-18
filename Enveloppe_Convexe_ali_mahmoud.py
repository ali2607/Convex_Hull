import turtle 
import random
import numpy as np
import time #pour la présentation

class Point:
    def __init__(self,i,j):
        self.x = i
        self.y = j
    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y

min_x = -200
max_x = 200
min_y = -200
max_y = 200



#Crée un point aléatoire dans les bornes [min_x,max_x] et [min_y,max_y]
def randpoint():
    x=random.randint(min_x,max_x)
    y=random.randint(min_y,max_y)
    return Point(x,y)

#représente le point P dans une fenetre turtle
#@param P: le point que l'on veut représenter
def drawpoint(p):
    turtle.penup()
    turtle.goto(p.x,p.y)
    turtle.dot()

#représente le polygone ayant pour sommet les point contenus dans l
#@param l: la lsite des sommets du polygone
def drawpoly(l):
    turtle.penup()
    turtle.goto(l[0].x,l[0].y)
    drawpoint(l[0])
    turtle.pendown()
    for i in range(1,len(l)):
        turtle.pendown()
        turtle.goto(l[i].x,l[i].y)
        drawpoint(l[i])
    turtle.pendown()
    turtle.goto(l[0].x,l[0].y)

#donne l'angle entre l'axe horizontal et le point p
#@param ref: le point d'origine , p: le point dont on veut savoir l'angle
#par rapport à l'axe horizontal 
def getangle(ref,p):
    turtle.goto(ref.x,ref.y)
    res=turtle.towards(p.x,p.y)
    return res


#trie l'ensemble des points par ordre trigonométrique par rapport à un point 
#de référence
#@param l:la liste des points que l'on souhaite trier p:le point de référence
def trigosort(l,p):
    a=sorted(l,key=lambda x: getangle(p,x))
    return a


#donne le déterminant de la matrice des vecteurs origine->A et origine->B
#@param A,B,origine: les 3 points formant les deux vecteurs enoncé ci-dessus                                            
def determinant(A,B,origine):
    return (A.x-origine.x)*(B.y-origine.y)-(B.x-origine.x)*(A.y-origine.y)

#determine l'ensemble des points formant l'enveloppe convexe 
#du nuage de point l 
#@param l : liste de points représentant le nuage de points étudié       
def convexehull(l):
    #trie par ordre trigo
    y=max_y
    ind=0
    for i in range(0,len(l)):
        if l[i].y < y:
            y= l[i].y
            ind=i
    p0=l[ind]
    liste_trie=trigosort(l,p0)
    
    #etude de l'enveloppe convexe grace à la liste trié
    lconvex=[p0,liste_trie[1]]
    for i in range(2,len(liste_trie)):
        while len(lconvex)>=2 and determinant(lconvex[-2],liste_trie[i],lconvex[-1])>=0 :
            del lconvex[-1]
            
        lconvex.append(liste_trie[i])    
    return lconvex

#représentation étape par étape de la construction de l'enveloppe convexe
#dans une fenetre turtle
#@param l:liste du nuage de point dont on veut determiner l'enveloppe convexe
def drawconvexehull(l):
    #trie par ordre trigo
    y=max_y
    ind=0
    for i in range(0,len(l)):
        if l[i].y < y:
            y= l[i].y
            ind=i
    p0=l[ind]
    liste_trie=trigosort(l,p0)
    
    #etude de l'enveloppe convexe grace à la liste trié
    turtle.penup()
    turtle.goto(p0.x,p0.y)
    turtle.pendown()
    lconvex=[p0,liste_trie[1]]
    turtle.goto(lconvex[1].x,lconvex[1].y)
    for i in range(2,len(liste_trie)):
        turtle.goto(liste_trie[i].x,liste_trie[i].y)
        while len(lconvex)>=2 and determinant(lconvex[-2],liste_trie[i],lconvex[-1])>=0 :
            del lconvex[-1]
            turtle.undo()
        turtle.undo()
        lconvex.append(liste_trie[i])
        turtle.goto(liste_trie[i].x,liste_trie[i].y)
    turtle.goto(p0.x,p0.y)

#trouve un couple de point antipodaux 
#(ici les points d'ordonné minimale et maximale)
#@param l:liste des sommets d'un polygone convexe
# return les indices dans l du couple de points antipodaux   
def AntipodalPair(l):
    max_y=l[0].y
    min_y=l[0].y
    indmax=0
    indmin=0
    for i in range(1,len(l)):
        if l[i].y < min_y:
            min_y= l[i].y
            indmin=i
        elif l[i].y > max_y:
            max_y=l[i].y
            indmax=i
    return indmin,indmax         

#détermine l'angle en degrée entre les points A et B
#@param A,B: deux points
def angle(A, B):
    angle1 = np.arctan2(A.y,A.x)
    angle2 = np.arctan2(B.y,B.x)
    return np.rad2deg((angle1 - angle2) % (2 * np.pi))


#trouve la prochaine paire antipodal après la paire i,j
# @param i,j : l'indice des points antipodaux actuel
# @param thetai,thetaj: l'angle entre la ligne de support et le prochain point
# i ou j 
# return les indices de la prochaine paire de points antipodal         
def NextAntipodalPair(i,j,thetai,thetaj):
    if thetai>thetaj:
        return i,j+1
    elif thetai<thetaj:
        return i+1,j
    elif thetai==thetaj:
        return i+1,j+1

#trouve le diametre de l'enveloppe convexe du nuage de point entré en parametre
#@ param l: la liste des nuages de points    
def diameter(l):
    l=convexehull(l)
    antipod=[AntipodalPair(l)]
    i=antipod[0][0]
    j=antipod[0][1]
    pi=l[i]
    pj=l[j]
    arreti=j      
    thetai=angle(l[antipod[0][0]+1],pi)  
    thetaj=angle(l[antipod[0][1]+1],pj)-180
           
    while j<len(l)-1:
        if i == arreti:
            break
        antipod.append(NextAntipodalPair(i,j,thetai,thetaj))
        if thetai>thetaj:
            thetai-=thetaj
        elif thetai<thetaj:
            thetaj-=thetai     
        i=antipod[-1][0]
        j=antipod[-1][1]
        if j == len(l)-1:
            j=0
            i+=1
    
    diam=0
    for i in range(len(antipod)):
        if np.sqrt((l[antipod[i][0]].x-l[antipod[i][1]].x)**2+(l[antipod[i][0]].y-l[antipod[i][1]].y)**2)>diam:
            diam=np.sqrt((l[antipod[i][0]].x-l[antipod[i][1]].x)**2+(l[antipod[i][0]].y-l[antipod[i][1]].y)**2)

    return diam

#represente étape par étape la procédure pour trouver le diametre
#de l'enveloppe convexe du nuage de point entré en paramètre
#@ param l: la liste des nuages de points 
def drawdiameter(l):
    l=convexehull(l)
    antipod=[AntipodalPair(l)]
    i=antipod[0][0]
    j=antipod[0][1]
    pi=l[i]
    pj=l[j]
    turtle.penup()
    turtle.goto(pi.x,pi.y)
    turtle.color("green")
    turtle.pendown()
    turtle.goto(pj.x,pj.y)
    arreti=j      
    thetai=angle(l[antipod[0][0]+1],pi)  
    thetaj=angle(l[antipod[0][1]+1],pj)-180
           
    while j<len(l)-1 :
        if i == arreti:
            break
        antipod.append(NextAntipodalPair(i,j,thetai,thetaj))
        if thetai>thetaj:
            thetai-=thetaj
        elif thetai<thetaj:
            thetaj-=thetai     
        i=antipod[-1][0]
        j=antipod[-1][1]
        if j == len(l)-1:
            j=0
            i+=1
        turtle.penup()
        turtle.goto(l[i].x,l[i].y)
        turtle.color("green")
        turtle.pendown()
        turtle.goto(l[j].x,l[j].y)
        
        
    diam=0
    for k in range(len(antipod)):
        if np.sqrt((l[antipod[k][0]].x-l[antipod[k][1]].x)**2+(l[antipod[k][0]].y-l[antipod[k][1]].y)**2)>diam:
            diam=np.sqrt((l[antipod[k][0]].x-l[antipod[k][1]].x)**2+(l[antipod[k][0]].y-l[antipod[k][1]].y)**2)
            point1=l[antipod[k][0]]
            point2=l[antipod[k][1]]
    turtle.penup()
    turtle.goto(point1.x,point1.y)
    turtle.color("red")
    turtle.pensize(3)
    turtle.pendown()
    turtle.goto(point2.x,point2.y) 
         
        
    
    
if __name__=='__main__'  :
    turtle.speed(0)
    turtle.hideturtle()
    turtle.clear()
    turtle.penup()
    
    turtle.write(" Création et étude d'Enveloppe convexe \n Par Ali Mahmoud",align='center',font=('Arial',15,'normal'))
    time.sleep(5)
    turtle.clear()
    
    '''1er PARTIE'''
    
    polygone=[]
    for i in range (0,100):
       polygone.append(randpoint())
       
    turtle.write(" 1re PARTIE \n Creation du nuage de point et trigosort",align='center',font=('Arial',15,'normal'))
    time.sleep(5)
    turtle.clear()
    
    turtle.write(" Sans Trigosort()",align='center',font=('Arial',15,'normal'))
    time.sleep(5)
    turtle.clear()
    
    for i in range(len(polygone)):
       drawpoint(polygone[i])
    drawpoly(polygone)
    
    time.sleep(5)
    turtle.clear()
    
    turtle.penup()
    turtle.setpos(0,0)
    turtle.write(" Avec Trigosort()",align='center',font=('Arial',15,'normal'))
    time.sleep(5)
    turtle.clear()
    
    p=Point(0,0)
    for i in range(len(polygone)):
       drawpoint(polygone[i])    
    l=trigosort(polygone,p)
    drawpoly(l)
    
    time.sleep(5)
    turtle.clear()
   
    '''2eme Partie'''
    turtle.penup()
    turtle.setpos(0,0)
    turtle.write("2eme PARTIE \n Creation de l'enveloppe convexe",align='center',font=('Arial',15,'normal'))
    time.sleep(5)
    turtle.clear()
      
    for i in range(len(polygone)):
       drawpoint(polygone[i])
    drawconvexehull(polygone)

    time.sleep(5)
    turtle.clear()    
    
    

    '''3eme Partie'''
    turtle.penup()
    turtle.setpos(0,0)
    turtle.write("3eme PARTIE \n Recherche du diametre du polygone",align='center',font=('Arial',15,'normal'))
    time.sleep(5)
    turtle.clear()

    for i in range(len(polygone)):
       drawpoint(polygone[i])    
    drawconvexehull(polygone)
    drawdiameter(polygone)
    
    time.sleep(5)
    turtle.clear()
    
    turtle.penup()
    turtle.color("black")
    turtle.setpos(0,0)
    turtle.write("FIN \n Je vous remercie de votre attention",align='center',font=('Arial',15,'normal'))

    turtle.Screen().exitonclick()