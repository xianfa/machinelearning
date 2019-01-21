#我正在减肥，想着不妨用画图的方式把自己的体重数据显示出来，也刚好学习下画图的使用
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

weight = [217.8,216.1,217,213.3,212.8,214.2,213.4,211.3,211.6,211.2,210.2,210.7,210,209,208.5,208.6,208.7,207.8,207.2,204.9,203.4,204.6,204.7,205,205.2,203.2,203.7,204.2,205.8,205.2]
x = np.linspace(0,len(weight)-1, len(weight))
y = np.array(weight)

plt.plot(x, y)
plt.title('Weight change chart', fontsize=20)
plt.savefig('./test.jpg')
plt.show()
