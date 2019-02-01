# 全文关键词搜索项目


这个项目是2018年5月份参加平安产险的挑战赛的项目，当时做的很差，后来慢慢做了几次优化，现在算是可以正常使用。

##项目需求：

题目的需求是在40万条微博文本中迅速搜索到给定关键词所在的文本。

##解决方案：

本项目搜索部分采用了倒排索引，将所有文本拆分为词，以词为索引，找到词所在句的id，就完成了搜索。

较为理想的存储方案是把40万存入数据库，讲索引文件放在缓存中，查询的时候从缓存中快速拿到所有id，根据id去数据库中拿到原始数据。在实际操作中发现把40万条数据全塞进redis也只占用大概300M内存，而且原始数据key-value型的，用redis很恰当，于是就把redis当数据库使用了。

后端框架一开始选用了django，后来觉得这个项目功能需求太简单，不需要用那么庞大的框架，于是改用web.py，大大降低了代码量。整个网页中也没有什么静态资源，nginx都可以不必上，直接用uwsgi调用就行。

## 最终产品

![深度截图_选择区域_20190201153735.png](https://i.loli.net/2019/02/01/5c53f75b92b25.png)

![深度截图_选择区域_20190201153745.png](https://i.loli.net/2019/02/01/5c53f75b879bc.png)

最终的功能只有两个，搜索和下载搜索结果，技术亮点也不多，在redis查询时用了redis的管道技术，多次id查询集中到一次查询，降低网络延迟带来的时间损耗。在后台发送查询结果的xls文件时却遇到了中文编码问题：`TypeError: http header must be encodable in latin1` ，解决方案是把http header 中的`'Content-Disposition','attachment;filename="{}"'`filename用`urllib.parse.quote()`编码了一次，参考 [HTTP协议header中Content-Disposition中文文件名乱码 - 乒乓狂魔 - 开源中国](https://my.oschina.net/pingpangkuangmo/blog/376332)

#### 示例网站
[adiao.me:800](http://adiao.me:800)

#### 项目地址
[github](https://github.com/131mm/weibo_text_search)


