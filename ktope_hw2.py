#Copyright (C) 2011  Alexey Agapitov
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import collections

__name__='ktope_hw2'

def buildCircuits(lines):
    """Iterate over lines and build dict of circuits"""
    
    #dict because we need to store numbers of circuits
    circuits={}
    i=1
    for line in lines:
        if line=='':
            continue
        #using set to avoid duplicate elements
        circuit=set()
        for element in line.split(','):
            el=int(element)
            circuit.add(el)
        #circuits[i]=circuit
        circuits[i]=list(circuit)
        i+=1
    return circuits

def buildComplexMatrix(circuits,elements):
    """build complex matrix of circuits"""
    
    matrix=[]
    for elem in elements:
        temp=[]
        for c in circuits:
            if elem in circuits[c]:
                temp.append(1)
            else:
                temp.append(0)
        matrix.append(temp)
    return matrix

def buildConnMatrix(circuits,elements):
    """Build connections matrix"""
    
    matrix=[]
    for elem in elements:
        temp=[]
        for el in elements:
            s=0
            if el!=elem:
                for cir in circuits:
                    if elem in circuits[cir] and el in circuits[cir]:
                        s+=1
            temp.append(s)
        matrix.append(temp)
    return matrix

def buildGraph(matrix,elements):
    """Build graph from connections matrix"""
    
    i=0
    graph={}
    for row in matrix:
        graph[elements[i]]=[]
        k=-1
        for el in row:
            k+=1
            if el==0:
                continue
            graph[elements[i]].append(elements[k])
        i+=1
    return graph

def sortGraph(graph):
    """Sort graph by not descending of nodes(amount of connected to node nodes)"""

    #returns new OrderedDict
    sorted=collections.OrderedDict()
    length=len(graph)
    #nodes which are not in sorted
    keys=list(graph.keys())
    while len(sorted)!=length:
        maxlen=-1
        maxind=0
        for key in keys:
            if len(graph[key])>maxlen:
                maxlen=len(graph[key])
                maxind=key
        sorted[maxind]=graph[maxind]
        keys.remove(maxind)
    return sorted

def colorGraph(graph):
    """Colorise given graph"""
    
    j=1
    colored={}
    sorted=graph
    while len(sorted)!=0:
        colored[j]=[]
        sorted=sortGraph(sorted)
        (node,nodes)=sorted.popitem(False)
        colored[j].append(node)
        #coloring nodes
        for nod in sorted:
            if node in sorted[nod] and nod not in nodes:
                print('bullshit',node,nod)
                exit()
            if nod in nodes and node not in sorted[nod]:
                print('bullshit2',node,nod)
                exit()
            add=True
            #check that nodes colored on this iteration not connected to nod
            for n in colored[j]:
                if n in sorted[nod]:
                    add=False
                    break
            if add:
                colored[j].append(nod)
            #if node not in sorted[nod]:
            #    colored[j].append(nod)
        for key in colored[j]:
            #deleting node
            if key!=node:
                del sorted[key]
            #deleting all connections to this node
            for nod in sorted:
                if key in sorted[nod]:
                    sorted[nod].remove(key)
        j+=1
    return colored
