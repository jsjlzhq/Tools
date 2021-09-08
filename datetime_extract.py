#!/usr/bin/python
# -*- coding:utf-8 -*-

def process(text):
    """Version: 2020_07_25
    时间提取脚本模版
    """
    import re
    from datetime import datetime

    text = text.strip()

    rules = [
        r"(\d{2}\d{2}([\.\-/|年月\s]{1,3}\d{1,2}){2}日?(\s?\d{1,2}:\d{1,2}(:\d{1,2})?)?)|(\d{1,2}\s?(分钟|小时|天|周)前)|昨天|前天",  # 常见中文日期格式, 网上找的
        # r"\d{10}",  # 处理时间戳, 遇到再加: 15开头的10或13位数字, 其实匹配前10个就够了
        # r"",  # 如有不是常见的日期时间格式，此处替换成案例
    ]
    # 预处理，替换掉会影响正则提取的固定字符串, 如点击量的数字
    flags = [
        "发布时间",
    ]
    for each in flags:
        text = text.replace(each, "")
    # 无内容时间返回空
    length = len(re.sub(r"\s+", "", text))
    if length < 6:
        return f"error:{text}"
    # 提取日期时间
    for each in rules:
        p = re.compile(each)
        res = p.findall(text)
        if res:
            res = sorted([i for i in res[0]], key=len, reverse=True)
            return parse(res[0])
        else:
            continue
    else:
        return f"error:{text}"


def parse(text):
    import re
    import datetime

    release_time = text.strip()

    if "年前" in release_time:
        years = re.compile(r"(\d+)年前").findall(release_time)
        years_ago = datetime.datetime.now() - datetime.timedelta(days=int(years[0]) * 365)
        release_time = years_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "月前" in release_time:
        months = re.compile(r"(\d+)月前").findall(release_time)
        months_ago = datetime.datetime.now() - datetime.timedelta(days=int(months[0]) * 30)
        release_time = months_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "周前" in release_time:
        weeks = re.compile(r"(\d+)周前").findall(release_time)
        weeks_ago = datetime.datetime.now() - datetime.timedelta(days=int(weeks[0]) * 7)
        release_time = weeks_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "天前" in release_time:
        ndays = re.compile(r"(\d+)天前").findall(release_time)
        days_ago = datetime.datetime.now() - datetime.timedelta(days=int(ndays[0]))
        release_time = days_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "小时前" in release_time:
        nhours = re.compile(r"(\d+)小时前").findall(release_time)
        hours_ago = datetime.datetime.now() - datetime.timedelta(hours=int(nhours[0]))
        release_time = hours_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "分钟前" in release_time:
        nminutes = re.compile(r"(\d+)分钟前").findall(release_time)
        minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=int(nminutes[0]))
        release_time = minutes_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "昨天" in release_time or "昨日" in release_time:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        release_time = release_time.replace("昨天", str(yesterday))

    elif "今天" in release_time:
        release_time = release_time.replace("今天", get_current_date("%Y-%m-%d"))

    elif "刚刚" in release_time:
        release_time = get_current_date()

    elif re.search(r"^\d\d:\d\d", release_time):
        release_time = get_current_date("%Y-%m-%d") + " " + release_time

    elif not re.compile(r"\d{4}").findall(release_time):
        month = re.compile(r"\d{1,2}").findall(release_time)
        if month:
            if int(month[0]) <= int(get_current_date("%m")):
                release_time = get_current_date("%Y") + "-" + release_time
            else:
                release_time = str(int(get_current_date("%Y")) - 1) + "-" + release_time

    return release_time


def get_current_date(date_format="%Y-%m-%d %H:%M:%S"):
    import datetime
    return datetime.datetime.now().strftime(date_format)


if __name__ == "__main__":
    print(process('''
2021-03-02 08:58　　来源：'''))
