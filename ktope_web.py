# -*- coding: utf-8 -*-
import cherrypy
import ktope_hw2
import random

class KtoPage:
    
    header='''
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Скачать КТОПЭ БЕсПЛАНО БЕЗ СМС БЕЗ РЕГиСТРАЦИИ!!1</title>
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
    .lime {
        background:#3BFC01;
    }
    .pink {
        background:#FB0079;
    }
    .blue {
        background:#00FFD2;
    }
    .violet {
        background:#6B0088;
    }
    .yellow {
        background:#EDFC08;
    }
    .carrot {
        background:#E98400;
    }
    </style>
    </head>
<body>'''
    
    footer='''
    </body>
</html>'''
    
    funnyColors=['lime','pink','blue','violet','yellow','carrot']

    def index(self):
        return self.header+'''
        На каждой строке файла по одной цепи, в цепи через запятую - модули.
        <form action="/result" method="GET">
        <textarea rows="30" cols="80" name="data"></textarea><br />
        Не скучные цвета <input type="checkbox" name="boring" /><br />
        <input type="submit" /><br />
        Нажимая на эту кнопку, вы соглашаетесь, что пользуетесь этим сервисом на свой страх и риск
        <img src="http://forum.kgn.ru/Smileys/default/trollface.png" /><br />
        исходный скрипт - marwinXXII, веб версия - Egor-kun<br />
        <a href="https://github.com/marwinxxii/ktope-hw2/">Sources</a><br />
        <a href="http://rospil.info/donate">Donate :)</a>
        </form>'''+self.footer
    index.exposed=True

    def result(self,data=None,boring=None):
        if not data:
            return self.header+'''Введите <a href="/ktope">данные</a>'''+self.footer
        print(boring)
        if boring=='on':
            boring=False
        else:
            boring=True
        circuits=ktope_hw2.buildCircuits(data.split('\n'))
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
        matrix1=ktope_hw2.buildComplexMatrix(circuits,elements)
        width=int(100/(len(circuits)+1))
        html+='''<br />
        <b>Матрица комплексов</b><br /><br />
        <table cellspacing="0">
        <tr class="gray">
            <td width="%i%%" class="white"></td>
            ''' % width
        for key in circuits:
            html+='''<td width="%i%%"><b>%i</b></td>''' % (width,key)
        html+='</tr>'
        lgray=False
        i=0
        for row in matrix1:
            if boring:
                if lgray:
                    html+='<tr class="lightGray">'
                else:
                    html+='<tr>'
                html+='<td class="gray"><b>%i</b></td>' % elements[i]
            else:
                html+='''<tr class="%s">
                <td class="%s"><b>%i</b></td>'''%(self.funnyColors[random.randint(0,len(self.funnyColors)-1)],self.funnyColors[random.randint(0,len(self.funnyColors)-1)], elements[i])
            for el in row:
                if el==0:
                    html+='<td>%i</td>' % el
                else:
                    html+='<td><b>%i</b></td>' % el
            html+='</tr>'
            i+=1
            lgray=not lgray
        width=int(100/(len(elements)+1))
        matrix2=ktope_hw2.buildConnMatrix(circuits,elements)
        html+='''</table><br />
        <b>Матрица соединений</b><br /><br />
        <table cellspacing="0">
        <tr class="gray">
        <td width="%i%%" class="white">
        ''' % width
        for el in elements:
            html+='<td width="%i%%"><b>%i</b></td>' % (width,el)
        html+='</tr>'
        i=0
        lgray=False
        for row in matrix2:
            if boring:
                if lgray:
                    html+='<tr class="lightGray">'
                else:
                    html+='<tr>'
                html+='<td class="gray"><b>%i</b></td>' % elements[i]
            else:
                html+='''<tr class="%s">
                <td class="%s"><b>%i</b></td>'''%(self.funnyColors[random.randint(0,len(self.funnyColors)-1)],self.funnyColors[random.randint(0,len(self.funnyColors)-1)],elements[i])
            k=0
            for val in row:
                if k==i:
                    html+='<td><b>%i</b></td>' % val
                else:
                    html+='<td>%i</td>' % val
                k+=1
            html+='</tr>'
            i+=1
            lgray=not lgray
        html+='''</table><br /><br />
        <b>Раскраска графа</b><br /><br />
        <table cellspacing="0">
        <tr class="gray">
        <td width="%i%%">Вершина</td>''' % width
        for el in elements:
            html+='<td width="%i%%"><b>%i</b></td>' % (width,el)
        html+='''</tr>
        <tr><td class="gray">Кол-во смежных</td>'''
        graph=ktope_hw2.buildGraph(matrix2,elements)
        for key in graph:
            html+='<td>%i</td>' % len(graph[key])
        html+='</tr></table><br /><br />'
        colored=ktope_hw2.colorGraph(graph)
        for key in colored:
            html+='j=%i: %s<br />' % (key,str(colored[key]))
        if not boring:
            html+='''<br /><h1>Эти нескучные цвета как бы намекают, что не стоит всем сдавать
            одинаковые отчёты</h1>'''
        return self.header+html+self.footer
    result.exposed=True

    def ktope(self):
        return self.index()
    ktope.exposed=True

import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')
if __name__ == '__main__':
    cherrypy.quickstart(KtoPage(), config=tutconf)
else:
    cherrypy.tree.mount(KtoPage(), config=tutconf)
