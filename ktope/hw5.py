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

__name__='hw5'

def hamiltonChain(connMatrix,elements):
    '''Build a hamilton chain and full list of steps for its building.
    Last element of list is result chain.'''
    
    length=len(connMatrix)
    matrix=[]
    result=[]
    s=[elements[0]]
    ind=0
    blocked={}# list of paths, that were already checked
    while len(s)!=len(elements):
        i=0
        appended=False
        ss=str(s)
        for el in connMatrix[ind]:
            if el!=0 and elements[i] not in s\
                   and (ss not in blocked or \
                        elements[i] not in blocked[ss]):
                s.append(elements[i])
                appended=True
                break
            i+=1
        if not appended:
            result.append(str(s))
            temp=s.pop()
            ss=str(s)
            if ss in blocked:
                blocked[ss].append(temp)
            else:
                blocked[ss]=[temp]
        ind=elements.index(s[-1])
    result.append(str(s))
    return result
