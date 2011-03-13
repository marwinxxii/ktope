# -*- coding: utf-8 -*-
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import fileinput

#генерим хтмлку
print '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>KTOPE - Homework 2</title>'
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
<body>
<b>Задание</b><br /><br />'''
#на каждой строке файла по одной цепи, в цепи через запятую-модули
fileName='circuits3.txt'
elements={}#словарь с модулями
firstIndex=1#номер первой цепи и модуля
i=firstIndex
elemCount=0
for line in fileinput.input(fileName):
	for element in line[:len(line)-1].split(','):
		el=int(element)
		if el in elements:
			if i not in elements[el]:#проверка на повторение модулей
				elements[el].append(i)
		else:
			elements[el]=[i]
                        elemCount+=1
	#цепь пустая если в ней 1 эл-т
	if len(elements[el])==1:
                elemCount-=1
		del elements[el]
	print 'Цепь №%i %s<br />' % (i,line)
	i+=1
print len(elements)
print '<br />'
print '''<b>Матрица комплексов</b>\n<br /><br />
<table cellspacing="0">
<tr>\n<td>&nbsp;</td>'''
us=range(firstIndex,i)
str=''
#header
for k in us:
	str+='<td width="%i%%" class="gray"><b>%i</b></td>' % (100/i,k)
print str
print '</tr>'
k=firstIndex
matrix={}
lightGray=False
for element in elements:
	if lightGray:
		str='<tr class="lightGray">'
	else:
		str='<tr>'
	lightGray=not lightGray
	str+='\n<td class="gray"><b>%i</b></td>' % k
	mels=[]
	#для каждой цепи проверяем входит ли в нее эл-т
	for u in us:
		str+='<td>'
		if u in elements[element]:
			str+='<b>1</b>'
			mels.append(1)
		else:
			str+='0'
			mels.append(0)
		str+='</td>'
	matrix[k]=mels
	k+=1
	str+='</tr>'
	print str
us=range(firstIndex,len(elements)+firstIndex)
print '''</table><br /><br />
<b>Матрица соединений</b>\n<br /><br />
<table cellspacing="0">'''
print '<tr>\n<td width="%i%%">&nbsp;</td>' % (100/len(us))
str=''
#header
#print matrix
for k in us:
	str+='<td width="%i%%" class="gray"><b>%i</b></td>' % (100/len(us),k)
print str
print '</tr>'
k=firstIndex
lightGray=False
matrix2={}
for row in us:
	if lightGray:
		str='<tr class="lightGray">'
	else:
		str='<tr>'
	lightGray=not lightGray
	str+='\n<td class="gray"><b>%i</b></td>' % k
	print str
	matrix2[row]=[]
	for row2 in us:
		s=0
		if row==row2:
			print '<td><b>0</b></td>'
			continue
		if len(matrix[row])!=len(matrix[row2]):
			print 'fial!'
		for i in range(len(matrix[row])):
			if matrix[row][i]==1 and matrix[row][i]==matrix[row2][i]:
				s+=1
		print '<td>%i</td>' % s
		if s!=0:
			matrix2[row].append(row2)
	print '</tr>'
	k+=1
width=100/(len(us)+1)
print '''</table><br /><br />
<b>Раскраска графа</b><br /><br />
<table cellspacing="0">
<tr class="gray">
	<td width="%i%%">Вершина</td>''' % width
for key in matrix2:
	print '<td width="%i%%">%i</td>' % (width,key)
print '''</tr>
<tr>
	<td>Кол-ов смежных</td>'''
for key in matrix2:
	print '<td>%i</td>' % (len(matrix2[key]))
print '''</tr>
</table><br />'''
#раскрашиваем граф по алгоритму
j=1
matrix=matrix2
#print matrix
colored={}
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
	print 'Выберем цвет j=%i<br />' % j
	str='%i' % dots[0]
	print 'Упорядоченные по невозрастанию вершины:<br />'
	for dot in dots[1:]:
		str+=',%i' % dot
	str+='<br />'
	print str
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
print '<br />Раскрашиваем вершины в соответствующие цвета:<br />'
for color in colored:
	print 'j=%i ' % color
	print colored[color]
	print '<br />'
print '</body>\n</html>'
