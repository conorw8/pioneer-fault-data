from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras.optimizers import Adam
from keras.models import model_from_yaml
import matplotlib.pyplot as plt
from keras import losses
import numpy as np
import tensorflow as tf
import os
import csv

tf.reset_default_graph()
#number of epochs for training
num_epochs = 1
#number of possible labels
n_labels = 3
#number of features
n_features = 4
#number of regressive data points
n_input = 10
#size of each epoch (i.e. batch)
batch_size = 64
#number of hidden units in input layer lstm cell
#hidden layer number of units
#percentage to drop
dropout = 0.3

def read_data_sets(name):
    read_data_set = []
    with open(name, "r") as fault_data:
        for row in csv.reader(fault_data):
            read_data_set = np.append(read_data_set, np.array(row))
    return read_data_set

training_file = '../config/training_data.csv'
data_set = read_data_sets(training_file)
print("Loaded training data...")

def generate_train_test_data_sets():
    # divides the entire data set into sequences of 10 data points
    #data = np.reshape(data_set, [int(len(data_set)/5), n_features+1])
    #print(data)
    #data = data[int((len(data)/20)+1):]
    #data = np.reshape(data, [int(len(data)/n_input), n_input, n_features+1])
    #print(len(data))
    #print(np.as_array(data_set.shape()))
    data = np.reshape(data_set, [int(len(data_set)/5), n_features+1])
    print(len(data))
    data = np.reshape(data, [int(len(data)/n_input), n_input, n_features+1])
    print(len(data))
    # shuffles the set of sequences
    np.random.shuffle(data)

    # takes the tire pressure classification from every 10th data point in every sequence
    seg_label_data = data[:, n_input-1, n_features]
    # takes the feature data parameters from every sequence
    seg_feature_data = data[:, :, :n_features]

    return np.asarray(seg_feature_data), np.asarray(seg_label_data)

features, labels_norm = generate_train_test_data_sets()
print(len(features))
labels = []
# convert label data to one_hot arrays
for k in range(0, len(labels_norm)):
    one_hot_label = np.zeros([3], dtype=float)
    one_hot_label[int(float(labels_norm[k]))] = 1.0
    labels = np.append(labels, one_hot_label)
labels = np.reshape(labels, [-1, n_labels])

# Create LSTM
# expected input data shape: (batch_size, timesteps, data_dim)
model = Sequential()
model.add(LSTM(4, input_shape=(n_features, n_input), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(4))
model.add(Dense(n_labels, activation='sigmoid'))

l=[]
weights1=np.random.rand(10, 16) #weights
weights2=np.random.rand(4, 16) #weights
y=[-0.0014059, -0.00201148, -0.00739692,  0.00954951,  1.0000411, 0.9941291, 1.0001715, 1.0, -0.00176348, 0.01269362, 0.00883426, -0.00830622, 0.00263229, -0.00198024, -0.00776822, 0.0090275] #array of biases
l.append(weights1)
l.append(weights2)
l.append(np.asarray(y))
model.layers[0].set_weights(np.asarray(l)) #loaded_model.layer[0] being the layer

l=[]
weights1=np.random.rand(4, 16) #weights
weights2=np.random.rand(4, 16) #weights
y=[-0.0014059, -0.00201148, -0.00739692,  0.00954951,  1.0000411, 0.9941291, 1.0001715, 1.0, -0.00176348, 0.01269362, 0.00883426, -0.00830622, 0.00263229, -0.00198024, -0.00776822, 0.0090275] #array of biases
l.append(weights1)
l.append(weights2)
l.append(np.asarray(y))
model.layers[2].set_weights(np.asarray(l)) #loaded_model.layer[0] being the layer

l=[]
weights1=np.random.rand(4, 3) #weights
y=[0.02566409, -0.02650933, -0.00851871] #array of biases
l.append(weights1)
l.append(np.asarray(y))
model.layers[3].set_weights(np.asarray(l)) #loaded_model.layer[0] being the layer
model.compile(optimizer, loss)
#adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
#model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(np.reshape(features, (features.shape[0], n_features, features.shape[1])),labels, batch_size=batch_size, epochs=num_epochs, validation_split= .3)

weight_origin_0=model.layers[0].get_weights()
weight_origin_1=model.layers[2].get_weights()
weight_origin_2=model.layers[3].get_weights()

print("model shape")
print(np.asarray(model.layers).shape)
print("LSTM Layer 1")
print(np.asarray(weight_origin_0))
print("LSTM Layer 2")
print(np.asarray(weight_origin_1))
print("Dense Layer")
print(np.asarray(weight_origin_2))

# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

model_yaml = model.to_yaml()
with open("../config/model.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
model.save_weights("../config/model.h5")
