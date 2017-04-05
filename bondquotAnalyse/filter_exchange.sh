#!/bin/sh

#筛选报价
#param1 输入文件名
#param2 输出文件名
#param3 goodsCode

tmpfile1=$1'_tmp1'
destfile=$2

goodsCode='[Code]('$3')'


# 删除所有的回车
# 根据[Type]头分行
tr -d '\n' < $1 | sed 's/\(\[[^]]*]\[Type]\)/\n\1/g' > $tmpfile1

# 过滤掉goodsCode
fgrep -a $goodsCode $tmpfile1 > $destfile


# 根据时间字段将数据还原
sed -i 's/\(\[[0-9].\{11\}\]\)/\n\1/g' $destfile


if [ -f $tmpfile1 ]
then
	rm $tmpfile1
fi
