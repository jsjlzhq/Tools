splitPacket.py	    JMS2QPID.FANOUT.FULL队列消息分包
参数:               param1 输入文件名
				    param2 输出文件名
					
spligPacket_bond.py BOND_OFFER_PUSH_V5/BOND_DEAL_PUSH_V5队列消息分包
参数:				param1 输入文件名
				    param2 输出文件名
					
filter_bond.sh      筛选报价
参数：				param1 输入文件名
					param2 输出文件名
					param3 类型 0-bondoffer 1-bonddeal 2-jms2qpid筛选offer数据 3-jms2qpid筛选deal数据
					param4 简化类型 0-只筛选出id 1-筛选多个字段
					param5 剔除NCD券 0-不需要剔除 1-需要剔除
					param6 brokerId
					param7 goodsCode
					param8 offer中symbol,bid=1,ofr=-1
param3 ~ param8以下情况：
0 0 0					// bondOffer 只筛选出id 不剔除NCD 
0 0 0 1					// bondOffer 只筛选出id 不剔除NCD BrokerID
0 0 0 1 160019			// bondOffer 只筛选出id 不剔除NCD BrokerID goodsCode
0 0 0 1 160019 -1		// bondOffer 只筛选出id 不剔除NCD BrokerID goodsCode bid/ofr
0 1 0					// bondOffer 筛出多个字段 不剔除NCD
0 1 0 1					// bondOffer 筛出多个字段 不剔除NCD BrokerID
0 1 0 1 160019			// bondOffer 筛出多个字段 不剔除NCD BrokerID goodsCode
0 1 0 1 160019 -1		// bondOffer 筛出多个字段 不剔除NCD BrokerID goodsCode bid/ofr
0 0 1					// bondOffer 只筛选出id 剔除NCD 
0 0 1 1					// bondOffer 只筛选出id 剔除NCD BrokerID
0 0 1 1 160019			// bondOffer 只筛选出id 剔除NCD BrokerID goodsCode
0 0 1 1 160019 -1		// bondOffer 只筛选出id 剔除NCD BrokerID goodsCode bid/ofr
0 1 1					// bondOffer 筛出多个字段 剔除NCD
0 1 1 1					// bondOffer 筛出多个字段 剔除NCD BrokerID
0 1 1 1 160019			// bondOffer 筛出多个字段 剔除NCD BrokerID goodsCode
0 1 1 1 160019 -1		// bondOffer 筛出多个字段 剔除NCD BrokerID goodsCode bid/ofr

1 0 0					// bondDeal 只筛选出id 不剔除NCD 
1 0 0 1					// bondDeal 只筛选出id 不剔除NCD BrokerID
1 0 0 1 160019			// bondDeal 只筛选出id 不剔除NCD BrokerID goodsCode
1 1 0					// bondDeal 筛出多个字段 不剔除NCD
1 1 0 1					// bondDeal 筛出多个字段 不剔除NCD BrokerID
1 1 0 1 160019			// bondDeal 筛出多个字段 不剔除NCD BrokerID goodsCode
1 0 1					// bondDeal 只筛选出id 剔除NCD 
1 0 1 1					// bondDeal 只筛选出id 剔除NCD BrokerID
1 0 1 1 160019			// bondDeal 只筛选出id 剔除NCD BrokerID goodsCode
1 1 1					// bondDeal 筛出多个字段 剔除NCD
1 1 1 1					// bondDeal 筛出多个字段 剔除NCD BrokerID
1 1 1 1 160019			// bondDeal 筛出多个字段 剔除NCD BrokerID goodsCode

2 0 0					// jms2qpid-offer 只筛选出id 不剔除NCD 
2 0 0 1					// jms2qpid-offer 只筛选出id 不剔除NCD BrokerID
2 0 0 1 160019			// jms2qpid-offer 只筛选出id 不剔除NCD BrokerID goodsCode
2 0 0 1 160019 -1		// jms2qpid-offer 只筛选出id 不剔除NCD BrokerID goodsCode bid/ofr
2 1 0					// jms2qpid-offer 筛出多个字段 不剔除NCD
2 1 0 1					// jms2qpid-offer 筛出多个字段 不剔除NCD BrokerID
2 1 0 1 160019			// jms2qpid-offer 筛出多个字段 不剔除NCD BrokerID goodsCode
2 1 0 1 160019 -1		// jms2qpid-offer 筛出多个字段 不剔除NCD BrokerID goodsCode bid/ofr
2 0 1					// jms2qpid-offer 只筛选出id 剔除NCD 
2 0 1 1					// jms2qpid-offer 只筛选出id 剔除NCD BrokerID
2 0 1 1 160019			// jms2qpid-offer 只筛选出id 剔除NCD BrokerID goodsCode
2 0 1 1 160019 -1		// jms2qpid-offer 只筛选出id 剔除NCD BrokerID goodsCode bid/ofr
2 1 1					// jms2qpid-offer 筛出多个字段 剔除NCD
2 1 1 1					// jms2qpid-offer 筛出多个字段 剔除NCD BrokerID
2 1 1 1 160019			// jms2qpid-offer 筛出多个字段 剔除NCD BrokerID goodsCode
2 1 1 1 160019 -1		// jms2qpid-offer 筛出多个字段 剔除NCD BrokerID goodsCode bid/ofr

3 0 0					// jms2qpid_deal 只筛选出id 不剔除NCD 
3 0 0 1					// jms2qpid_deal 只筛选出id 不剔除NCD BrokerID
3 0 0 1 160019			// jms2qpid_deal 只筛选出id 不剔除NCD BrokerID goodsCode
3 1 0					// jms2qpid_deal 筛出多个字段 不剔除NCD
3 1 0 1					// jms2qpid_deal 筛出多个字段 不剔除NCD BrokerID
3 1 0 1 160019			// jms2qpid_deal 筛出多个字段 不剔除NCD BrokerID goodsCode
3 0 1					// jms2qpid_deal 只筛选出id 剔除NCD 
3 0 1 1					// jms2qpid_deal 只筛选出id 剔除NCD BrokerID
3 0 1 1 160019			// jms2qpid_deal 只筛选出id 剔除NCD BrokerID goodsCode
3 1 1					// jms2qpid_deal 筛出多个字段 剔除NCD
3 1 1 1					// jms2qpid_deal 筛出多个字段 剔除NCD BrokerID
3 1 1 1 160019			// jms2qpid_deal 筛出多个字段 剔除NCD BrokerID goodsCode
