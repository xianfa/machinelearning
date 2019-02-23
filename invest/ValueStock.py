import sys
import tushare as ts

#handle input parameters
print '\n'
print 'Script File Name:', sys.argv[0]

if 4 != len(sys.argv):
 print 'Usage:python ValueStock.py startyear yearcount minroepercent'
 print '\n'
 exit()

print 'startyear:', sys.argv[1]
print 'yearcount:', sys.argv[2]
print 'minroepercent:', sys.argv[3]

for yearindex in range(0, int(sys.argv[2])):
 yeardata = ts.get_report_data(int(sys.argv[1])+yearindex, 4)
 print '\n'
 for i in range(0, len(yeardata)):
  if yeardata[i:i+1]['roe'].values[0] > float(sys.argv[3]):
   print yeardata[i:i+1]['code'].values
