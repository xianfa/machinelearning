import sys
import tushare as ts


#handle input parameters
print('Script File Name:' + sys.argv[0])

if 4 != len(sys.argv):
    print('Usage:python HighWaveStock.py starttime endtime MinMeanWeave')
    exit()

print('StartTime:' + sys.argv[1])
print('EndTime:' + sys.argv[2])
print('MinMeanWave:' + sys.argv[3])

#get all the stock code then get everyone history data and handle it
basicinfo = ts.get_stock_basics()
#handle everyone stock

for code in basicinfo.index:
    histdata = ts.get_hist_data(code, start=sys.argv[1], end=sys.argv[2])
    if histdata is None:
        continue
    if 1 < len(histdata):
        curentwavesum = 0.0
        currentprofitsum = 0.0
        highwave = 0.0
        for i in range(1, len(histdata)):
            growwave = abs(histdata[i-1:i]['high'].values[0]/histdata[i:i+1]['close'].values[0] - 1)
            belowwave = abs(histdata[i-1:i]['low'].values[0]/histdata[i:i+1]['close'].values[0] - 1)
            swingwave = (histdata[i-1:i]['high'].values[0] - histdata[i-1:i]['low'].values[0])/histdata[i:i+1]['close'].values[0]
            maxwave = growwave
            if belowwave > maxwave:
                maxwave = belowwave
            if swingwave > maxwave:
                maxwave = swingwave
            if highwave < maxwave:
                highwave = maxwave
            curentwavesum += maxwave
        meanwave = curentwavesum/(len(histdata)-1)*100

        if meanwave > float(sys.argv[3]):
            #fix invest profitloss infomation
            closelist = histdata['close'].values.tolist()
            closelist.reverse()

            investcount = 0
            profitloss = 0
            
            startindex = 0
            currentindex = 1
            investcount = 0
            currentprofitsum = 0
            while currentindex < len(histdata):
                investcount = 0
                currentprofitsum = 0
                for i in range(startindex, currentindex):
                    investcount += 1
                    currentprofitloss = (closelist[currentindex]/closelist[i] - 1)*1000
                    currentprofitsum += currentprofitloss
                if currentprofitsum < 0:
                    currentindex += 1
                else:
                    startindex = currentindex
                    currentindex += 1

            #print the result
            if(currentprofitsum > -1000000000):
                print('StockCode:' + code)
                print('MeanWave:' + '%.2f' % meanwave)
                print('HighWave:' + '%.2f' % highwave)
                print('InvestCount:' + '%d' % investcount)
                print('ProfitLoss:' + '%.2f' % currentprofitsum)
                print('Percent:' + '%.2f' % (currentprofitsum/investcount/10))
                print('\n')


basicinfo.loc[((basicinfo.index >= u'600000') | (basicinfo.index < u'100000')) & (basicinfo['timeToMarket'] < 20160218) & (basicinfo['pe'] > 0) & (basicinfo['pe'] < 20) & (basicinfo['bvps']*basicinfo['totals']*basicinfo['pb'] < 50)].to_csv('./basicinfo.csv')

histdata = ts.get_hist_data('601595',start='2016-09-07',end='2016-09-20')
print(histdata)

rownum = len(histdata)

lastprice = 0
for price in histdata[0:1]['high']:
 lastprice = price

#copy close to a list
newcloselist = []
closelist = histdata['close']
for price in closelist:
 print(price)
 newcloselist.append(price)

newcloselist[0] = lastprice
newcloselist.reverse()
print(newcloselist)
