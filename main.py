# from common.logger import Logger
# from generator.parser import Parser
# from PIL import Image
#
# Logger.set_level(Logger.INFO)
# for i in range(2000):
#     # Logger().error("Create {}/2000".format(i))
#     p = Parser("schemas/h_capital_1.sch",
#                move_point_rnd=2,
#                paint_chance_rnd=0.8)
#     p.parse()
#     p.paint()
#     img = Image.open('test.bmp')
#
#     new_img = img.resize((128, 128))
#     new_img.save('database/gen_train/h_capital/train_{:04d}.png'.format(i), 'png')
#
# exit()

import tensorflow as tf  # deep learning library. Tensors are just multi-dimensional arrays

datagen = tf.keras.preprocessing.image.ImageDataGenerator()
train_it = datagen.flow_from_directory('database/real_train/',
                                       # batch_size=64,
                                       target_size=(32, 32),
                                       class_mode="sparse")

test_it = datagen.flow_from_directory('database/real_test/',
                                      # batch_size=64,
                                      target_size=(32, 32),
                                      class_mode="sparse")

# model = tf.keras.models.Sequential()
# model.add(tf.keras.layers.Flatten())
# model.add(tf.keras.layers.Dense(350, activation=tf.nn.relu))
# model.add(tf.keras.layers.Dense(150, activation=tf.nn.relu))
# model.add(tf.keras.layers.Dense(50, activation=tf.nn.relu))
# model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))



# model = tf.keras.models.Sequential()
#
# model.add(tf.keras.layers.Conv2D(32, (3, 3), input_shape=(32, 32, 3)))
# model.add(tf.keras.layers.Activation('relu'))
# model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
#
# model.add(tf.keras.layers.Conv2D(32, (3, 3)))
# model.add(tf.keras.layers.Activation('relu'))
# model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
#
# model.add(tf.keras.layers.Conv2D(64, (3, 3)))
# model.add(tf.keras.layers.Activation('relu'))
# model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
#
# model.add(tf.keras.layers.Flatten())
# model.add(tf.keras.layers.Dense(64))
# model.add(tf.keras.layers.Activation('relu'))
# model.add(tf.keras.layers.Dropout(0.5))
# model.add(tf.keras.layers.Dense(26))
# model.add(tf.keras.layers.Activation('sigmoid'))

# model.compile(optimizer='rmsprop',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
#
# model.fit_generator(train_it, epochs=1000, validation_steps=8)
# loss = model.evaluate_generator(test_it, steps=24)
# print(loss)

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
                    # validation_data=test_it
                    )

# 2 classes:
# gen [181.09806474049887, 0.8313802]
# real [13.652371724446615, 0.99283856]
# 10 classes:
# gen [2512.6373901367188, 0.1953125]
# real [2.1766373813152313, 0.2467448]
model.save('crc.model')
