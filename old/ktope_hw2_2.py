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

#на каждой строке по одной цепи, в цепи через запятую-модули
circuits=[
'11,17,15,13',
'9,1,13,14',
'6,13,11',
'8,14,3,17',
'2,16,13,10',
'10,5,5,7',
'11,17,13',
'17,17,13',
'13,14,17',
'11,14',
'2,14',
'5,13,8',
'11,16',
'1,4,12,13',
'3,8',
'15,17,9,3',
'8,12,8,10',
'9,17,10,17',
'17,17,17,13',
'5,13,8,17',
'9,9,15,9',
'3,9,10',
'14,14,6',
'15,7,8,1',
'16,9,9,15',
'15,9,7,4',
'16,5',
'16,16,7,12',
'16,16,8,7',
'11,3,3,3',
'3,16',
'6,15,12,14'
]
elements={}#словарь с модулями
firstIndex=1#номер первой цепи и модуля
i=firstIndex
for line in circuits:
	for element in line.split(','):
		el=int(element)
		if el in elements:
			if i not in elements[el]:#проверка на повторение модулей
				elements[el].append(i)
		else:
			elements[el]=[i]
	print 'Цепь №%i %s<br />' % (i,line)
	i+=1
#print elements
#генерим хтмлку
print '<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
print '<title>KTOPE - Homework 2</title>'
print ''''<style type="text/css">
table{
width:100%;
text-align:center;
}
.gray{
background:#ccc;
}
.lightGray{
background:#eee;
}'''
print '</style>\n</head>\n<body>'
print '<b>Матрица комплексов</b>\n<br /><br />'
print '<table cellspacing="0">'
print '<tr>\n<td>&nbsp;</td>'
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
print '</table><br /><br />'
us=range(firstIndex,len(elements)+firstIndex)
print '<b>Матрица соединений</b>\n<br /><br />'
print '<table cellspacing="0">'
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
print '</table><br /><br />'
print '<b>Раскраска графа</b><br /><br />'
#раскрашиваем граф по алгоритму
j=1
matrix=matrix2
colored={}
while len(matrix)>0:
	dots=[]
	matrix2=matrix.copy()
	#сортируем по невозрастанию
	while len(matrix2)>0:
		min=len(matrix2[matrix2.keys()[0]])
		minkey=matrix2.keys()[0]
		for key in matrix2:
			if len(matrix2[key])<min:
				min=len(matrix2[key])
				minkey=key
		dots.append(minkey)
		del matrix2[minkey]
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
#print colored
print '</body>\n</html>'
