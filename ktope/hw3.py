# Copyright (C) 2011  Alexey Agapitov
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math

__name__='hw3'

def buildGraph(matrix,elems,rows,cols):
    """Build graph of elements using reverse placing method"""
    
    if rows*cols<len(elems):
        raise ValueError('Not enough positions for elements')
    graph=[]
    row=col=0
    graph.append([])
    # counting sum of r for each row of matrix
    ri=[]
    for r in matrix:
        sum=0
        for i in r:
            sum=sum+i
        ri.append(sum)
    # matrix of distances
    d=buildDistMatrix(rows,cols)
    # sum of distances for each row
    di=[]
    for de in d:
        sum=0
        for i in de:
            sum=sum+i
        di.append(sum)
    # sorting elements by not ascending of ri
    els=[]
    temp=list(ri)
    for i in range(len(temp)):
        max=temp[0]
        ind=0
        for r in temp:
            if r>max:
                max=r
                ind=temp.index(r)
        temp[ind]=0
        els.append(elems[ind])
    # sorting positions by not descending of di
    ps=[]
    temp=list(di)
    for i in range(len(temp)):
        min=100500
        ind=0
        for de in temp:
            if not de is None and de<min:
                min=de
                ind=temp.index(de)
        temp[ind]=None
        ps.append(ind)
    newgraph=[]
    # reserving places at graph
    for i in range(rows):
        newgraph.append([])
        for k in range(cols):
            newgraph[i].append(0)
    # setting elements to their places at graph
    for p in range(len(els)):
        i=int(ps[p]/cols);
        k=ps[p]%cols;
        newgraph[i][k]=els[p]
    dm=buildNodeDistMatrix(elems,newgraph)
    result={
        'ri':ri,
        'd':d,
        'di':di,
        'graph':newgraph,
        'es':els,
        'ps':ps,
        'dm':dm
        }
    return result

def getCoords(graph):
    """Return dict with coordonates of each element"""
    
    r=0
    coords={}
    for row in graph:
        c=0
        for el in row:
            coords[el]=(r,c)
            c=c+1
        r=r+1
    return coords

def orthogonalMetric(x1,y1,x2,y2):
    """Returns metric between to positions"""
    
    x=x1-x2
    if x<0:
        x=-x
    y=y1-y2
    if y<0:
        y=-y
    return x+y

def buildDistMatrix(rows,cols):
    """Returns matrix of distances for field of specified size"""
    
    matrix=[]
    size=rows*cols
    for r in range(size):
        matrix.append([])
        for c in range(size):
            if r==c:
                matrix[r].append(0)
                continue
            matrix[r].append(orthogonalMetric(
                int(r/cols),
                r%cols,
                int(c/cols),
                c%cols))
    return matrix

def buildNodeDistMatrix(elems,graph):
    """Returns matrix of distances for specified elems"""
    
    matrix=[]
    i=0
    coords=getCoords(graph)
    for el in elems:
        matrix.append([])
        for e in elems:
            if el==e:
                matrix[i].append(0)
                continue
            matrix[i].append(orthogonalMetric(
                coords[el][0],
                coords[el][1],
                coords[e][0],
                coords[e][1]))
        i=i+1
    return matrix

def buildWeightMatrix(connMatrix,distMatrix):
    """Returns matrix of weights and bandwidths"""
    
    if len(distMatrix)<len(connMatrix):
        raise ValueError('Not enough positions for elements')
    matrix=[]
    count=len(connMatrix)
    for i in range(count):
        matrix.append([])
        for k in range(count):
            weight=connMatrix[i][k]*distMatrix[i][k]
            if i!=k and weight==0:
                # -1 means that nodes are not connected
                matrix[i].append(-1)
            else:
                matrix[i].append(weight)
    return matrix

def buildPathMatrix(node,elems,weightMatrix):
    """Returns result matrix of Dijkstra’s algorithm"""
    
    visited=[]
    marks={}
    matrix=[]
    # initial state. mark of start node=0, others-infinity
    for el in elems:
        if el==node:
            marks[el]=0
        else:
            marks[el]=100500 #infinity
    val=0
    k=0
    while len(visited)!=len(elems):
        minW=100500
        key=node
        matrix.append([])
        # searching shortest path and filling matrix
        '''for mark in marks:
            if mark not in visited and marks[mark]<minW:
                minW=marks[mark]
                key=mark
            matrix[k].append(marks[mark])'''
        for el in elems:
            if el not in visited and marks[el]<minW:
                minW=marks[el]
                key=el
            matrix[k].append(marks[el])
        visited.append(key)
        val=minW
        # selecting neighbours
        #j=0
        ind=elems.index(key)
        for i in elems:
            j=elems.index(i)
            weight=weightMatrix[ind][j]
            if i==key:
                marks[i]=-1 # node was already marked as constant
            elif i not in visited and weight!=-1 and val+weight<marks[i]:
                marks[i]=weight+val
            #j=j+1
        k=k+1
    return matrix
