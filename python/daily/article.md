![](http://upload-
images.jianshu.io/upload_images/1262158-f126fdfe9729726c.jpg?imageMogr2/auto-
orient/strip%7CimageView2/2/w/1240)  

BeautifulSoup

* * *

官方文档如下介绍：

> **Beautiful Soup** 是一个可以从 **HTML** 或 **XML** 文件中提取数据的 **Python**
库.它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式.**Beautiful Soup** 会帮你节省数小时甚至数天的工作时间.

* * *

## 1\. 安装

> 以下都是在 **python2.7** 中进行测试的

可以直接使用 **pip** 安装：

    
    
    $ pip install beautifulsoup4

**BeautifulSoup** 不仅支持 **HTML** 解析器,还支持一些第三方的解析器，如，**lxml，XML，html5lib** 但是需要安装相应的库。
    
    
    $ pip install lxml
    
    $ pip install html5lib

* * *

## 2\. 开始使用

> **Beautiful Soup** 的功能相当强大，但我们只介绍经常使用的功能。

### 简单用法

将一段文档传入 **BeautifulSoup** 的构造方法,就能得到一个文档的对象, 可以传入一段字符串或一个文件句柄.

    
    
    >>> from bs4 import BeautifulSoup
    
    >>> soup = BeautifulSoup("<html><body><p>data</p></body></html>")
    
    >>> soup
    <html><body><p>data</p></body></html>
    
    >>> soup('p')
    [<p>data</p>]

首先传入一个 **html** 文档，`soup` 是获得文档的对象。然后,文档被转换成 **Unicode** ,并且 **HTML** 的实例都被转换成
**Unicode** 编码。然后,**Beautiful Soup** 选择最合适的解析器来解析这段文档,如果手动指定解析器那么 **Beautiful
Soup** 会选择指定的解析器来解析文档。但是一般最好手动指定解析器，并且使用 **requests** 与 **BeautifulSoup**
结合使用， **requests** 是用于爬取网页源码的一个库，此处不再介绍，**requests** 更多用法请参考 [ Requests 2.10.0
文档 ](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html)。

  * 要解析的文档是什么类型: 目前支持, **html, xml,** 和 **html5**
  * 指定使用哪种解析器: 目前支持, **lxml, html5lib,** 和 **html.parser**
    
    
    from bs4 import BeautifulSoup
    import requests
    
    html = requests.get(‘http://www.jianshu.com/’).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    result = soup('div')

### 对象的种类

**Beautiful Soup** 将复杂 **HTML** 文档转换成一个复杂的树形结构,每个节点都是 **Python** 对象,所有对象可以归纳为 4 种: `Tag , NavigableString , BeautifulSoup , Comment .`

  * `Tag`：通俗点讲就是 **HTML** 中的一个个标签，像上面的 `div，p`。每个 `Tag` 有两个重要的属性 `name` 和 `attrs，name` 指标签的名字或者 `tag` 本身的 `name，attrs` 通常指一个标签的 `class`。
  * `NavigableString`：获取标签内部的文字，如，`soup.p.string`。
  * `BeautifulSoup`：表示一个文档的全部内容。
  * `Comment：Comment` 对象是一个特殊类型的 `NavigableString` 对象，其输出的内容不包括注释符号.

### 示例

下面是一个示例，带你了解 **Beautiful Soup** 的常见用法：

    
    
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    from bs4 import BeautifulSoup
    import requests
    
    
    html_doc = """
    <head>
          <meta charset="utf-8">
          <meta http-equiv="X-UA-Compatible" content="IE=Edge">
        <title>首页 - 简书</title>
    </head>
    
    <body class="output fluid zh cn win reader-day-mode reader-font2 " data-js-module="recommendation" data-locale="zh-CN">
    
    <ul class="article-list thumbnails">
    
      <li class=have-img>
          <a class="wrap-img" href="/p/49c4728c3ab2"><img src="http://upload-images.jianshu.io/upload_images/2442470-745c6471c6f8258c.jpg?imageMogr2/auto-orient/strip%7CimageView2/1/w/300/h/300" alt="300" /></a>
        <div>
          <p class="list-top">
            <a class="author-name blue-link" target="_blank" href="/users/0af6b163b687">阿随向前冲</a>
            <em>·</em>
            <span class="time" data-shared-at="2016-07-27T07:03:54+08:00"></span>
          </p>
          <h4 class="title"><a target="_blank" href="/p/49c4728c3ab2"> 只装了这六款软件，工作就高效到有时间逛某宝刷某圈</a></h4>
          <div class="list-footer">
            <a target="_blank" href="/p/49c4728c3ab2">
              阅读 1830
    </a>        <a target="_blank" href="/p/49c4728c3ab2#comments">
               · 评论 35
    </a>        <span> · 喜欢 95</span>
              <span> · 打赏 1</span>
    
          </div>
        </div>
      </li>
    </ul>
    
    </body>
    """
    
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
    
    # 查找所有有关的节点
    tags = soup.find_all('li', class_="have-img")
    
    for tag in tags:
            image = tag.img['src']
            article_user = tag.p.a.get_text()
            article_user_url = tag.p.a['href']
            created = tag.p.span['data-shared-at']
            article_url = tag.h4.a['href']
    
            # 可以在查找的 tag 下继续使用 find_all()
            tag_span = tag.div.div.find_all('span')
    
            likes = tag_span[0].get_text(strip=True)

**BeautifulSoup** 主要用来遍历子节点及子节点的属性，通过点取属性的方式只能获得当前文档中的第一个 `tag`，例如，`soup.li`。如果想要得到所有的`<li>` 标签,或是通过名字得到比一个 `tag` 更多的内容的时候,就需要用到 `find_all()`，`find_all()` 方法搜索当前 tag 的所有 tag 子节点,并判断是否符合过滤器的条件`find_all()` 所接受的参数如下：
    
    
    find_all( name , attrs , recursive , string , **kwargs )

  1. 按 `name` 搜素: `name` 参数可以查找所有名字为 `name` 的 `tag`,字符串对象会被自动忽略掉:
    
         soup.find_all("li")

  2. 按 `id` 搜素: 如果包含一个名字为 `id` 的参数,搜索时会把该参数当作指定名字 `tag` 的属性来搜索:
    
         soup.find_all(id='link2')

  3. 按 `attr` 搜索：有些 `tag` 属性在搜索不能使用,比如 **HTML5** 中的 `data-*` 属性，但是可以通过 `find_all()` 方法的 `attrs` 参数定义一个字典参数来搜索包含特殊属性的 `tag`:
    
         data_soup.find_all(attrs={"data-foo": "value"})

  4. 按 `CSS` 搜索: 按照 `CSS` 类名搜索 `tag` 的功能非常实用,但标识`CSS` 类名的关键字 `class` 在 **Python** 中是保留字,使用 `class` 做参数会导致语法错误.从 **Beautiful Soup** 的 4.1.1 版本开始,可以通过 `class_` 参数搜索有指定 `CSS` 类名的 `tag`:
    
         soup.find_all('li', class_="have-img")

  5. `string` 参数：通过 `string` 参数可以搜搜文档中的字符串内容.与 `name` 参数的可选值一样, `string` 参数接受 字符串 , 正则表达式 , 列表, `True` 。 看例子:
    
         soup.find_all("a", string="Elsie")

  6. `recursive` 参数：调用 `tag` 的 `find_all()` 方法时,**Beautiful Soup** 会检索当前 `tag` 的所有子孙节点,如果只想搜索 `tag` 的直接子节点,可以使用参数 `recursive=False` .
    
         soup.find_all("title", recursive=False)

> **find_all()** 几乎是 **Beautiful Soup**中最常用的搜索方法,也可以使用其简写方法，以下代码等价：

    
    
        soup.find_all("a")
        soup("a")

### get_text()

如果只想得到 `tag` 中包含的文本内容,那么可以嗲用 `get_text()` 方法,这个方法获取到 `tag` 中包含的所有文版内容包括子孙
`tag` 中的内容,并将结果作为 `Unicode` 字符串返回:

    
    
        tag.p.a.get_text()

如果想看更多内容，请参考 [ Beautiful Soup 4.4.0 文档
](http://beautifulsoup.readthedocs.io/zh_CN/latest/#id18)（中文文档）。

