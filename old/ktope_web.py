#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import cherrypy

class WelcomePage:
    header = u'''
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Скачать КТОПЭ БЕсПЛАНО БЕЗ СМС БЕЗ РЕГиСТРАЦИИ!!1</title>
    <style type="text/css">
    table{
    width:100%;
    text-align:center;
    }
    .gray{
    background:#ccc;
    }
    .lightGray{
    background:#eee;
    }
    </style>
    </head>
    <body>'''

    footer = u'''
    </body>
</html>'''

    def index(self):
        return self.header + u'''
    На каждой строке файла по одной цепи, в цепи через запятую - модули.
    <form action="result" method="GET">
    <textarea rows="30" cols="80" name="data"> </textarea> <br /> 
    <input type="submit" /><br />
    Нажимая на эту кнопку, вы соглашаетесь, что пользуетесь этим сервисом на свой страх и риск <img src="http://forum.kgn.ru/Smileys/default/trollface.png" /><br />
    исходный скрипт - marwinXXII, веб версия - Egor-kun<br />
    <a href="http://rospil.info/donate">Donate</a>
    </form>''' + self.footer
    index.exposed = True
    
    def result(self, data=None):
        data = data.decode('utf-8').split(u'\r\n')
        data = data[:-1]
        #return repr(data)
        if not data:
            return self.header + u'''Ненене, введите <a href="./">данные</a> то!''' + self.footer

        res = u'''<b>Задание</b><br /><br />'''
        #на каждой строке файла по одной цепи, в цепи через запятую-модули
        elements = {} #словарь с модулями
        firstIndex = 1 #номер первой цепи и модуля
        i = firstIndex
        for line in data:
            #детектор пустой цепи
            circuit=set()
            for element in line[:len(line)].split(','):
		el = int(element)
                circuit.add(el)
            if len(circuit)<=1:
                res +=u'Цепь №%i пустая %s<br />' % i
                continue
            #обрабатываем эл-ты цепи
            for el in circuit:
		if el in elements:
                    elements[el].append(i)
                else:
                    elements[el]=[i]
            res += u'Цепь №%i %s<br />' % (i,line)
            i+=1
        #print 'shit'
        #print elements
        res += u'''<br />'''
        res += u'''<b>Матрица комплексов</b>\n<br /><br />
<table cellspacing="0">
<tr>\n<td width="%i%%">&nbsp;</td>''' % (100/i)
        us = range(firstIndex,i)#цепи
        st = u''
#header
        for k in us:
            st += u'<td width="%i%%" class="gray"><b>%i</b></td>' % (100/i,k)
        res += st
        res += u'</tr>'
        k = firstIndex
        matrix = {}
        lightGray = False
        for element in elements:
            if lightGray:
		st = u'<tr class="lightGray">'
            else:
		st = u'<tr>'
            lightGray=not lightGray
            st += u'\n<td class="gray"><b>%i</b></td>' % element
            mels = []
            for u in us:#проверяем принадлежит ли модуль цепи
		st += u'<td>'
		if u in elements[element]:
                    st += u'<b>1</b>'
                    mels.append(1)
		else:
                    st += u'0'
                    mels.append(0)
		st += u'</td>'
            matrix[element] = mels
            k+=1
            st += u'</tr>'
            res += st
        #print k
        #print matrix
        us=range(firstIndex,len(elements)+firstIndex)
        res += u'''</table><br /><br />
<b>Матрица соединений</b>\n<br /><br />
<table cellspacing="0">'''
        res += u'<tr>\n<td width="%i%%">&nbsp;</td>' % (100/len(us))
        st = u''
#header
#print matrix
        for k in matrix:
            st += u'<td width="%i%%" class="gray"><b>%i</b></td>' % (100/len(us),k)
        res += st
        res += u'</tr>'
        k = firstIndex
        lightGray = False
        matrix2 = {}
        for row in matrix:
            if lightGray:
		st = u'<tr class="lightGray">'
            else:
		st = u'<tr>'
            lightGray = not lightGray
            st += u'\n<td class="gray"><b>%i</b></td>' % row
            res += st
            matrix2[row] = []
            for row2 in matrix:
		s = 0
		if row==row2:
                    res += u'<td><b>0</b></td>'
                    continue
		if len(matrix[row])!=len(matrix[row2]):
                    res += u'fial!'
		for i in range(len(matrix[row])):
                    if matrix[row][i]==1 and matrix[row][i]==matrix[row2][i]:
                        s+=1
		res += u'<td>%i</td>' % s
		if s!=0:
                    matrix2[row].append(row2)
            res += u'</tr>'
            k+=1
        width=100/(len(us)+1)
        res += u'''</table><br /><br />
<b>Раскраска графа</b><br /><br />
<table cellspacing="0">
<tr class="gray">
	<td width="%i%%">Вершина</td>''' % width
        for key in matrix2:
            res += u'<td width="%i%%">%i</td>' % (width,key)
        res += u'''</tr>
<tr>
	<td>Кол-ов смежных</td>'''
        for key in matrix2:
            res += u'<td>%i</td>' % (len(matrix2[key]))
        res += u'''</tr>
</table><br />'''
#раскрашиваем граф по алгоритму
        j = 1
        matrix = matrix2
#print matrix
        colored = {}
        while len(matrix)>0:
            dots=[]
            matrix2=matrix.copy()
	#сортируем по невозрастанию
            while len(matrix2)>0:
		#по очереди извлекаем индексы вершин с наиб числом смежных
		max=len(matrix2[matrix2.keys()[0]])
		maxkey=matrix2.keys()[0]
		for key in matrix2:
                    if len(matrix2[key])>max:
                        max=len(matrix2[key])
                        maxkey=key
                dots.append(maxkey)
		del matrix2[maxkey]
            res +=u'Выберем цвет j=%i<br />' % j
            st=u'%i' % dots[0]
            res+= u'Упорядоченные по невозрастанию вершины:<br />'
            for dot in dots[1:]:
                st+=u',%i' % dot
            st += u'<br />'
            res += st
            key=dots[0]
            colored[j]=[key]
	#выбираем не смежные вершины
            for key2 in dots[1:]:
                if key2 in matrix[key]:
                    continue
                colored[j].append(key2)
                #удаляем окрашенные вершины
            for key in colored[j]:
                del matrix[key]
                
            j+=1
#print '<br />'
        res += u'<br />Раскрашиваем вершины в соответствующие цвета:<br />'
        for color in colored:
            res += u'j=%i ' % color
            res += str(colored[color])
            res += u'<br />'
        return self.header + res + self.footer
    result.exposed = True
import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

if __name__ == '__main__':
    cherrypy.quickstart(WelcomePage(), config=tutconf)
else:
    cherrypy.tree.mount(WelcomePage(), config=tutconf)
