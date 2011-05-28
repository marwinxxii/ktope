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

class KtoPage:
    html='''
    <!DOCTYPE html>
<html>
    <head>
        <meta charset=utf-8>
        <title>KTOPE Homeworks</title>
    </head>
    <body>
    <center>
    <a href="/hw2"><strong>Домашнее задание №2</strong></a> (Полностью)<br/>
    <a href="/hw3"><strong>Домашнее задание №3</strong></a> (Без Франка-Фриша и списка путей)<br/>
    <a href="/hw5"><strong>Домашнее задание №5</strong></a> (Только гамильтонов цикл)<br/>
    <a href="https://github.com/marwinxxii/ktope/">Исходники</a><br />
    </center>
    </body>
</html>
    '''
    def index(self):
        return self.html
    index.exposed=True
