# -*- coding: utf-8 -*-
"""
take the position file from Zeiss, simulate for the tile scan
and write the coordinates and write into a position file 

@author: boris
"""

"""the important variables
========================================================"""
dire = "C:/ZEN/"
posFileName = "C:/ZEN/07-25-2019_relative.pos"
#tileSize=340.1
tileSize=490
tileDilate=1
m = 120
"""m is the maximum number of position will be written into the file"""

RelativePositions = 0 #for absolute position file
RelativePositions = 1 #for relative position file

positionFileStyle = 1

"""====================================================="""
"""start to read the position file"""
text_file = open(posFileName,"r")
lines = text_file.readlines()
print(len(lines))
print(lines)
x=[]
y=[]
z=[]
"""here I assume the z is the same everywhere"""
import re
for line in lines:
    if '\t\tX' in line:
        s=re.findall('-?\d*\.?\d+', line)
        x.append(float(s[0]))
    elif '\t\tY' in line:
        s=re.findall('-?\d*\.?\d+', line)
        y.append(float(s[0]))
    elif '\t\tZ' in line:
        s=re.findall('-?\d*\.?\d+', line)
        z.append(float(s[0]))
    else:
        continue
    
text_file.close()

"""start to simulate tileScan"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.path as mpltPath
import numpy as np
from scipy.spatial import ConvexHull

"""
draw polygon with input coordinates
coord here is a list
"""
"""combine x and y"""
xyz= list(zip(x,y,z)) 

def drawTile(centralpoint,tilesize):
    """central point =[x,y]
    """
    [xs,ys] = centralpoint
    minx = xs-0.5*tilesize
    maxx = xs+0.5*tilesize
    miny = ys-0.5*tilesize
    maxy = ys+0.5*tilesize
    xr = (minx, minx,maxx,maxx,minx)
    yr = (miny,maxy,maxy,miny,miny)
    vertice =[]
    for i in range(4):
        vertice.append([xr[i],yr[i]])
    #plt.figure()
    #plt.plot(xr,yr,dashes=[2, 2],color='#f92874')
    #plt.show()
    return (vertice)#vertice
#t = drawTile([1,2],3)
#y1=y[1]

"""make a function to create tiles 
and excludes out the ones outside the polygon
1> one input is a list of coordinates that define the polygon
2> the other input is the tile size
"""
def TriPntDefSurface(points):
    """take in a list of 3 points (x,y,z)
    three points define a surface
    """
    p1 = np.array(points[0])
    p2 = np.array(points[1])
    p3 = np.array(points[2])
    # These two vectors are in the plane
    v1 = p3-p1
    v2 = p2-p1
    # the cross product is a vector normal to the plane
    cp = np.cross(v1, v2)
    a, b, c = cp
    # This evaluates a * x3 + b * y3 + c * z3 which equals d
    #p1, p2 or p3 could be used to calculate d
    d = np.dot(cp, p2)
    #print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))
    # z = (d-a*x-b*y)/c
    return (a,b,c,d)

#tri3 = [[1,2,3],[2,4,4],[5,6,2]]
#TriPntDefSurface(tri3)

def findzInSurf(x,y,TriPoints):
    """x,y is from a dot on a surface determined by three points (x,y,z).
    z will be calculated
    """
    a,b,c,d= TriPntDefSurface(TriPoints)
    z= (d-a*x-b*y)/c
    return z
#findzInSurf(0,0,tri3)
    
def findzInLine(x,y, BiPoints):
    """x,y is from a dot on a line determined by two points (x,y,z).
    if x,y is in the line, then z will be calculated
    return the boolean and z value (boolean, z)
    """
    p1 = np.array(BiPoints[0])
    p2 = np.array(BiPoints[1])
    #check if (x,y) is on the line
    a_xy= (p2[1]-p1[1])/(p2[0]-p1[0])
    b_xy = p1[1]-a_xy*p1[0]
    if y==x*a_xy+b_xy:
        #This evaluates a * x + b =z
        a_xz=(p2[2]-p1[2])/(p2[0]-p1[0])
        b_xz = p1[2]-a_xz*p1[0]
        #print('the equation is {0}x+{1}=z'.format(a_xz,b_xz))
        z=a_xz*x+b_xz
        boo = True
        return (boo,z)
    else:
        print("the point is not on the line")
        boo =False
        z = np.nan
    return (boo,z)
    
#two2 = [[1,2,3],[2,6,6]]
#findzInLine(3,10,two2)
    
    
    
def makeTilesExcludeOut(coord,tileSize):
    coord.append(coord[0])
    """coord is a list of x,y,z"""
    #repeat the first point to create a 'closed loop'
    xs, ys, zs = zip(*coord) #create lists of x and y values
    """
    xmin xmax ymin ymax are the coordinate values for the rectangle
    """
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
    lenx=xmax-xmin
    leny=ymax-ymin
    print("how are you")
    print("the smallest rectagle to contains all the tiles: length/width "+ str(lenx) +" "+str(leny))
    xr = (xmin, xmin,xmax,xmax,xmin)
    yr = (ymin,ymax,ymax,ymin,ymin)
    fig, ax = plt.subplots()
    #ax = fig.gca(projection="3d")
    #ax = fig.add_subplot(111, projection='3d')
    # Using set_dashes() to modify dashing of an existing line
    line1, = ax.plot(xs, ys, 'ro',label='polygon')
    #line1.set_dashes([2, 2, 10, 2]) 
    # 2pt line, 2pt break, 10pt line, 2pt break
    # Using plot(..., dashes=...) to set the dashing when creating a line
    line2, = ax.plot(xr, yr, color='#f16824',dashes=[6, 2], label='minRectCover')
    """get the convext hull vertices"""
    coord.pop()                 
    xyz_narray = np.asarray(coord)
    xynarray = xyz_narray[:,range(2)]
    hull = ConvexHull(xynarray)
    indV=hull.vertices
    """this is a numpy array of indices of points forming the vertices of the convex hull.
    be very careful about numpy array
    """
    indVclose =np.append(indV,[indV[0]], axis=0)
    """convert numpy array to a list"""
    coordConvexH=xynarray[indVclose].tolist()
    plt.plot(xyz_narray[indVclose,0], xyz_narray[indVclose,1], 'ko')
    plt.plot(xyz_narray[indVclose,0], xyz_narray[indVclose,1], 'r--', lw=2)
    
    x_n = int((xmax-xmin)/tileSize+1)
    y_n = int((ymax-ymin)/tileSize+1)
    xy_n = x_n*y_n
    x_n = int((xmax-xmin)/tileSize+1)
    y_n = int((ymax-ymin)/tileSize+1)
    xy_n = x_n*y_n  
    tilelist =[]#all the tiles. central coordinates (x,y)
    tileInsideVlist=[]#all the tiles inside
    tileInsideList=[]
    for i in range(x_n):
        for j in range (y_n):
            tilelist.append([(0.5+i)*tileSize+xmin,(0.5+j)*tileSize+ymin])
    """
    divide the surface into several triangles
    """
    polygonVertices = xyz_narray[indV].tolist()
    triV=[]
    triaVList =[]#contains the coordinate of (x,y,z)
    triV_xy=[]
    triaVList_xy=[]#contains the coordinate of (x,y)
    """find the lines between the triangels
    """
    lineV = []
    lineVlist = []#contains the coordinates of (x,y)
    for i in range(len(indV)-2):
        
        triV.append([polygonVertices[0][0],polygonVertices[0][1],polygonVertices[0][2]])
        triV.append([polygonVertices[i+1][0],polygonVertices[i+1][1],polygonVertices[i+1][2]])
        triV.append([polygonVertices[i+2][0],polygonVertices[i+2][1],polygonVertices[i+2][2]])
        triaVList.append(triV)
        triV=[]
        triV_xy.append([polygonVertices[0][0],polygonVertices[0][1]])
        triV_xy.append([polygonVertices[i+1][0],polygonVertices[i+1][1]])
        triV_xy.append([polygonVertices[i+2][0],polygonVertices[i+2][1]])
        triaVList_xy.append(triV_xy)
        triV_xy=[]
        lineV.append([polygonVertices[0][0],polygonVertices[0][1],polygonVertices[0][2]])
        lineV.append([polygonVertices[i+2][0],polygonVertices[i+2][1],polygonVertices[i+2][2]])
        lineVlist.append(lineV)
        lineV = []
    
    
    #coordConvexH.remove(coordConvexH[-1])
    coordConvexH.pop()
    path = mpltPath.Path(coordConvexH)# input is a list of (x,y)
    """calculate the central coordinates of tiles within a rectangle
    defined by four vertice and exclude those fall out of the polygon
    """

    for i in range(xy_n):
        st= drawTile(tilelist[i],tileSize)#st is a list of (x,y)
        inside = path.contains_points(st)
        if False in inside:
            continue
        else:
            tileInsideVlist.append(st)
            tileInsideList.append(tilelist[i])

    """
    time to calculate z
    """
    zc=[]
    """++++++++++++++++++++++++++++++
   The break statement, like in C, 
   breaks out of the innermost enclosing for or while loop.
   +++++++++++++++++++++++++++++++++++"""
    for i in range(len(tileInsideList)):
        xc,yc=zip(*tileInsideList)
        #print(''.join(['begin to check tile point_',str(i+1)]))
        inside1=False
        j=0        
        while(inside1==False & j<len(triaVList_xy)):
            path1 = mpltPath.Path(triaVList_xy[j])
            inside1= path1.contains_point(tileInsideList[i])
            if inside1 == True:
                zc.append(findzInSurf(xc[i],yc[i],triaVList[j]))
                j=0
                break
            else:
                j+=1
        """check if the central point of the tile inside the triangle
        """
            
        for z in range(len(lineVlist)):
            if inside1== True:
                break
            else:
                boo1, z1 = findzInLine(xc[i],yc[i], lineVlist[z])#return (boo,z)
                if boo1 == True:
                    print("find the point on the line")
                    zc.append(z1)
                    break
                else:
                    continue
         
        xs,ys=zip(*tileInsideVlist[i])
        xs=list(xs)
        xs.append(xs[0])#make a close drawing
        ys=list(ys)
        ys.append(ys[0])#make a close drawing
        line1,= ax.plot(xs,ys,color='blue')
    
    line1,=ax.plot(xc,yc,'go')
    tileNewList=list(zip(xc,yc,zc))
    
    ax.legend()
    plt.savefig('plane.png')
    plt.show()
    return (len(tileNewList),tileNewList)

NumOfTiles, xyz_Tile = makeTilesExcludeOut(xyz,tileSize*tileDilate)
print("number of tiles = ",NumOfTiles)

"""plot the tile dot in 3d"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xt,yt,zt =zip(*xyz_Tile)
ax.plot(xt,yt,zt, color='r', linestyle=' ', marker='o')
#ax.set_zlim3d(30,400)
ax.view_init(10, 70)#adjust the elevation and azimuth
plt.tight_layout()
plt.savefig('tileCenter3d.png')
plt.show()
"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
calculate z positions of points if the surface is 100% horizontal
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

    

"""start to write the position file"""
"""+++create x,y,z lists for tiles+++++"""
#xt,yt,zt =zip(*xyz_Tile)

"""m is the maximum number of position will be written into the file
   n is the numbers of position files
   x is the xth position file
   
"""
"""delete the old position files
"""
import os

for filename in os.listdir(dire):
    #print(filename)
    if "tilePos-" in filename and ".pos" in filename:
        #print("Deleting old file \"{}\"".format(filename))
        os.remove(dire+filename)
        
def writeFile(x, m, n, NumOfTiles, dire, positionFileStyle):
    filename =''.join(['tilePos-',str(x),'.pos'])
    if(n==1):
        NumT = NumOfTiles
    elif (x<n):
        NumT = m
    elif(x==n):
        NumT = NumOfTiles%m
    else:
        NumT = 0
    
    #write_file = open(''.join(['C:/ZEN/',filename]),"w")
    write_file = open(''.join([dire,filename]),"w")
    write_file.write('Carl Zeiss LSM 510 - Position list file - Version = 1.000\n')
    write_file.write('BEGIN PositionList Version = 10001\n')
    
    write_file.write('\tBEGIN  10001\n')
    write_file.write(''.join(['\t\tRelativePositions = ',str(positionFileStyle),'\n']))
    write_file.write('\t\tReferenceX = 0.000 µm\n')
    write_file.write('\t\tReferenceY = 0.000 µm\n')
    write_file.write('\t\tReferenceZ = -0.000 µm\n')
    write_file.write('\tEND\n')
    
    """
    write in the numbers of positions
    """
    #write_file.write()
    write_file.write(''.join(['\tNumberPositions = ',str(NumT),'\n']))
    
    """
    
    """
    print("#"+str(x)+"file contains "+str(NumT)+" tiles")
    
    for i in range(NumT):
        positionIndex=i+1
        
        if (n==1):
            DataIndex = i 
        else:
            DataIndex = i+m*(x-1)
        write_file.write(''.join(['\tBEGIN Position',str(positionIndex),' Version = 10001\n']))
        write_file.write(''.join(['\t\tX = ',str(round(xt[DataIndex],3)),' µm\n']))
        write_file.write(''.join(['\t\tY = ',str(round(yt[DataIndex],3)),' µm\n']))
        write_file.write(''.join(['\t\tZ = ',str(round(zt[DataIndex],3)),' µm\n']))
        write_file.write('\tEND\n')
        
    write_file.write('END\n')
    write_file.close()
    return

n= NumOfTiles//m
rem = NumOfTiles//m
if (rem>0):
    NumOfPosF= n+1
else:
    NumOfPosF = n
for j in range(NumOfPosF):
    writeFile(j+1, m, NumOfPosF, NumOfTiles, dire, positionFileStyle)
    
print("numberOfPositionFiles = "+str(NumOfPosF))
    
