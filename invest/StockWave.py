import sys
import tushare as ts

#handle input parameters
print('Script File Name:' + sys.argv[0])

if 4 != len(sys.argv):
    print('Usage:python HighWaveStock.py starttime endtime MinMeanWeave')
    exit()

print('StockCode:' + sys.argv[1])
print('StartTime:' + sys.argv[2])
print('EndTime:' + sys.argv[3])

histdata = ts.get_hist_data(sys.argv[1], start=sys.argv[2], end=sys.argv[3])
if histdata is None:
    exit()
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
    print('Current totalprofit:' +str(currentprofitsum))
    print('Current meanwave:' + str(meanwave))
