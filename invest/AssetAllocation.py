import sys
import matplotlib
import numpy as np
import tushare as ts
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#format string with space
def formatstr(strsource, totallen):
    str = ''
    spacenum = totallen - len(strsource)
    for k in range(0, spacenum):
        str += ' '
    str += strsource
    return str

def printpolicyinfo(policyname, stockassetarray, cashassetarray, totalassetarray):
    print('\nPolicy Name:' + policyname)

    stockasset = 'StockAsset'
    cashasset = ' CashAsset'
    totalasset = 'TotalAsset'

    for i in range(0, len(stockassetarray)):
        stockasset += formatstr('%.2f' % stockassetarray[i], 12)
        cashasset += formatstr('%.2f' % cashassetarray[i], 12)
        totalasset += formatstr('%.2f' % totalassetarray[i], 12)
    
    print(stockasset)
    print(cashasset)
    print(totalasset)

if __name__ == '__main__':
    
    #handle input parameters
    print('\n')
    print('Script File Name:'+ sys.argv[0])
    
    if 4 > len(sys.argv):
        print('Usage:python AssetAllocation.py stockcode starttime endtime')
        print('\n')
        exit()
    
    #print input parameters
    print('StockCode:' + sys.argv[1])
    print('StartTime:' + sys.argv[2])
    print('EndTime:' + sys.argv[3])
    print('\n')
    
    #get the history price
    histdata = ts.get_hist_data(sys.argv[1],start=sys.argv[2],end=sys.argv[3])
    if 0 == len(histdata):
        print('Get histdata Failed')
        print('\n')
        exit()
    
    #handle price list
    newcloselist = histdata['close'].values.tolist()
    newcloselist.reverse()
    
    print(newcloselist)
    print('\n')

    #AssetAllocation
    TotalAsset = 1000000
    StockRatio = 0.5
    StockRatioStockAsset = TotalAsset * StockRatio
    StockRatioCashAsset = TotalAsset - StockRatioStockAsset
    
    StockRatioTotalAssetArray = []
    StockRatioStockAssetArray = []
    StockRatioCashAssetArray = []
    StockRatioTotalAssetArray.append(TotalAsset)
    StockRatioStockAssetArray.append(StockRatioStockAsset)
    StockRatioCashAssetArray.append(StockRatioCashAsset)

    for i in range(1, len(newcloselist)):
        StockRatioProfit = (newcloselist[i]/newcloselist[i-1] - 1) * StockRatioStockAsset
        StockRatioStockAsset += StockRatioProfit
        StockRatioStockAsset -= StockRatioProfit * StockRatio
        StockRatioCashAsset += (1 - StockRatio) * StockRatioProfit

        StockRatioTotalAssetArray.append(StockRatioStockAsset + StockRatioCashAsset)
        StockRatioStockAssetArray.append(StockRatioStockAsset)
        StockRatioCashAssetArray.append(StockRatioCashAsset)
    
    printpolicyinfo('Asset Allocation Fix Ratio', StockRatioStockAssetArray, StockRatioCashAssetArray, StockRatioTotalAssetArray)
    
    x = np.linspace(0,len(StockRatioTotalAssetArray)-1, len(StockRatioTotalAssetArray))
    y = np.array(StockRatioTotalAssetArray)
    
    plt.plot(x, y)
    plt.title('fixinvest profitloss percent chart', fontsize=20)
    plt.savefig('./StockRatioAsset.jpg')
    plt.show()

