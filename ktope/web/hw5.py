# -*- coding: utf-8 -*-
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

from ktope import hw2,hw5

class Hw5Page:
    header='''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>КТОПЭ ДЗ №5</title>
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

    footer='</body></html>'

    def index(self):
        return self.header+'''
        На каждой строке файла по одной цепи, в цепи через запятую - модули.
        <form action="/hw5/result" method="GET">
        <textarea rows="30" cols="80" name="data"></textarea><br />
        <input type="submit" /><br />
        Нажимая на эту кнопку, вы соглашаетесь, что пользуетесь этим сервисом на свой страх и риск
        <img src="http://forum.kgn.ru/Smileys/default/trollface.png" /><br />
        исходный скрипт - marwinXXII, веб версия - Egor-kun<br />
        <a href="https://github.com/marwinxxii/ktope">Sources</a><br />
        </form>'''+self.footer
    index.exposed=True

    def result(self,data=None):
        if not data:
            return self.header+'''Введите <a href="/hw5">данные</a>'''+self.footer
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
        matrix1=hw2.buildComplexMatrix(circuits,elements)
        width=int(100/(len(circuits)+1))
        html+='''<br />
        <b>Матрица комплексов</b><br /><br />
        <table cellspacing="0">
        <tr class="gray">
            <td width="%i%%" class="white">&nbsp;</td>
            ''' % width
        for key in circuits:
            html+='<td width="%i%%"><b>%i</b></td>\n' % (width,key)
        html+='</tr>\n'
        lgray=False
        i=0
        for row in matrix1:
            if lgray:
                html+='<tr class="lightGray">\n'
            else:
                html+='<tr>\n'
            html+='<td class="gray"><b>%i</b></td>\n' % elements[i]
            for el in row:
                if el==0:
                    html+='<td>%i</td>\n' % el
                else:
                    html+='<td><b>%i</b></td>\n' % el
            html+='</tr>\n'
            i+=1
            lgray=not lgray
        width=int(100/(len(elements)+1))
        matrix2=hw2.buildConnMatrix(circuits,elements)
        html+='''</table><br />
        <b>Матрица соединений</b><br /><br />
        <table cellspacing="0">
        <tr class="gray">
        <td width="%i%%" class="white">&nbsp;</td>
        ''' % width
        for el in elements:
            html+='<td width="%i%%"><b>%i</b></td>\n' % (width,el)
        html+='</tr>\n'
        i=0
        lgray=False
        for row in matrix2:
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
            html+='</tr>\n'
            i+=1
            lgray=not lgray
        html+='''</table><br /><br />
        <b>Гамильтонов цикл</b><br/><br/>'''
        for line in hw5.hamiltonChain(matrix2,elements):
            html+=line+'<br/>'
        return self.header+html+self.footer

    result.exposed=True
