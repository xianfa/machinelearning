import sys
import tushare as ts


#handle input parameters
print 'Script File Name:', sys.argv[0]

if 4 != len(sys.argv):
 print 'Usage:python HighWaveStock.py starttime endtime MinMeanWeave'
 exit()

print 'StartTime:', sys.argv[1]
print 'EndTime:', sys.argv[2]
print 'MinMeanWave:', sys.argv[3]

#get all the stock code then get everyone history data and handle it
basicinfo = ts.get_stock_basics()
#handle everyone stock
weaves = {}
profitloss = {}
for code in basicinfo.index:
 histdata = ts.get_hist_data(code, start=sys.argv[1], end=sys.argv[2])
 if histdata is None:
  continue
 if 1 < len(histdata):
  curentwavesum = 0
  currentprofitsum = 0
  for i in range(1, len(histdata)):
   growwave = abs(histdata[i-1:i]['high'].values[0]/histdata[i:i+1]['close'].values[0] - 1)
   belowwave = abs(histdata[i-1:i]['low'].values[0]/histdata[i:i+1]['close'].values[0] - 1)
   swingwave = (histdata[i-1:i]['high'].values[0] - histdata[i-1:i]['low'].values[0])/histdata[i:i+1]['close'].values[0]
   maxwave = growwave
   if belowwave > maxwave:
    maxwave = belowwave
   if swingwave > maxwave:
    maxwave = swingwave
   curentwavesum += maxwave
   currentprofitloss = (histdata[0:1]['close'].values[0]/histdata[i:i+1]['close'].values[0] - 1)*100
   currentprofitsum += currentprofitloss
  meanwave = curentwavesum/(len(histdata)-1)*100
  weaves[code] = meanwave
  print code, ',', currentprofitsum
  profitloss[code] = currentprofitsum

print '\nHigh weave stocks'
for key in weaves:
 if weaves[key] > float(sys.argv[3]):
  print key, ',', weaves[key]

print '\nBig loss stocks'
for key in profitloss:
 if profitloss[key] < 0:
  print key, ',', profitloss[key]

basicinfo.loc[((basicinfo.index >= u'600000') | (basicinfo.index < u'100000')) & (basicinfo['timeToMarket'] < 20160218) & (basicinfo['pe'] > 0) & (basicinfo['pe'] < 20) & (basicinfo['bvps']*basicinfo['totals']*basicinfo['pb'] < 50)].to_csv('./basicinfo.csv')

histdata = ts.get_hist_data('601595',start='2016-09-07',end='2016-09-20')
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
