import jieba
from redis import Redis

rds = Redis(host='localhost',port=6379) 
class Engine():
    def __init__(self):
        self.black_list = {'@',',','.','?','!',' ','[',']','{','}','(',')',\
                '，','。','！','？','#','//','...','--','----','\'','\"','‘','“',\
                ':',';','：','；','…','《','》','<','>',\
                '的','哈','哈哈','啊','等',}

    def get_index(self,keyword):
        keyindex=()
        keysplit=jieba.cut_for_search(keyword)
        wordset = rds.smembers('wordset')
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

    def search(self,keyword,last_id,page_len):
        coIndex=self.get_index(keyword)
        msg = []
        for i in coIndex:
            post = rds.get('item_'+str(i))
            msg.append([i,post.decode()])

    def download(self,data,name):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('Sheet1',cell_overwrite_ok=True)
        k=0
        for i in data:
            sheet.write(k,0,i)
            sheet.write(k,1,)
        wbk.save(name+'.xls')

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
    search.run()
