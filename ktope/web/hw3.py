# -*- coding: utf-8 -*-
# Copyright (C) 2011  Alexey Agapitov
#    This file is part of Ktope.
#
#    Ktope is free software: you can redistribute it and/or modify
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
from ktope import hw2,hw3
import random

class Hw3Page:
    
    header='''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>КТОПЭ ДЗ №3</title>
    <style type="text/css">
    table {
        width:100%;
        text-align:center;
    }
    .gray {
        background:#ccc;
    }
    .lightGray {
        background:#eee;
    }
    .white {
        background:#fff;
    }
    </style>
    </head>
<body>'''
    
    footer='''
    </body>
</html>'''
    
    def index(self):
        return self.header+'''
        На каждой строке файла по одной цепи, в цепи через запятую - модули.
        <form action="/hw3/result" method="GET">
        <textarea rows="30" cols="80" name="data"></textarea><br />
        Количество строк: <input type="text" name="rows" maxlength="2" />
        Столбцов: <input type="text" name="cols" maxlength="2" /><br/>
        <input type="submit" /><br />
        Нажимая на эту кнопку, вы соглашаетесь, что пользуетесь этим сервисом на свой страх и риск
        <img src="http://forum.kgn.ru/Smileys/default/trollface.png" /><br />
        исходный скрипт - marwinXXII, веб версия - Egor-kun<br />
        <a href="https://github.com/marwinxxii/ktope">Sources</a><br />
        </form>'''+self.footer
    index.exposed=True

    def result(self,data=None,rows=None,cols=None):
        if not data or not rows or not cols:
            return self.header+'''Введите <a href="/hw3">данные</a>'''+self.footer
        try:
            rows=int(rows)
            cols=int(cols)
            if rows<1 or cols<1:
                raise ValueError()
        except ValueError:
            return self.header+'''Некорректное число строк или столбцов<br/>
            <a href="javascript:history.back()">Назад</a>'''+self.footer
        circuits=hw2.buildCircuits(data.split('\n'))
        elements=set()
        html='''<b>Исходные данные</b><br /><br />'''
        for i in range(1,len(circuits)+1):
            if len(circuits[i])<=1:
                del circuits[i]
                html+='Цепь №%i пустая <br />' % i
                continue
            html+='Цепь №%i %s<br />' % (i,str(circuits[i]))
            for el in circuits[i]:
                elements.add(el)
        elements=list(elements)
        elements.sort()
        width=int(100/(len(elements)+2))
        connMatrix=hw2.buildConnMatrix(circuits,elements)
        result=hw3.buildGraph(connMatrix,elements,rows,cols)
        html+='''<br/>
        <b>Матрица соединений</b><br /><br />
        <table cellspacing="0">
        <tr class="gray">
        <td width="%i%%" class="white">&nbsp;</td>
        ''' % width
        for el in elements:
            html+='<td width="%i%%"><b>%i</b></td>' % (width,el)
        html+='<td width="%i%%"><b>r<sub>i</sub></b></td></tr>' % width
        i=0
        lgray=False
        for row in connMatrix:
            if lgray:
                html+='<tr class="lightGray">\n'
            else:
                html+='<tr>\n'
            html+='<td class="gray"><b>%i</b></td>\n' % elements[i]
            k=0
            for val in row:
                if k==i:
                    html+='<td><b>%i</b></td>\n' % val
                else:
                    html+='<td>%i</td>\n' % val
                k+=1
            html+='<td><b>%i</b></td></tr>\n' % result['ri'][i]
            i+=1
            lgray=not lgray
        html+='''</table><br/><br/>'''
        width=int(100/(len(result['d'])+2))
        html+='''<b>Матрица расстояний</b><br/><br/>
        <table cellspacing="0">
        <tr class="gray">
        <td width="%i%%" class="white">&nbsp;</td>
        ''' % width
        for el in range(len(result['d'])):
            html+='<td width="%i%%"><b>%i</b></td>\n' % (width,el+1)
        html+='<td width="%i%%"><b>d<sub>i</sub></b></td>\n</tr>\n' % width
        lgray=False
        i=0
        for row in result['d']:
            if lgray:
                html+='<tr class="lightGray">\n'
            else:
                html+='<tr>\n'
            html+='<td class="gray"><b>%i</b></td>\n' % (i+1)
            k=0
            for val in row:
                if k==i:
                    html+='<td><b>%i</b></td>\n' % val
                else:
                    html+='<td>%i</td>\n' % val
                k+=1
            html+='<td><b>%i</b></td>\n</tr>\n' % result['di'][i]
            i+=1
            lgray=not lgray
        html+='''</table>\n<br/><br/>'''
        width=int(100/(len(elements)+1))
        html+='''<b>Упорядоченные элементы и позиции</b><br/><br/>
        <table cellspacing="0">
        <tr class="lightGray">
        <td width="%i%%" class="gray"><b>l<sub>i</sub></b></td>
        ''' % width
        for el in result['es']:
            html+='<td width="%i%%">%i</td>\n' % (width,el)
        html+='''</tr>\n</table>\n<br/>'''
        width=int(100/(len(result['ps'])+1))
        html+='''<table cellspacing="0">
        <tr class="lightGray"><td class="gray"><b>p<sub>i</sub></b></td>
        '''
        for p in result['ps']:
            html+='<td>%i</td>\n' % (p+1)
        html+='''</tr>
        </table><br/>
        <b>Расположение элементов</b><br/><br/>
        <table cellspacing="0" border="1">'''
        width=int(100/cols)
        for row in result['graph']:
            html+='<tr>'
            for el in row:
                html+='<td width="%i%%">' % width
                if el==0:
                    html+='&nbsp;'
                else:
                    html+=str(el)
                html+='</td>\n'
            html+='</tr>\n'
        html+='</table>\n<br/>'#F(p)='+str(result['f'])
        width=int(100/(len(elements)+1))
        html+='''<b>Матрица расстояний между вершинами</b><br /><br />
        <table cellspacing="0">
        <tr class="gray">
        <td width="%i%%" class="white">&nbsp;</td>
        ''' % width
        for el in elements:
            html+='<td width="%i%%"><b>%i</b></td>\n' % (width,el)
        i=0
        html+='</tr>\n'
        lgray=False
        for row in result['dm']:
            if lgray:
                html+='<tr class="lightGray">\n'
            else:
                html+='<tr>\n'
            html+='<td class="gray"><b>%i</b></td>\n' % elements[i]
            k=0
            for val in row:
                if k==i:
                    html+='<td><b>%i</b></td>\n' % val
                else:
                    html+='<td>%i</td>\n' % val
                k+=1
            i+=1
            lgray=not lgray
            html+='</tr>\n'
        html+='''</table>
        <br /><br />
        <b>Матрица весов и пропускных способностей</b><br/><br/>
        <table cellspacing="0" border="1">
        <tr class="gray">
        <td width="%i%%" class="white">&nbsp;</td>
        ''' % width
        for el in elements:
            html+='<td width="%i%%"><b>%i</b></td>\n' % (width,el)
        html+='</tr>'
        weightMatrix=hw3.buildWeightMatrix(connMatrix,result['dm'])
        lgray=False
        i=0
        for row in weightMatrix:
            if lgray:
                html+='<tr class="lightGray">\n'
            else:
                html+='<tr>\n'
            html+='<td class="gray"><b>%i</b></td>\n' % elements[i]
            k=0
            for val in row:
                if k==i:
                    html+='<td><b>%i</b></td>\n' % val
                elif val!=-1:
                    html+='<td>%i</td>\n' % val
                else:
                    html+='<td>&nbsp;</td>\n'
                k+=1
            i+=1
            lgray=not lgray
            html+='</tr>\n'
        html+='''</table>
        <br/><br/>
        <b>Алгоритм Дейкстры</b><br/><br/>
        Исходная вершина: l<sub>%i</sub>
        <br/><br/>''' % result['graph'][0][0]
        # choosing left-upper node
        pathMatrix=hw3.buildPathMatrix(result['graph'][0][0],elements,weightMatrix)
        lGray=False
        html+='''
        <table cellspacing="0">
        <tr class="gray">
        <td class="white">&nbsp;</td>'''
        for i in range(len(pathMatrix)):
            html+='<td width="%i%%"><b>%i</b></td>' % (width,i+1)
        html+='</tr>\n'
        for i in range(len(pathMatrix)):
            if lgray:
                html+='<tr class="lightGray">'
            else:
                html+='<tr>'
            html+='<td width="%i%%" class="gray"><b>x%i</b></td>' % (width,elements[i])
            for k in range(len(pathMatrix)):
                html+='<td>'
                if pathMatrix[k][i]==100500:
                    html+='∞'
                elif pathMatrix[k][i]==-1:
                    html+='&nbsp;'
                else:
                    html+=str(pathMatrix[k][i])
                html+='</td>\n'
            html+='</tr>\n'
            lgray=not lgray
        html+='''</table>\n'''
        return self.header+html+self.footer
    result.exposed=True
