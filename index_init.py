import jieba,csv
from redis import Redis
from multiprocessing import Process,Pool

rds = Redis(host='localhost',port=6379) 
class searchEngine:
    def __init__(self):
        self.black_list = {'@',',','.','?','!',' ','[',']','{','}','(',')',\
                '，','。','！','？','#','//','...','--','----','\'','\"','‘','“',\
                ':',';','：','；','…','《','》','<','>',\
                '的','哈','哈哈','啊','等',}

    def toIndex(self,dataset,no):
        for item in dataset:
            rds.set('item_'+item[0],item[1])
            itemsplit=jieba.cut_for_search(item[1])
            for t in itemsplit:
                word=str(t)
                if word in self.black_list:
                    continue
                rds.sadd('wordset',word)
                rds.sadd('word_'+word,item[0])

    def rawToRedis(self,data):
        for i in data:
            rds.set('data_'+i[0],i[1])

    def indexCreat(self,testdata):
        #初始化数据
        lens=round(len(testdata)/8)
        datasplit=[]
        process=[]
        for i in range(8):
            datasplit.append(testdata[i*lens:(i+1)*lens])
        for i in range(8):
            p=Process(target=self.toIndex,args=(datasplit[i],i))
            process.append(p)
        for i in process:
            i.start()
        for i in process:
            i.join()

    def searchEngine(self,keyword):
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
                    keyindex |= index
        return sorted([int(ii.decode()) for ii in keyindex])
    def store(self,data,name):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('Sheet1',cell_overwrite_ok=True)
        k=0
        for i in data:
            sheet.write(k,0,i)
            sheet.write(k,1,)
        wbk.save(name+'.xls')

    def search(self):
        datapath='data.csv'
        with open(datapath,mode='r',encoding='gbk',errors='ignore') as f:
            data=csv.reader(f)
            j=0
            testdata=[]
            for i in data:
                testdata.append(i)
        self.indexCreat(testdata)
        while 1:
            keyword=input('请输入搜索关键词\n')
            coIndex=self.searchEngine(keyword)
            msg = []
            for i in coIndex:
                post = rds.get('item_'+str(i))
                msg.append([i,post.decode()])
            print(msg)

if __name__ == '__main__':
    search=searchEngine()
    search.search()
