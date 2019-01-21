import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#根据索引单词组成句子
def decode_review(reverse_word_index, text):
    return ' '.join([reverse_word_index.get(i, '?') for i in text])

def my_decode_review(reverse_word_index, text):
    result = ''
    for i in text:
        result += ' ' + reverse_word_index[i]
    return result

#画出训练和验证的val以及loss曲线
def drawfigure(epochs, bodata, bolabel, bdata, blabel, title, xlabel, ylabel, savefilename):
    plt.clf()   # clear figure
    # "bo" is for "blue dot"
    plt.plot(epochs, bodata, 'bo', label=bolabel)
    # b is for "solid blue line"
    plt.plot(epochs, bdata, 'b', label=blabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(savefilename)


#获取训练和测试数据
imdb = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

#打印一个实际的测试数据，以便了解原始数据形式
exampleindex = 10
print('\ntrain_data example:' + str(train_data[exampleindex]) + '\n')
print('\ntrain_label example:' + str(train_labels[exampleindex]) + '\n')

#key:单词 value:单词索引整数值
word_index = imdb.get_word_index()

#0-3索引值保留，原来的索引值均加3，并加上保留的三个，这里有个疑问，在数据处理的时候为什么不直接处理好，在这里处理下感觉怪怪的。
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2  # unknown
word_index["<UNUSED>"] = 3

#一个反向索引，key：单词索引整数值 value：单词
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

#根据句子单词索引，建立原来的句子，打印出来，直观的了解数据。
examplecomment = decode_review(reverse_word_index, train_data[exampleindex])
#examplecomment = my_decode_review(reverse_word_index, train_data[exampleindex])
print('example comment:' + examplecomment + '\n')

#格式化处理数据，统一处理为256元素，长度不足的后面补0，大于256的，截取后面的256个单词，这样比较合理，一般影评前面会讲剧情，后面说是否推荐。
#当然了对于先说是否推荐，后面说内容的数据，显然这样处理就不合适
train_data = keras.preprocessing.sequence.pad_sequences(train_data,
        value=word_index["<PAD>"],
        padding='post',
        maxlen=256)

test_data = keras.preprocessing.sequence.pad_sequences(test_data,
        value=word_index["<PAD>"],
        padding='post',
        maxlen=256)

#input shape is the vocabulary count used for the movie reviews (10,000 words)
#这里不明白，这里是指用的词汇量不超过10000个，还是指的单篇评论不超过10000单词
vocab_size = 10000

#神经网络模型 对比基本分类，又学习到一种写法。
model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

#打印出模型概要信息，这个好，基本分类也要加上
model.summary()

#编译
model.compile(optimizer=tf.train.AdamOptimizer(),
        loss='binary_crossentropy',
        metrics=['accuracy'])

#前一万个数据作为验证数据，后面的数据作为训练数据 训练模型
x_val = train_data[:10000]
partial_x_train = train_data[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

history = model.fit(partial_x_train,
        partial_y_train,
        epochs=40,
        batch_size=512,
        validation_data=(x_val, y_val),
        verbose=1)

#评估测试数据 并打印评估结果
results = model.evaluate(test_data, test_labels)
print(results)

#作图需要的数据
history_dict = history.history
acc = history_dict['acc']
val_acc = history_dict['val_acc']
loss = history_dict['loss']
val_loss = history_dict['val_loss']
epochs = range(1, len(acc) + 1)

#画出训练和验证的loss和acc曲线
drawfigure(epochs, loss, 'Training loss', val_loss, 'Validation loss', 'Training and validation loss', 'Epochs', 'Loss', './epochs-loss.jpg')
drawfigure(epochs, acc, 'Training acc', val_acc, 'Validation acc', 'Training and validation accuracy', 'Epochs', 'Accuracy', './epochs-accuracy.jpg')

