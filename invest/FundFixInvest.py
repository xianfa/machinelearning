import sys
import matplotlib
import numpy as np
import pandas as pd
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

def printpolicyinfo(policyname, profitlossarray, totalinarray, percentarray, lastprice):
    print('\nPolicy Name:' + policyname)

    profitloss = 'PROFLOSS'
    totalin = ' TOTALIN'
    percent = ' PERCENT'

    for i in range(0, len(profitlossarray)):
        profitloss += formatstr('%.2f' % profitlossarray[i], 8)
        totalin += formatstr('%.1f' % totalinarray[i], 8)
        percent += formatstr('%.3f' % percentarray[i], 8)
    
    print(profitloss)
    print(totalin)
    print(percent)

    totalincount = len(percentarray)
    lastpercent = percentarray[totalincount-1]
    if lastpercent < 0:
        goalrisepercent = -100*lastpercent/(100+lastpercent)
        print('\nGoal price:' + '%.2f' %(lastprice/(1+lastpercent/100)))
        print('Goal rise percent:' + '%.2f' %(goalrisepercent))
        print('Total in:' + '%.2f' %(totalinarray[totalincount-1]))
        print('Goal profit:' + '%.2f' %(totalinarray[totalincount-1]*goalrisepercent/100))
        print('\n')



if __name__ == '__main__':
    
    #handle input parameters
    print('\n')
    print('Script File Name:'+ sys.argv[0])
    
    if 2 > len(sys.argv):
        print('Usage:python FundFixedInvest.py FileName [high]')
        print('\n')
        exit()
    
    #print input parameters
    print('FileName:' + sys.argv[1])
    
    #get the history price
    histdata = pd.read_csv('./FundData/' + sys.argv[1] + '.csv')
    if 0 == len(histdata):
        print('Get histdata Failed')
        print('\n')
        exit()
    
    #handle price list
    lastprice = histdata[-1:]['high'].values[0]
    newcloselist = histdata['close'].values.tolist()

    print(lastprice)
    
    #change the last close price to high price
    if 2 < len(sys.argv):
        newcloselist[-1] = lastprice
    lastprice = newcloselist[-1]
    newcloselist.append(lastprice)
    
    print(newcloselist)
    print('\n')
    
    #compute and print invest info
    for i in range(0, len(newcloselist)):
        strprice = '%.3f' % newcloselist[i]
        strline = ''
        strline += formatstr(strprice, 8)
        
        #empty column handle
        for empty in range(0, i):
            strline += '        '
            
        #profit and loss handle
        for j in range(i+1, len(newcloselist)):
            profit = newcloselist[j]/newcloselist[i] - 1
            profit *= 100
            strprofit = '%.3f' % profit
            strline += formatstr(strprofit, 8)
        print(strline)

    #compute profitloss totalin and percent for every policy 
    fixprofitlossarray = []
    fixtotalinarray = []
    fixpercentarray = []

    fixaddprofitlossarray = []
    fixaddtotalinarray = []
    fixaddpercentarray = []

    #fix in value is 1000
    currentfixtotalin = 0
    currentfixaddtotalin = 0

    fixstockcount = 0
    fixaddstockcount = 0
    for i in range(1, len(newcloselist)):

        #compute invest money
        currentfixin = 1000
        currentfixaddin = 1000
        if i > 1 and newcloselist[i] < newcloselist[0]:
            currentfixaddin += (newcloselist[0]/newcloselist[i-1]-1)*1000
        
        #all invest money
        currentfixtotalin += currentfixin
        currentfixaddtotalin += currentfixaddin

        fixstockcount += currentfixin/newcloselist[i-1]
        fixaddstockcount += currentfixaddin/newcloselist[i-1]

        fixtotalinarray.append(currentfixtotalin)
        fixaddtotalinarray.append(currentfixaddtotalin)
        
        #compute profitloss
        profitloss = fixstockcount*newcloselist[i] - currentfixtotalin
        fixprofitlossarray.append(profitloss)
        fixpercentarray.append(100*profitloss/currentfixtotalin)

        profitloss = fixaddstockcount*newcloselist[i] - currentfixaddtotalin
        fixaddprofitlossarray.append(profitloss)
        fixaddpercentarray.append(100*profitloss/currentfixaddtotalin)

    printpolicyinfo('Fix Invest', fixprofitlossarray, fixtotalinarray, fixpercentarray, lastprice)
    printpolicyinfo('Fix Add Invest', fixaddprofitlossarray, fixaddtotalinarray, fixaddpercentarray, lastprice)
    
    x = np.linspace(0,len(fixpercentarray)-1, len(fixpercentarray))
    y = np.array(fixpercentarray)
    
    plt.plot(x, y)
    plt.title('fixinvest profitloss percent chart', fontsize=20)
    plt.savefig('./Fundfixinvest.jpg')
    plt.show()

