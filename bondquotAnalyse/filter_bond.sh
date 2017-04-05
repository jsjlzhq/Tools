#!/bin/sh

#筛选报价
#param1 输入文件名
#param2 输出文件名
#param3 类型 0-bondoffer 1-bonddeal 2-jms2qpid筛选offer数据 3-jms2qpid筛选deal数据
#param4 简化类型 0-只筛选出id 1-筛选多个字段
#param5 剔除NCD券 0-不需要剔除 1-需要剔除
#param6 brokerId
#param7 goodsCode
#param8 offer中symbol,bid=1,ofr=-1

tmpfile1=$1'_tmp1'
tmpfile2=$1'_tmp2'
destfile=$2
simplefile=$2'_simple'

if [ $3 -eq 0 ]
then
	companyId='[cid]('$6')'
	goodsCode='[gc]('$7')'
	symbol='[sym]('$8')'
	if [ $4 -eq 0 ]
	then
		grepfield='\[id\]'
	else
		grepfield='\[Type\]|\[ds\]|\[gc\]|\[id\]|\[pri\]|\[sts\]|\[sym\]|\[vol\]'
	fi
	ncdfilter='\[bk\]\(.*NCD.*\)'
elif [ $3 -eq 1 ]
then
	companyId='[MS_COMPANY_ID]('$6')'
	goodsCode='[MS_GOODS_CODE]('$7')'
	if [ $4 -eq 0 ]
	then
		grepfield='\[MS_id\]'
	else
		grepfield='\[Type\]|\[MS_GOODS_CODE\]|\[MS_OPERATE\]|\[MS_TYPE\]|\[MS_id\]|\[MS_price\]|\[MS_dealStatus\]|\[MS_yield\]'
	fi
	ncdfilter='\[MS_BOND_KEY\]\(.*NCD.*\)'
elif [ $3 -ge 2 ]
then
	companyId='[companyId]('$6')'
	goodsCode='[goodsCode]('$7')'
	symbol='[symbol]('$8')'
	if [ $3 -eq 2 ]
	then
		filteritem='bondOfferMessage'
	elif [ $3 -eq 3 ]
	then
		filteritem='bondDealMessage'
	fi
	if [ $4 -eq 0 ]
	then
		grepfield='\[id\]'
	else
		grepfield='\[Type\]|\[dealStatus\]|\[goodsCode\]|\[id\]|\[internally\]|\[price\]|\[status\]|\[symbol\]|\[yield\]|\[volume\]|\[createTime\]'
	fi
	ncdfilter='\[bondKey\]\(.*NCD.*\)'
fi


# 删除所有的回车
# 根据[Type]头分行
tr -d '\n' < $1 | sed 's/\(\[[^]]*]\[Type]\)/\n\1/g' > $tmpfile1

# 过滤掉BondOfferMessage/BondDealMessage
if [ $3 -ge 2 ]
then
	grep -a $filteritem $tmpfile1 > $tmpfile2
	mv $tmpfile2 $tmpfile1
fi

if [ $5 -eq 1 ]
then
	grep -av $ncdfilter $tmpfile1 > $tmpfile2
	mv $tmpfile2 $tmpfile1
fi

# 过滤掉Broker/goodsCode/symbol
if [ $# -eq 6 ]
then
	fgrep -a $companyId $tmpfile1 > $tmpfile2
	mv $tmpfile2 $tmpfile1
elif [ $# -eq 7 ]
then
	fgrep -a $companyId $tmpfile1 | fgrep -a $goodsCode > $tmpfile2
	mv $tmpfile2 $tmpfile1
elif [ $# -eq 8 ]
then
	fgrep -a $companyId $tmpfile1 | fgrep -a $goodsCode | fgrep -a $symbol > $tmpfile2
	mv $tmpfile2 $tmpfile1
fi

mv $tmpfile1 $destfile

# 根据时间字段将数据还原
sed -i 's/\(\[[0-9].\{11\}\]\)/\n\1/g' $destfile

# 简化字段
egrep $grepfield $destfile > $tmpfile1

# 简化后的字段归整
if [ $4 -eq 0 ]
then
	sed -i 's/^\[[^]]*]//g' $tmpfile1
	awk -F '(' '{print $2}' $tmpfile1 | sed 's/)//g' > $tmpfile2
	sort -n $tmpfile2 | uniq > $simplefile
else
	sed -i 's/\[Type\]\(.*\)/\[Type\]/' $tmpfile1
	sed -i 's/$/,/g' $tmpfile1
	sed -i 's/--------<STR>//g' $tmpfile1
	sed -i 's/------<STR>//g' $tmpfile1
	tr -d '\n' < $tmpfile1 | sed 's/\(\[[^]]*]\[Type]\)/\n\1/g' > $simplefile
	sed -i 's/,\[[0-9].\{11\}\]/,/g' $simplefile
	sed -i 's/\[Type\]//' $simplefile
	sed -i 's/,$//g' $simplefile
fi

if [ -f $tmpfile1 ]
then
	rm $tmpfile1
fi

if [ -f $tmpfile2 ]
then
	rm $tmpfile2
fi
