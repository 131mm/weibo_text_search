import jieba
import xlwt
from redis import Redis

rds = Redis(host='localhost',port=6379) 
class Engine():
    def __init__(self):
        self.black_list = {'@',',','.','?','!',' ','[',']','{','}','(',')',\
                '，','。','！','？','#','//','...','--','----','\'','\"','‘','“',\
                ':',';','：','；','…','《','》','<','>',\
                '的','哈','哈哈','啊','等',}

    def get_index(self,keyword):
        wordset = rds.smembers('wordset')
        keyindex=()
        keysplit=jieba.cut_for_search(keyword)
        for key in keysplit:
            if key in self.black_list:
                continue
            if key.encode('utf-8') in wordset:
                index = rds.smembers('word_'+keyword)
                if keyindex==():
                    keyindex = index
                else:
                    keyindex &= index
        return sorted([int(ii.decode()) for ii in keyindex])
    
    def get_index2(self,keyword):
        wordset = rds.smembers('wordset')
        index = ()
        if keyword in self.black_list:
            return []
        if keyword.encode('utf-8') in wordset:
            index = rds.smembers('word_'+keyword)
        return sorted([int(ii.decode()) for ii in index])

    def search(self,keyword,page=0,page_len=20):
        coIndex=self.get_index2(keyword)
        msg = []
        '''使用redis管道查询'''
        pipe = rds.pipeline()
        for i in coIndex[page*page_len:(page+1)*page_len]:
            pipe.get('item_'+str(i))
        result = pipe.execute()
        for j,i in enumerate(coIndex[page*page_len:(page+1)*page_len]):
            msg.append({'id':i,'msg':result[j].decode()})
        return msg,len(coIndex)

    def download(self,keyword):
        """开始制作表格"""
        wb=xlwt.Workbook()
        wb.encoding='utf8'  #设置字符编码
        ws=wb.add_sheet('1')    
        """表头开始"""
        ws.write(0,0,u'id')
        ws.write(0,1,u'text')
        """表体开始"""
        coIndex=self.get_index2(keyword)
        count = 1 
        pipe = rds.pipeline()
        for i in coIndex:
            pipe.get('item_'+str(i))
            ws.write(count,0,i)
            count+=1
        result = pipe.execute()
        count = 1
        for i in result:
            ws.write(count,1,i.decode())
            count+=1
        return wb

    def run(self):
        while 1:
            keyword=input('请输入搜索关键词\n')
            coIndex=self.search(keyword)
            msg = []
            for i in coIndex:
                post = rds.get('item_'+str(i))
                msg.append([i,post.decode()])
            print(msg,len(msg))

if __name__ == '__main__':
    search=Engine()
    msg = search.search(keyword='haha')
    print(msg)
