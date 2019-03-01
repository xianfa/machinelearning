import sys
import tushare as ts

#handle input parameters
print('\nScript File Name:' + sys.argv[0])

if 4 != len(sys.argv):
 print('Usage:python ValueStock.py startyear yearcount minroepercent \n')
 exit()

print('startyear:' + sys.argv[1])
print('yearcount:' + sys.argv[2])
print('minroepercent:' + sys.argv[3])

stockminroe = {}
for yearindex in range(0, int(sys.argv[2])):
    print('\n')
    yeardata = ts.get_report_data(int(sys.argv[1])+yearindex, 4)

    for i in range(0, len(yeardata)):
        if yeardata[i:i+1]['code'].values[0] not in stockminroe:
            stockminroe[yeardata[i:i+1]['code'].values[0]] = yeardata[i:i+1]['roe'].values[0]
        elif stockminroe[yeardata[i:i+1]['code'].values[0]] > yeardata[i:i+1]['roe'].values[0]:
            stockminroe[yeardata[i:i+1]['code'].values[0]] = yeardata[i:i+1]['roe'].values[0]
            
for key in stockminroe:
    if(stockminroe[key] > float(sys.argv[3])):
        print(key + ':' + str(stockminroe[key]))
