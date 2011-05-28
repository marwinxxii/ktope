# Copyright (C) 2011  Alexey Agapitov
#    This file is part of Ktope.
#
#    Ktope is free software: you can redistribute it and/or modify
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

def eulerCycle(g):
    st=[]
    st.append(0)
    res=[]
    size=len(g)
    while len(st)!=0:
        v=st[-1]
        i=0
        for k in range(size):
            if g[v][i]!=0:
                break
            i+=1
        if i==size:
            res.append(v+1)
            st.pop()
        else:
            g[v][i]-=1
            g[i][v]-=1
            st.append(i)
    return res

import sys

conf=None
if len(sys.argv)==1:
    print('Please specify command to execute')
    exit()
if sys.argv[1].startswith('web'):
    import cherrypy
    import os.path
    conf = os.path.join(os.path.dirname(__file__), 'cherrypy.conf')
    from ktope.web import hw2,hw3,hw5,main
if sys.argv[1]=='web':
    cherrypy.tree.mount(hw2.Hw2Page(), '/hw2', config=conf)
    cherrypy.tree.mount(hw3.Hw3Page(), '/hw3', config=conf)
    cherrypy.tree.mount(hw5.Hw5Page(), '/hw5', config=conf)
    cherrypy.quickstart(main.KtoPage(), config=conf)
elif sys.argv[1]=='web.hw2':
    cherrypy.quickstart(hw2.Hw2Page(), '/', config=conf)
elif sys.argv[1]=='web.hw3':
    cherrypy.quickstart(hw3.Hw3Page(), '/', config=conf)
elif sys.argv[1]=='web.hw5':
    cherrypy.quickstart(hw5.Hw5Page(), '/', config=conf)
elif sys.argv[1]=='cli.hw5':
    if len(sys.argv)<2:
        print('Please specify a file with circuits')
        exit()
    from ktope.cli import hw5
    hw5.main(sys.argv[2])
elif sys.argv[1]=='euler':
    if len(sys.argv)<2:
        print('Please specify a file with circuits')
        exit()
    from ktope import hw2
    import fileinput
    lines=[]
    #only for python >=3.2
    '''with fileinput.input(files=(sys.argv[2])) as f:
        for line in f:
            lines.append(line)
    '''
    finp=fileinput.input(files=(sys.argv[2]))
    for line in finp:
        lines.append(line)
    finp.close()
    circuits=hw2.buildCircuits(lines)
    elements=hw2.getElements(circuits)
    connMatrix=hw2.buildConnMatrix(circuits,elements)
    print(eulerCycle(connMatrix))
