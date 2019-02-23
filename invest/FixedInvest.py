import sys
import matplotlib
import numpy as np
import tushare as ts
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#handle input parameters
print('\n')
print('Script File Name:'+ sys.argv[0])

if 4 > len(sys.argv):
 print('Usage:python FixedInvest stockcode starttime endtime [high]')
 print('\n')
 exit()

print('StockCode:' + sys.argv[1])
print('StartTime:' + sys.argv[2])
print('EndTime:' + sys.argv[3])

#get the history price
histdata = ts.get_hist_data(sys.argv[1],start=sys.argv[2],end=sys.argv[3])
if 0 == len(histdata):
 print('Get histdata Failed')
 print('\n')
 exit()

lastprice = 0
for price in histdata[0:1]['high']:
 lastprice = price

#copy close to a list
newcloselist = []
closelist = histdata['close']
for price in closelist:
 newcloselist.append(price)

#change the last close price to high price
if 4 < len(sys.argv):
 newcloselist[0] = lastprice
lastprice = newcloselist[0]
newcloselist.reverse()
newcloselist.append(lastprice)

print(newcloselist)

for i in range(0, len(newcloselist)):
 strprice = '%.2f' % newcloselist[i]
 spacenum = 8-len(strprice)
 strline = ''
 for j in range(0, spacenum):
  strline += ' '
 strline += strprice


 #empty column handle
 for empty in range(0, i):
  strline += '        '

 #profit and loss handle
 for j in range(i+1, len(newcloselist)):
   profit = newcloselist[j]/newcloselist[i] - 1
   profit *= 100
   strprofit = '%.2f' % profit
   #space handle
   spacenum = 8-len(strprofit)
   for k in range(0, spacenum):
    strline += ' '
   strline += strprofit
 print(strline)

profitloss = 'PROFLOSS'
totalin = ' TOTALIN'
percent = ' PERCENT'

percentarray = []

for i in range(1, len(newcloselist)):
 strtotalin = '%d' % i
 spacenum = 8-len(strtotalin)
 for j in range(0, spacenum):
  totalin += ' '
 totalin += strtotalin

 totalprofitloss = 0
 for j in range(0, i):
  totalprofitloss += ((newcloselist[i]/newcloselist[j]-1)*100)
 strtotalprofitloss = '%.2f' % totalprofitloss
 spacenum = 8 - len(strtotalprofitloss)
 for j in range(0, spacenum):
  profitloss += ' '
 profitloss += strtotalprofitloss

 strpercent = '%.2f' % (totalprofitloss/i)
 percentarray.append(totalprofitloss/i)
 spacenum = 8 - len(strpercent)
 for j in range(0, spacenum):
  percent += ' '
 percent += strpercent

print(profitloss)
print(totalin)
print(percent)
print('\n')

x = np.linspace(0,len(percentarray)-1, len(percentarray))
y = np.array(percentarray)

plt.plot(x, y)
plt.title('fixinvest profitloss percent chart', fontsize=20)
plt.savefig('./test.jpg')
plt.show()

