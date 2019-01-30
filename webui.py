import web
from web.contrib.template import render_jinja

## 路由
urls=(
    '/', 'home',
    '/search', 'search',
    '/download', 'download',
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
class search():
    def GET(self):
        data = web.input()
        keyword = data.get('keyword','')


application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
