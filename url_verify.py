#!/usr/bin/python
# -*- coding:utf-8 -*-


def validate(context):
    """Version: 2020_07_18
    验证链接是否合法
    """
    import re
    from urllib.parse import urlparse

    text = context.strip()
    # 调度中可能复制带了空格
    if len(text) != len(context):
        return False

    rules = [
        r"(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]",
        r"@^(https?|ftp)://[^\s/$.?#].[^\s]*$@iS",
        r"#\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))#iS",
    ]
    for each in rules:
        p = re.compile(each)
        res = p.findall(text)
        if res:
            return True
    else:
        try:
            q = urlparse(text)
        except:
            return False
        else:
            if all([q.scheme, q.netloc, q.path]):
                return True
            else:
                return False


def process(text):
    """
    处理文本, 返回处理后的文本
    """
    idx = text.find('https')
    text = text[idx:]
    idx = text.rfind('?')
    if idx > 0:
        return text[0:idx]
    else:
        return text
    # idx2 = text.rfind('?')
    # if idx2 > 0:
    #     return text[idx:idx2+idx]
    # else:
    #     return text[idx:]


if __name__ == "__main__":
    #validate('''<a href="http://www.malingshu7.com/jg/show-htm-itemid-85660.html" target="_blank" title="3月8日山东济南马铃薯价格">3月8日山东济南马铃薯价格</a>''')
    result = process("/remote.axd?https://agfstorage.blob.core.windows.net/misc/Stock_photos/Potatoes/Potato_0006_135.jpg")
    print(result)

