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
print('StockCode,MeanWave,HighWave,InvestCount,ProfitLoss,Percent')
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
            highlist = histdata['high'].values.tolist()
            closelist.reverse()
            highlist.reverse()

            investcount = 0
            profitloss = 0
            
            startindex = 0
            currentindex = 1
            investcount = 0
            currentprofitsum = 0
            histinvestinfo = ''
            while currentindex < len(histdata):
                investcount = 0
                currentprofitsum = 0
                for i in range(startindex, currentindex):
                    investcount += 1
                    currentprofitloss = (highlist[currentindex]/closelist[i] - 1)*1000
                    currentprofitsum += currentprofitloss
                if currentprofitsum < 0:
                    currentindex += 1
                else:
                    startindex = currentindex
                    currentindex += 1
                    if investcount > 10:
                        histinvestinfo += 'UseTime:' + str(investcount) + '\n'

            currentprofitsum = 0
            currentindex = len(histdata) - 1
            for i in range(startindex, currentindex):
                currentprofitloss = (closelist[currentindex]/closelist[i] - 1)*1000
                currentprofitsum += currentprofitloss

            #print the result
            if(currentprofitsum < -0.1) & (investcount >= 3):
                print(code + ',' + '%.2f' % meanwave + ',' + '%.2f' % highwave + ',' + '%d' % investcount + ',' + '%.2f' % currentprofitsum + ',' + '%.2f' % (currentprofitsum/investcount/10))
                #print(histinvestinfo)
