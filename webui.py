import web
from io import BytesIO
from search import Engine
from web.contrib.template import render_jinja

## 路由
urls=(
    '/', 'home',
    '/search/', 'search',
    '/download/', 'download',
)

app=web.application(urls,globals())

## 使用jinja渲染
render=render_jinja(
    'templates',
    encoding='utf-8'
)


## 主页
class home():
    def GET(self):
        return render.home()

    def POST(self):
        return self.GET()

Engine = Engine()
class search():
    def GET(self):
        data = web.input()
        keyword = data.get('keyword','')
        page = int(data.get('page',0))
        page_len = 20
        msg, len2 = Engine.search(keyword=keyword, page=page, page_len=page_len)
        ret = {
        'start': page*page_len,
        'end': min((page+1)*page_len,len2),
        'len2': len2,
        'message': msg,
        'keyword': keyword,
        'page': page+1 if len2>page_len else 0,
        }
        return render.result(ret)

class download():
    def GET(self):
        data = web.input()
        keyword = data.get('keyword','')
        import urllib
        file_name=urllib.parse.quote((keyword+".xls"))
        """设置web header"""
        web.header('Content-type','application/vnd.ms-excel')  #指定返回的类型
        web.header('Transfer-Encoding','chunked')
        web.header('Content-Disposition','attachment;filename="{}"'.format(file_name)) #设定文件名
        msg = Engine.download(keyword)
        sio=BytesIO()
        msg.save(sio)
        return sio.getvalue() 

application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
