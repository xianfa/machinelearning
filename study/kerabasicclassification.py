# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def saveimg(imagearray, index):
    plt.figure()
    plt.imshow(imagearray[index])
    plt.colorbar()
    plt.grid(False)
    plt.savefig('./test' + str(index) + '.jpg')

def saveimgs(imgwidth, imgheight, subrows, subcols, imagearray, labelindexarray, labels, savefilename):
    plt.figure(figsize=(imgwidth, imgheight))
    for i in range(subrows*subcols):
        plt.subplot(subrows, subcols, i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(imagearray[i], cmap=plt.cm.binary)
        plt.xlabel(labels[labelindexarray[i]])
        plt.savefig(savefilename)

def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'
    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
        100*np.max(predictions_array),
        class_names[true_label]),
        color=color)

def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

def savesingleprediction(index, images, labels, predictions):
    plt.figure(figsize=(6,3))
    plt.subplot(1,2,1)
    plot_image(index, predictions, labels, images)
    plt.subplot(1,2,2)
    plot_value_array(index, predictions,  labels)
    plt.savefig('prediction' + str(index) + '.jpg')

def savepredictions(num_rows, num_cols, images, labels, predictions, savefilename):
    num_images = num_rows*num_cols
    plt.figure(figsize=(2*2*num_cols, 2*num_rows))
    for i in range(num_images):
        plt.subplot(num_rows, 2*num_cols, 2*i+1)
        plot_image(i, predictions, labels, images)
        plt.subplot(num_rows, 2*num_cols, 2*i+2)
        plot_value_array(i, predictions, labels)
    plt.savefig(savefilename)

if __name__ == '__main__':
    #get data
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    #save a train image
    for i in range(1):
        saveimg(train_images, i)

    #change value to range [0, 1]
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    #save train images
    saveimgs(10, 10, 5, 5, train_images, train_labels, class_names, 'first25.jpg')

    #neural network training
    model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(10, activation=tf.nn.softmax)
            ])
    model.compile(optimizer=tf.train.AdamOptimizer(),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=1)

    #use test data to test
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('Test accuracy:', test_acc)

    #use test data to predict
    predictions = model.predict(test_images)

    #save predict result and check it
    savesingleprediction(5, test_images, test_labels, predictions)
    savesingleprediction(12, test_images, test_labels, predictions)
    savepredictions(5, 3, test_images, test_labels, predictions, 'predictiontotal.jpg')

    #predict single one example
    img = test_images[0]
    img = (np.expand_dims(img,0))

    #predict result
    predictions_single = model.predict(img)

    #save file to check
    savesingleprediction(0, test_images, test_labels, predictions_single)
