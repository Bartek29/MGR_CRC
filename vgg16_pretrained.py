from __future__ import absolute_import, division, print_function
from tqdm import tqdm
from numpy.random import randn

import pathlib
import random
import matplotlib.pyplot as plt

import tensorflow as tf
import numpy as np

from matplotlib.image import imread
from keras.preprocessing import image

tf.enable_eager_execution()

AUTOTUNE = tf.data.experimental.AUTOTUNE

PATH = "/"
data_dir = pathlib.Path(PATH + "database/gen_train")
test_dir = pathlib.Path(PATH + "database/real_test")

label_names = {
    "a_capital": 0,
    "b_capital": 1,
    "c_capital": 2,
    "d_capital": 3,
    "e_capital": 4,
    "f_capital": 5,
    "g_capital": 6,
    "h_capital": 7,
    "i_capital": 8,
    "j_capital": 9,
    "k_capital": 10,
    "l_capital": 11,
    "m_capital": 12,
    "n_capital": 13,
    "o_capital": 14,
    "p_capital": 15,
    "q_capital": 16,
    "r_capital": 17,
    "s_capital": 18,
    "t_capital": 19,
    "u_capital": 20,
    "v_capital": 21,
    "w_capital": 22,
    "x_capital": 23,
    "y_capital": 24,
    "z_capital": 25,
}

label_key = [
    "a_capital",
    "b_capital",
    "c_capital",
    "d_capital",
    "e_capital",
    "f_capital",
    "g_capital",
    "h_capital",
    "i_capital",
    "j_capital",
    "k_capital",
    "l_capital",
    "m_capital",
    "n_capital",
    "o_capital",
    "p_capital",
    "q_capital",
    "r_capital",
    "s_capital",
    "t_capital",
    "u_capital",
    "v_capital",
    "w_capital",
    "x_capital",
    "y_capital",
    "z_capital",
]

all_images = list(data_dir.glob('*/*'))
test_images = list(test_dir.glob('*/*'))
all_images = [str(path) for path in all_images]
test_images = [str(path) for path in test_images]
random.shuffle(all_images)
random.shuffle(test_images)

all_labels = [label_names[pathlib.Path(path).parent.name] for path in all_images]
test_labels = [label_names[pathlib.Path(path).parent.name] for path in test_images]

data_size = len(all_images)

train_test_split = (int)(data_size * 0.2)

x_train = all_images[train_test_split:]
x_test = all_images[:train_test_split]

y_train = all_labels[train_test_split:]
y_test = all_labels[:train_test_split]

IMG_SIZE = 32
BATCH_SIZE = 32


def _parse_data(x, y):
    image = tf.read_file(x)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.cast(image, tf.float32)
    image = (image / 127.5) - 1
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))

    return image, y


def _input_fn(x, y):
    ds = tf.data.Dataset.from_tensor_slices((x, y))
    ds = ds.map(_parse_data)
    ds = ds.shuffle(buffer_size=(int)(data_size*0.1))

    ds = ds.repeat()

    ds = ds.batch(BATCH_SIZE)

    ds = ds.prefetch(buffer_size=AUTOTUNE)

    return ds


train_ds = _input_fn(x_train, y_train)
validation_ds = _input_fn(x_test, y_test)
test_ds = _input_fn(test_images, test_labels)

IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)
VGG16_MODEL = tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
                                          include_top=False,
                                          weights='imagenet')

VGG16_MODEL.trainable = False
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(len(label_names),
                                         activation='softmax')


model = tf.keras.Sequential([
  VGG16_MODEL,
  global_average_layer,
  prediction_layer
])


model.compile(optimizer=tf.train.AdamOptimizer(),
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=["accuracy"])


history = model.fit(train_ds,
                    epochs=40,
                    steps_per_epoch=1000 ,
                    validation_steps=20,
                    validation_data=validation_ds)

validation_steps = 500
loss0, accuracy0 = model.evaluate(test_ds, steps=validation_steps)

print("loss: {:.2f}".format(loss0))
print("accuracy: {:.2f}".format(accuracy0))
