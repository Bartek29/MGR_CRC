from common.logger import Logger
from generator.parser import Parser
from PIL import Image
import tensorflow as tf

Logger.set_level(Logger.INFO)

datagen = tf.keras.preprocessing.image.ImageDataGenerator()
train_it = datagen.flow_from_directory('database/gen_train/',
                                       # batch_size=64,
                                       target_size=(32, 32),
                                       class_mode="sparse")

test_it = datagen.flow_from_directory('database/real_test/',
                                      # batch_size=64,
                                      target_size=(32, 32),
                                      class_mode="sparse")

label_names = [
    "a_capital",
    "b_capital",
    "c_capital",
    "d_capital",
    "e_capital",
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

IMG_SHAPE = (32, 32, 3)
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

history = model.fit(train_it,
                    epochs=100,
                    steps_per_epoch=2,
                    validation_steps=2,
                    validation_data=test_it
                    )

model.save('crc.model')
