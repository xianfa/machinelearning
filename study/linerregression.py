import tensorflow as tf
import numpy as np
import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#样本数据
x_data = np.random.rand(20).astype(np.float32)
#y_data = x_data*3.0 + 5.0
noise = np.random.rand(20).astype(np.float32)*0.1
#y_data = x_data*3.0 + 5.0 + noise
y_data = x_data*x_data*3.0 + 5.0 + noise

#打印样本数据信息
print('\nsample data length:' + str(len(x_data)) + '\n')
print('x_data:' + str(x_data) + '\n')
print('noise:' + str(noise) + '\n')
print('y_data:' + str(y_data) + '\n')

#初始参数
Weights = tf.Variable(tf.random_uniform([1], - 1.0, 1.0))
biases = tf.Variable(tf.zeros([1]))

#估计方程
#y = Weights*x_data + biases
y = Weights*x_data*x_data + biases;

#训练方法使用梯度下降方法 训练目标是使方差最小(差方得均值是不是是不是就是方差 记不大清)
loss = tf.reduce_mean(tf.square(y-y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

#初始化变量
init = tf.global_variables_initializer()

#用Session来执行 前面相当于指定怎么做，这里才是真正的执行
sess = tf.Session()
sess.run(init)

traincount = 100
printstep = 1
#做traincount次迭代(这里称为训练), 打印出当前拟合的参数
print('weights:' + str(sess.run(Weights)))
print('biases:' + str(sess.run(biases)))
for step in range(traincount):
    sess.run(train)
    if(0 == step % printstep):
        print(step,sess.run(Weights), sess.run(biases))
