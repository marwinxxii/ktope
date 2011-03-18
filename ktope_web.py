# -*- coding: utf-8 -*-
import cherrypy

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
        bacground:#eee;
    }
    </style>
    </head>
<body>'''
    
    footer='''
    </body>
</html>'''

    def index(self):
        return self.index+'''
        На каждой строке файла по одной цепи, в цепи через запятую - модули.
        <form action="result" method="GET">
        <textarea rows="30" cols="80" name="data"></textarea><br />
        <input type="submit" /><br />
        Нажимая на эту кнопку, вы соглашаетесь, что пользуетесь этим сервисом на свой страх и риск
        <img src="http://forum.kgn.ru/Smileys/default/trollface.png" /><br />
        исходный скрипт - marwinXXII, веб версия - Egor-kun<br />
        <a href="http://rospil.info/donate">Donate</a>
        </form>'''+self.footer
    index.exposed=True

    def result(self,data=None):
        if not data:
            return self.header+'''Введите <a href="./">данные</a>'''+self.footer
        
