import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        print('.', end='')
        if (epoch+1) % 100 == 0:
            print(epoch+1)

def build_model():
    model = keras.Sequential([
    layers.Dense(64, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation=tf.nn.relu),
    layers.Dense(1)
    ])
    
    optimizer = tf.train.RMSPropOptimizer(0.001)
    model.compile(loss='mse',
            optimizer=optimizer,
            metrics=['mae', 'mse'])
    return model

def plot_history(hist, savefileprefix):
    plt.clf()
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['mean_absolute_error'],
            label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
            label = 'Val Error')
    plt.legend()
    plt.ylim([0,5])
    plt.savefig('./' + savefileprefix + '-epoch-meanabserror.jpg')
    
    plt.clf()
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(hist['epoch'], hist['mean_squared_error'],
            label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_squared_error'],
            label = 'Val Error')
    plt.legend()
    plt.ylim([0,20])
    plt.savefig('./' + savefileprefix + '-epoch-meansquarederror.jpg')

def get_dataset():
    #download first if not exist data
    dataset_path = keras.utils.get_file("auto-mpg.data", "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")
    column_names = ['MPG','Cylinders','Displacement','Horsepower','Weight', 'Acceleration', 'Model Year', 'Origin']
    
    #read data from csvfile
    raw_dataset = pd.read_csv(dataset_path, names=column_names, na_values = "?", comment='\t', sep=" ", skipinitialspace=True)
    
    #copy data and drop useless data
    dataset = raw_dataset.copy()
    dataset = dataset.dropna()
    
    #deal with origin
    origin = dataset.pop('Origin')
    dataset['USA'] = (origin == 1)*1.0
    dataset['Europe'] = (origin == 2)*1.0
    dataset['Japan'] = (origin == 3)*1.0
    return dataset

if __name__ == '__main__':
    #get data and prehandle the data
    dataset = get_dataset()
    
    #divid into train and test data
    train_dataset = dataset.sample(frac=0.8,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    
    #draw the train data
    plt.clf()
    sns.pairplot(train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde")
    plt.savefig('./pairplot.jpg')
    
    #prehandle train_stats used to normalize train_data and test_data
    train_stats = train_dataset.describe()
    train_stats.pop("MPG")
    train_stats = train_stats.transpose()
    print('\ntrain_status:\n' + str(train_stats))
    
    #target values
    train_labels = train_dataset.pop('MPG')
    test_labels = test_dataset.pop('MPG')
    
    #normalize
    normed_train_data = (train_dataset - train_stats['mean']) / train_stats['std']
    normed_test_data = (test_dataset - train_stats['mean']) / train_stats['std']

    #farmiliar with the data, tail head inspect the last or ahead 5 data.
    print('\nnormed_train_data.tail:\n' + str(normed_train_data.tail()))
    
    #build model
    model = build_model()
    model.summary()
    
    #test predict.question:Can it predict without training? Is it right? Whether just the primitive parameters?
    example_batch = normed_train_data[:10]
    example_result = model.predict(example_batch)
    print('simple predict with out training:\n' + str(example_result))

    #training all model
    EPOCHS = 1000
    print('\ntrain all epoch start:')
    history = model.fit(
            normed_train_data, train_labels,
            epochs=EPOCHS, validation_split = 0.2, verbose=0,
            callbacks=[PrintDot()])
    print('\ntrain all epoch finish')

    #handle training history data
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    
    #draw train epoch info
    plot_history(hist, 'trainall')

    #training partial model
    model = build_model()
    # The patience parameter is the amount of epochs to check for improvement
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

    print('\ntrain partial epoch start:')
    earlystophistory = model.fit(
            normed_train_data, train_labels,
            epochs=EPOCHS,validation_split = 0.2, verbose=0,
            callbacks=[early_stop, PrintDot()])
    print('\ntrain partial epoch finish')
    
    #handle training history data
    earlystophist = pd.DataFrame(earlystophistory.history)
    earlystophist['epoch'] = earlystophistory.epoch

    #draw train epoch info
    plot_history(earlystophist, 'trainpatience')
    
    loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
    print("\nTesting set Mean Abs Error: {:5.2f} MPG".format(mae))
    
    #predict the test_data
    test_predictions = model.predict(normed_test_data).flatten()
    
    #draw truevalue and predictions
    plt.clf()
    plt.scatter(test_labels, test_predictions)
    plt.xlabel('True Values [MPG]')
    plt.ylabel('Predictions [MPG]')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0,plt.xlim()[1]])
    plt.ylim([0,plt.ylim()[1]])
    plt.plot([-100, 100], [-100, 100])
    plt.savefig('./truevalue-predictions.jpg')
    
    #draw prediction error and its count
    plt.clf()
    error = test_predictions - test_labels
    plt.hist(error, bins = 25)
    plt.xlabel("Prediction Error [MPG]")
    plt.ylabel("Count")
    plt.savefig('./predictionerror-count.jpg')
