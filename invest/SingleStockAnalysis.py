import sys
import tushare as ts


#handle input parameters
print('Script File Name:' + sys.argv[0])

if 4 > len(sys.argv):
    print('Usage:python SingleStockAnalysis.py code starttime endtime')
    exit()

print('Code:' + sys.argv[1])
print('StartTime:' + sys.argv[2])
print('EndTime:' + sys.argv[3])

indexdata = ts.get_hist_data('sh', start=sys.argv[2], end=sys.argv[3])
histdata = ts.get_hist_data(sys.argv[1], start=sys.argv[2], end=sys.argv[3])

if histdata is None:
    print('Get histdata failed!')
    exit()
if 1 < len(histdata):
    print('StockCode:' + sys.argv[1])
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

    if meanwave > 0:
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
        while currentindex < len(histdata):
            investcount = 0
            currentprofitsum = 0
            for i in range(startindex, currentindex):
                investcount += 1
                currentprofitloss = 0.0
                if 5 == len(sys.argv):
                    currentprofitloss = (highlist[currentindex]/closelist[i] - 1)*1000
                else:
                    currentprofitloss = (closelist[currentindex]/closelist[i] - 1)*1000
                currentprofitsum += currentprofitloss
            if currentprofitsum < 5:
                currentindex += 1
            else:
                print('CurrentProfitSum:' + str(currentprofitsum))
                print('StartIndex:' + str(startindex) + ' CurrentIndex:' + str(currentindex) + ' UseTime:' + str(investcount))
                startindex = currentindex
                currentindex += 1
                if investcount > 10:
                    print('UseTime:' + str(investcount))
                    
        #compute strong weak
        strongcount = 0.0
        if len(histdata) == len(indexdata):
            for i in range(0, len(histdata)):
                if histdata[i:i+1]['p_change'].values[0] > indexdata[i:i+1]['p_change'].values[0]:
                    strongcount += 1
        strongrate = strongcount/len(indexdata)

        #print the result
        print('StockCode:' + sys.argv[1])
        print('MeanWave:' + '%.2f' % meanwave)
        print('HighWave:' + '%.2f' % highwave)
        print('InvestCount:' + '%d' % investcount)
        print('ProfitLoss:' + '%.2f' % currentprofitsum)
        print('Percent:' + '%.2f' % (currentprofitsum/investcount/10))
        print('StrongRate:' + '%.2f' % strongrate)
        print('\n')
