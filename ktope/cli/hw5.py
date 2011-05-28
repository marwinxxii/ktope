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

from ktope import hw2,hw5
import sys
import fileinput

__name__='hw5'

def main(file):
    lines=[]
    '''with fileinput.input(files=(file)) as f:
        for line in f:
            lines.append(line)
    '''
    finp=fileinput.input(files=(sys.argv[2]))
    for line in finp:
        lines.append(line)
    circuits=hw2.buildCircuits(lines)    
    elements=hw2.getElements(circuits)
    connMatrix=hw2.buildConnMatrix(circuits,elements)
    for line in hw5.hamiltonChain(connMatrix,elements):
        print(line)
