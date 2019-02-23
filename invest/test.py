import tushare as ts
print '\nhigh wave stocks'
basicinfo = ts.get_stock_basics()
for line in basicinfo:
 print line

basicinfo.loc[((basicinfo.index >= u'600000') | (basicinfo.index < u'100000')) & (basicinfo['timeToMarket'] < 20160218) & (basicinfo['pe'] > 0) & (basicinfo['pe'] < 20) & (basicinfo['bvps']*basicinfo['totals']*basicinfo['pb'] < 50)].to_csv('./basicinfo.csv')

histdata = ts.get_hist_data('601595',start='2019-02-18',end='2019-02-22')
print histdata

rownum = len(histdata)

lastprice = 0
for price in histdata[0:1]['high']:
 lastprice = price

#copy close to a list
newcloselist = []
closelist = histdata['close']
for price in closelist:
 print price
 newcloselist.append(price)

newcloselist[0] = lastprice
newcloselist.reverse()
print newcloselist
