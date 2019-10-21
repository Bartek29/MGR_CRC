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
                                       batch_size=64)

test_it = datagen.flow_from_directory('database/real_test/',
                                      batch_size=64)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit_generator(train_it, epochs=3, validation_steps=8)
loss = model.evaluate_generator(test_it, steps=24)
print(loss)
# 2 classes:
# gen [181.09806474049887, 0.8313802]
# real [13.652371724446615, 0.99283856]
# 10 classes:
# gen [2512.6373901367188, 0.1953125]
# real [2.1766373813152313, 0.2467448]
model.save('crc.model')
