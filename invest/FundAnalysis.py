import sys
import pandas as pd
import tushare as ts


#handle input parameters
print('Script File Name:' + sys.argv[0])

if 2 > len(sys.argv):
    print('Usage:python FundAnalysis.py fundcode [high]')
    exit()

print('Code:' + sys.argv[1])

histdata = pd.read_csv('./FundData/' + sys.argv[1] + '.csv', dtype={'high':float})
if histdata is None:
    print('Get histdata failed!')
    exit()
print(histdata['open'])
if 1 < len(histdata):
    print('StockCode:' + sys.argv[1])
    curentwavesum = 0.0
    currentprofitsum = 0.0
    highwave = 0.0
    for i in range(1, len(histdata)):
        growwave = abs(histdata[i:i+1]['high'].values[0]/histdata[i-1:i]['close'].values[0] - 1)
        belowwave = abs(histdata[i:i+1]['low'].values[0]/histdata[i-1:i]['close'].values[0] - 1)
        swingwave = (histdata[i:i+1]['high'].values[0] - histdata[i:i+1]['low'].values[0])/histdata[i-1:i]['close'].values[0]
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
                if 3 == len(sys.argv):
                    currentprofitloss = (highlist[currentindex]/closelist[i] - 1)*1000
                else:
                    currentprofitloss = (closelist[currentindex]/closelist[i] - 1)*1000
                currentprofitsum += currentprofitloss
            if currentprofitsum < 0:
                currentindex += 1
            else:
                startindex = currentindex
                currentindex += 1
                if investcount > 10:
                    print('UseTime:' + str(investcount))

        #print the result
        print('StockCode:' + sys.argv[1])
        print('MeanWave:' + '%.2f' % meanwave)
        print('HighWave:' + '%.2f' % highwave)
        print('InvestCount:' + '%d' % investcount)
        print('ProfitLoss:' + '%.2f' % currentprofitsum)
        print('Percent:' + '%.2f' % (currentprofitsum/investcount/10))
        print('\n')
